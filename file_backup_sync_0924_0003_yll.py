# 代码生成时间: 2025-09-24 00:03:38
import os
import shutil
import cherrypy
def backup_and_sync(source_path, destination_path):
    """备份并同步源路径中的文件到目标路径。"""
    # 检查源路径是否存在
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"源路径'{source_path}'不存在")
    
    # 检查目标路径是否存在，如果不存在则创建
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
        
    # 遍历源路径中的所有文件和目录
    for item in os.listdir(source_path):
        source_item_path = os.path.join(source_path, item)
        destination_item_path = os.path.join(destination_path, item)
        
        # 如果是文件，则复制到目标路径
        if os.path.isfile(source_item_path):
            try:
                shutil.copy2(source_item_path, destination_item_path)
            except Exception as e:
                print(f"文件'{item}'复制失败: {e}")
        
        # 如果是目录，则递归复制目录及其内容
        if os.path.isdir(source_item_path):
            try:
                backup_and_sync(source_item_path, destination_item_path)
            except Exception as e:
                print(f"目录'{item}'同步失败: {e}")
                
# CherryPy 服务配置
class FileBackupSync:
    def backup(self, source, destination):
        """ 提供备份和同步的Web接口 """
        try:
            backup_and_sync(source, destination)
            return {"status": "success", "message": "文件备份和同步成功"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
# 设置 CherryPy 配置
cherrypy.config.update({
    'server.socket_host': '0.0.0.0',
    'server.socket_port': 8080,
})

# 暴露服务接口
cherrypy.quickstart(FileBackupSync())