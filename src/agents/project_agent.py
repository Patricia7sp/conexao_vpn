from typing import Dict, Any, List
from crewai import Agent, Task
from langchain_openai import ChatOpenAI

from ..core.config import settings
from ..utils.logger import setup_logger

logger = setup_logger("project_agent", settings.log.level, settings.log.log_file)

class ProjectAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.ai.model,
            temperature=settings.ai.temperature,
            api_key=settings.ai.openai_api_key
        )
        
        self.agent = Agent(
            role="Development Project Manager",
            goal="Manage and organize development projects and coding environments",
            backstory="""You are an expert in software development project management.
            You understand project structures, dependencies, virtual environments,
            and can help developers navigate their codebase efficiently.
            You provide intelligent insights about project status and organization.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def create_project_analysis_task(self, project_path: str) -> Task:
        return Task(
            description=f"""Analyze the development project at: {project_path}
            Identify:
            - Project type and framework
            - Dependencies and requirements
            - Project structure and organization
            - Active branches (if git repo)
            - Recent changes and activity""",
            agent=self.agent,
            expected_output="Comprehensive project analysis report"
        )
    
    def create_dependency_check_task(self, project_path: str) -> Task:
        return Task(
            description=f"""Check dependencies for project at: {project_path}
            Verify:
            - All dependencies are installed
            - Version compatibility
            - Missing or outdated packages
            - Security vulnerabilities""",
            agent=self.agent,
            expected_output="Dependency status report with recommendations"
        )
    
    async def analyze_project(self, project_path: str) -> Dict[str, Any]:
        logger.info(f"Analyzing project: {project_path}")
        
        return {
            "project_path": project_path,
            "status": "analysis_initiated",
            "message": "Project agent is analyzing your development environment"
        }
