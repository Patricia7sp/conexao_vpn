import socket
import subprocess
import ipaddress
from typing import Optional, Tuple
import asyncio
from dataclasses import dataclass

@dataclass
class NetworkStatus:
    is_local_network: bool
    local_ip: Optional[str]
    can_reach_ubuntu: bool
    connection_type: str

class NetworkDetector:
    def __init__(self, local_subnet: str, ubuntu_ip: str, timeout: int = 5):
        self.local_subnet = ipaddress.ip_network(local_subnet)
        self.ubuntu_ip = ubuntu_ip
        self.timeout = timeout
    
    def get_local_ip(self) -> Optional[str]:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(0)
            s.connect(('10.254.254.254', 1))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception:
            return None
    
    def is_in_local_network(self, ip: str) -> bool:
        try:
            return ipaddress.ip_address(ip) in self.local_subnet
        except ValueError:
            return False
    
    async def ping_host(self, host: str) -> bool:
        try:
            process = await asyncio.create_subprocess_exec(
                'ping', '-c', '1', '-W', str(self.timeout), host,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await asyncio.wait_for(process.communicate(), timeout=self.timeout + 1)
            return process.returncode == 0
        except (asyncio.TimeoutError, Exception):
            return False
    
    async def check_tcp_connection(self, host: str, port: int) -> bool:
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(host, port),
                timeout=self.timeout
            )
            writer.close()
            await writer.wait_closed()
            return True
        except Exception:
            return False
    
    async def detect_network_status(self) -> NetworkStatus:
        local_ip = self.get_local_ip()
        is_local = False
        
        if local_ip:
            is_local = self.is_in_local_network(local_ip)
        
        can_reach = await self.ping_host(self.ubuntu_ip)
        
        if is_local and can_reach:
            connection_type = "local"
        elif can_reach:
            connection_type = "vpn"
        else:
            connection_type = "disconnected"
        
        return NetworkStatus(
            is_local_network=is_local,
            local_ip=local_ip,
            can_reach_ubuntu=can_reach,
            connection_type=connection_type
        )
    
    def is_tailscale_active(self) -> bool:
        try:
            result = subprocess.run(
                ['tailscale', 'status'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False
    
    async def ensure_connection(self) -> Tuple[bool, str]:
        status = await self.detect_network_status()
        
        if status.can_reach_ubuntu:
            return True, status.connection_type
        
        if self.is_tailscale_active():
            await asyncio.sleep(2)
            status = await self.detect_network_status()
            if status.can_reach_ubuntu:
                return True, "vpn"
        
        return False, "failed"
