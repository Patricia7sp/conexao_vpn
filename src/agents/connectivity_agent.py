from typing import Dict, Any, Optional
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI

from ..core.config import settings
from ..utils.logger import setup_logger
from ..utils.network_detector import NetworkDetector

logger = setup_logger("connectivity_agent", settings.log.level, settings.log.log_file)

class ConnectivityAgent:
    def __init__(self, ubuntu_ip: str):
        self.ubuntu_ip = ubuntu_ip
        self.network_detector = NetworkDetector(
            settings.network.local_subnet,
            ubuntu_ip,
            settings.network.connection_timeout
        )
        
        self.llm = ChatOpenAI(
            model=settings.ai.model,
            temperature=settings.ai.temperature,
            api_key=settings.ai.openai_api_key
        )
        
        self.agent = Agent(
            role="Network Connectivity Specialist",
            goal="Ensure stable and optimal connection between MacBook and Ubuntu server",
            backstory="""You are an expert in network connectivity and VPN management.
            Your job is to monitor network status, detect connection issues, and automatically
            switch between local network and VPN connections to maintain seamless access.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    async def check_connection(self) -> Dict[str, Any]:
        status = await self.network_detector.detect_network_status()
        
        logger.info(f"Connection check: {status.connection_type}")
        
        return {
            "status": status.connection_type,
            "is_local": status.is_local_network,
            "can_reach": status.can_reach_ubuntu,
            "local_ip": status.local_ip,
            "recommendation": self._get_recommendation(status)
        }
    
    def _get_recommendation(self, status) -> str:
        if status.connection_type == "local":
            return "Using local network - optimal performance"
        elif status.connection_type == "vpn":
            return "Using VPN connection - secure remote access"
        else:
            return "Connection failed - check Tailscale or network settings"
    
    async def ensure_connection(self) -> Dict[str, Any]:
        success, conn_type = await self.network_detector.ensure_connection()
        
        if success:
            logger.info(f"Connection established via {conn_type}")
            return {
                "success": True,
                "connection_type": conn_type,
                "message": f"Successfully connected via {conn_type}"
            }
        else:
            logger.error("Failed to establish connection")
            return {
                "success": False,
                "connection_type": "none",
                "message": "Failed to establish connection. Please check network settings."
            }
    
    def create_monitoring_task(self) -> Task:
        return Task(
            description="""Monitor the network connection between MacBook and Ubuntu server.
            Check if we're on the same local network or need to use VPN.
            Ensure the connection is stable and recommend actions if needed.""",
            agent=self.agent,
            expected_output="Network status report with connection type and recommendations"
        )
