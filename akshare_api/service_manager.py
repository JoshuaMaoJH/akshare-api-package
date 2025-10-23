# -*- coding: utf-8 -*-
"""
AKTools服务管理器
自动安装、启动和管理AKTools服务
"""

import os
import sys
import time
import signal
import subprocess
import threading
import requests
from typing import Optional, List
from pathlib import Path


class AKToolsServiceManager:
    """AKTools服务管理器"""
    
    def __init__(self, port: int = 8080, auto_start: bool = True):
        """
        初始化服务管理器
        
        Args:
            port: 服务端口，默认8080
            auto_start: 是否自动启动服务
        """
        self.port = port
        self.auto_start = auto_start
        self.base_url = f"http://127.0.0.1:{port}"
        self.process: Optional[subprocess.Popen] = None
        self._service_thread: Optional[threading.Thread] = None
        self._shutdown_event = threading.Event()
        
        # 检查aktools是否已安装
        self._check_aktools_installation()
        
        if auto_start:
            self.start_service()
    
    def _check_aktools_installation(self) -> bool:
        """检查AKTools是否已安装"""
        try:
            result = subprocess.run(
                [sys.executable, "-c", "import aktools; print('aktools installed')"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                print("✅ AKTools已安装")
                return True
        except Exception:
            pass
        
        print("⚠️  AKTools未安装，正在自动安装...")
        return self._install_aktools()
    
    def _install_aktools(self) -> bool:
        """自动安装AKTools"""
        try:
            print("正在安装AKTools...")
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "aktools", "--upgrade"],
                capture_output=True,
                text=True,
                timeout=300  # 5分钟超时
            )
            
            if result.returncode == 0:
                print("✅ AKTools安装成功")
                return True
            else:
                print(f"❌ AKTools安装失败: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ AKTools安装超时")
            return False
        except Exception as e:
            print(f"❌ AKTools安装异常: {e}")
            return False
    
    def _is_service_running(self) -> bool:
        """检查服务是否正在运行"""
        try:
            response = requests.get(f"{self.base_url}/api/public/stock_sse_summary", timeout=5)
            return response.status_code == 200
        except Exception:
            return False
    
    def _start_service_process(self) -> bool:
        """启动AKTools服务进程"""
        try:
            # 启动AKTools服务
            self.process = subprocess.Popen(
                [sys.executable, "-m", "aktools"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                preexec_fn=os.setsid if os.name != 'nt' else None
            )
            
            # 等待服务启动
            print("正在启动AKTools服务...")
            for i in range(30):  # 等待30秒
                if self._is_service_running():
                    print(f"✅ AKTools服务启动成功 (端口: {self.port})")
                    return True
                time.sleep(1)
                if i % 5 == 0 and i > 0:
                    print(f"等待服务启动... ({i}s)")
            
            print("❌ AKTools服务启动超时")
            return False
            
        except Exception as e:
            print(f"❌ 启动AKTools服务失败: {e}")
            return False
    
    def start_service(self) -> bool:
        """启动服务"""
        if self._is_service_running():
            print("✅ AKTools服务已在运行")
            return True
        
        if self.process and self.process.poll() is None:
            print("✅ AKTools服务进程已在运行")
            return True
        
        return self._start_service_process()
    
    def stop_service(self):
        """停止服务"""
        if self.process:
            try:
                if os.name == 'nt':  # Windows
                    self.process.terminate()
                else:  # Unix/Linux
                    os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
                
                # 等待进程结束
                try:
                    self.process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    # 强制杀死进程
                    if os.name == 'nt':
                        self.process.kill()
                    else:
                        os.killpg(os.getpgid(self.process.pid), signal.SIGKILL)
                
                print("✅ AKTools服务已停止")
            except Exception as e:
                print(f"⚠️  停止服务时出现异常: {e}")
            finally:
                self.process = None
    
    def restart_service(self) -> bool:
        """重启服务"""
        print("正在重启AKTools服务...")
        self.stop_service()
        time.sleep(2)
        return self.start_service()
    
    def get_service_status(self) -> dict:
        """获取服务状态"""
        status = {
            "running": False,
            "port": self.port,
            "base_url": self.base_url,
            "process_id": None,
            "response_time": None
        }
        
        if self.process and self.process.poll() is None:
            status["process_id"] = self.process.pid
        
        if self._is_service_running():
            status["running"] = True
            try:
                start_time = time.time()
                response = requests.get(f"{self.base_url}/api/public/stock_sse_summary", timeout=5)
                status["response_time"] = (time.time() - start_time) * 1000  # 毫秒
            except Exception:
                pass
        
        return status
    
    def __enter__(self):
        """上下文管理器入口"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        if self.auto_start:
            self.stop_service()
    
    def __del__(self):
        """析构函数"""
        if hasattr(self, 'process') and self.process:
            self.stop_service()


# 全局服务管理器实例
_service_manager: Optional[AKToolsServiceManager] = None


def get_service_manager(port: int = 8080, auto_start: bool = True) -> AKToolsServiceManager:
    """获取全局服务管理器实例"""
    global _service_manager
    
    if _service_manager is None:
        _service_manager = AKToolsServiceManager(port=port, auto_start=auto_start)
    
    return _service_manager


def ensure_service_running(port: int = 8080) -> bool:
    """确保服务正在运行"""
    manager = get_service_manager(port=port, auto_start=True)
    return manager.start_service()


def stop_service():
    """停止全局服务"""
    global _service_manager
    if _service_manager:
        _service_manager.stop_service()
        _service_manager = None
