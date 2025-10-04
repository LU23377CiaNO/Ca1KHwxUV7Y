# 代码生成时间: 2025-10-05 02:39:21
import cherrypy
from cherrypy.process.plugins import Monitor
from cherrypy.lib import server
import threading
import time

# 定时任务调度器
class SchedulerService:
    def __init__(self):
        # 初始化定时任务列表
        self.tasks = []

    def add_task(self, task):
        # 添加定时任务
        self.tasks.append(task)

    def run(self):
        # 运行定时任务调度器
        while True:
            for task in self.tasks:
                task()
            time.sleep(1)  # 每秒检查一次任务

    def start(self):
        # 启动定时任务调度器
        threading.Thread(target=self.run).start()

# CherryPy服务
class CherryPyService:
    @cherrypy.expose
    def index(self):
        # 首页
        return "Welcome to Scheduler Service"

    @cherrypy.expose
    def add(self, task_name):
        # 添加定时任务
        try:
            # 根据任务名称获取任务函数
            task = globals()[task_name]
            # 添加任务到调度器
            scheduler.add_task(task)
            return f"Task {task_name} added successfully"
        except KeyError:
            return f"Task {task_name} not found"
        except Exception as e:
            return f"Error adding task: {str(e)}"

# 定时任务示例
def task1():
    # 任务1: 打印当前时间
    print("Task 1: ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

def task2():
    # 任务2: 计算1到100的和
    print("Task 2: Sum of 1 to 100 =", sum(range(1, 101)))

if __name__ == '__main__':
    # 创建调度器实例
    scheduler = SchedulerService()
    # 启动调度器
    scheduler.start()
    
    # 配置CherryPy服务
    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': 8080})
    cherrypy.quickstart(CherryPyService())