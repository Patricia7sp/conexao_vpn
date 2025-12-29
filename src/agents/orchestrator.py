from typing import Dict, Any, List
from crewai import Crew, Process
from langchain_openai import ChatOpenAI

from .connectivity_agent import ConnectivityAgent
from .file_agent import FileAgent
from .project_agent import ProjectAgent
from ..core.config import settings
from ..utils.logger import setup_logger

logger = setup_logger("orchestrator", settings.log.level, settings.log.log_file)

class AgentOrchestrator:
    def __init__(self, ubuntu_ip: str):
        self.ubuntu_ip = ubuntu_ip
        
        self.connectivity_agent = ConnectivityAgent(ubuntu_ip)
        self.file_agent = FileAgent()
        self.project_agent = ProjectAgent()
        
        self.llm = ChatOpenAI(
            model=settings.ai.model,
            temperature=settings.ai.temperature,
            api_key=settings.ai.openai_api_key
        )
    
    async def check_and_ensure_connection(self) -> Dict[str, Any]:
        logger.info("Checking connection status...")
        connection_status = await self.connectivity_agent.check_connection()
        
        if not connection_status["can_reach"]:
            logger.warning("Connection not available, attempting to establish...")
            result = await self.connectivity_agent.ensure_connection()
            return result
        
        return connection_status
    
    async def execute_file_operation(self, operation: str, **kwargs) -> Dict[str, Any]:
        logger.info(f"Executing file operation: {operation}")
        
        connection = await self.check_and_ensure_connection()
        if not connection.get("can_reach", False) and not connection.get("success", False):
            return {
                "error": "Cannot establish connection to Ubuntu server",
                "details": connection
            }
        
        if operation == "search":
            return await self.file_agent.smart_search(
                kwargs.get("query", ""),
                kwargs.get("base_path", "~")
            )
        
        return {"error": f"Unknown operation: {operation}"}
    
    async def execute_project_operation(self, operation: str, **kwargs) -> Dict[str, Any]:
        logger.info(f"Executing project operation: {operation}")
        
        connection = await self.check_and_ensure_connection()
        if not connection.get("can_reach", False) and not connection.get("success", False):
            return {
                "error": "Cannot establish connection to Ubuntu server",
                "details": connection
            }
        
        if operation == "analyze":
            return await self.project_agent.analyze_project(
                kwargs.get("project_path", "")
            )
        
        return {"error": f"Unknown operation: {operation}"}
    
    def create_crew_for_task(self, task_type: str, **kwargs) -> Crew:
        agents = []
        tasks = []
        
        agents.append(self.connectivity_agent.agent)
        tasks.append(self.connectivity_agent.create_monitoring_task())
        
        if task_type == "file_search":
            agents.append(self.file_agent.agent)
            tasks.append(self.file_agent.create_search_task(
                kwargs.get("query", ""),
                kwargs.get("base_path", "~")
            ))
        
        elif task_type == "project_analysis":
            agents.append(self.project_agent.agent)
            tasks.append(self.project_agent.create_project_analysis_task(
                kwargs.get("project_path", "")
            ))
        
        crew = Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
        
        return crew
    
    async def execute_intelligent_task(self, task_type: str, **kwargs) -> Dict[str, Any]:
        logger.info(f"Executing intelligent task: {task_type}")
        
        try:
            crew = self.create_crew_for_task(task_type, **kwargs)
            result = crew.kickoff()
            
            return {
                "task_type": task_type,
                "status": "completed",
                "result": str(result)
            }
        except Exception as e:
            logger.error(f"Error executing task: {e}")
            return {
                "task_type": task_type,
                "status": "failed",
                "error": str(e)
            }
