# 代码生成时间: 2025-10-18 01:21:34
import cherrypy
import time
from datetime import datetime
import socket
import logging

# 设置日志记录
logging.basicConfig(filename='network_latency.log', level=logging.INFO)

class LatencyMonitor:
    """监控网络延迟的类"""

    def __init__(self):
        self.targets = ['google.com', 'facebook.com', 'twitter.com']  # 监控目标

    def _ping(self, hostname):
        """发送ping命令并计算延迟"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)  # 设置超时为1秒
                start_time = time.time()
                s.connect((hostname, 80))  # 尝试连接HTTP端口
                s.close()
                end_time = time.time()
                return end_time - start_time  # 返回延迟时间（秒）
        except socket.error as e:
            logging.error(f"Ping {hostname} failed: {e}")
            return None

    @cherrypy.expose
    def get_latency(self):
        """处理GET请求，返回所有目标的网络延迟"""
        results = {}
        for hostname in self.targets:
            latency = self._ping(hostname)
            if latency is not None:
                results[hostname] = latency
            else:
                results[hostname] = 'Timeout'
        return results

    @cherrypy.expose
    def ping_all(self):
        """处理GET请求，对所有目标进行ping操作，并记录日志"""
        for hostname in self.targets:
            latency = self._ping(hostname)
            if latency is not None:
                logging.info(f"{datetime.now()}: {hostname} latency is {latency} seconds")
            else:
                logging.info(f"{datetime.now()}: Ping {hostname} failed")

if __name__ == '__main__':
    # 设置CherryPy服务器的配置
    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': 8080})
    # 启动CherryPy服务器
    cherrypy.quickstart(LatencyMonitor())