import aiohttp
import logging
import asyncio
import subprocess
from typing import Optional

logger = logging.getLogger(__name__)

class VPNConnector:
    def __init__(self):
        self.vpn_interface = "tun0"
        self.vpn_gateway_ip = "10.8.0.1"  # Стандартный gateway для OpenVPN
        
    async def is_vpn_connected(self) -> bool:
        """Проверяет, подключен ли VPN"""
        try:
            # Проверяем существование tun0 интерфейса
            result = subprocess.run(
                ["ip", "addr", "show", self.vpn_interface], 
                capture_output=True, 
                text=True,
                timeout=5
            )
            return result.returncode == 0 and "inet" in result.stdout
        except Exception as e:
            logger.error(f"Ошибка проверки VPN: {e}")
            return False
    
    async def add_route_for_host(self, hostname: str) -> bool:
        """Добавляет маршрут для конкретного хоста через VPN"""
        try:
            # Резолвим hostname в IP
            import socket
            ip = socket.gethostbyname(hostname)
            
            # Добавляем маршрут через VPN интерфейс
            result = subprocess.run([
                "sudo", "ip", "route", "add", f"{ip}/32", "dev", self.vpn_interface
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                logger.info(f"Добавлен маршрут для {hostname} ({ip}) через VPN")
                return True
            else:
                logger.warning(f"Маршрут для {hostname} уже существует или ошибка: {result.stderr}")
                return True  # Возможно, маршрут уже есть
                
        except Exception as e:
            logger.error(f"Ошибка добавления маршрута для {hostname}: {e}")
            return False
    
    async def create_vpn_session(self) -> Optional[aiohttp.ClientSession]:
        """Создает HTTP сессию, которая использует VPN"""
        try:
            # Проверяем VPN подключение
            if not await self.is_vpn_connected():
                logger.error("VPN не подключен")
                return None
            
            # Добавляем маршрут для Google API
            await self.add_route_for_host("generativelanguage.googleapis.com")
            
            # Создаем коннектор с привязкой к VPN интерфейу
            connector = aiohttp.TCPConnector(
                local_addr=await self._get_vpn_local_ip(),
                limit=10,
                limit_per_host=5
            )
            
            session = aiohttp.ClientSession(
                connector=connector,
                timeout=aiohttp.ClientTimeout(total=60)
            )
            
            logger.info("Создана VPN HTTP сессия")
            return session
            
        except Exception as e:
            logger.error(f"Ошибка создания VPN сессии: {e}")
            return None
    
    async def _get_vpn_local_ip(self) -> Optional[str]:
        """Получает локальный IP адрес VPN интерфейса"""
        try:
            result = subprocess.run([
                "ip", "addr", "show", self.vpn_interface
            ], capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0:
                # Ищем строку с inet
                for line in result.stdout.split('\n'):
                    if 'inet ' in line and not 'inet6' in line:
                        # Извлекаем IP адрес
                        ip = line.strip().split()[1].split('/')[0]
                        logger.info(f"VPN локальный IP: {ip}")
                        return ip
            
            logger.error("Не удалось получить VPN IP")
            return None
            
        except Exception as e:
            logger.error(f"Ошибка получения VPN IP: {e}")
            return None
