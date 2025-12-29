from typing import Dict, Any, List, Optional
from crewai import Agent, Task
from langchain_openai import ChatOpenAI

from ..core.config import settings
from ..utils.logger import setup_logger

logger = setup_logger("file_agent", settings.log.level, settings.log.log_file)

class FileAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.ai.model,
            temperature=settings.ai.temperature,
            api_key=settings.ai.openai_api_key
        )
        
        self.agent = Agent(
            role="File Management Specialist",
            goal="Efficiently manage, search, and organize files on the Ubuntu system",
            backstory="""You are an expert in file systems and data organization.
            Your job is to help users find, read, and manage their files intelligently.
            You understand file structures, can search efficiently, and provide
            smart recommendations for file operations.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def create_search_task(self, query: str, base_path: str = "~") -> Task:
        return Task(
            description=f"""Search for files matching the query: '{query}'
            Starting from base path: {base_path}
            Provide intelligent search results with relevance ranking.""",
            agent=self.agent,
            expected_output="List of relevant files with paths and descriptions"
        )
    
    def create_organization_task(self, path: str) -> Task:
        return Task(
            description=f"""Analyze the file structure at: {path}
            Provide recommendations for better organization if needed.
            Identify duplicate files, large files, and suggest cleanup actions.""",
            agent=self.agent,
            expected_output="File organization analysis and recommendations"
        )
    
    async def smart_search(self, query: str, base_path: str = "~") -> Dict[str, Any]:
        logger.info(f"Smart search for: {query} in {base_path}")
        
        return {
            "query": query,
            "base_path": base_path,
            "status": "search_initiated",
            "message": "File search agent is processing your request"
        }
