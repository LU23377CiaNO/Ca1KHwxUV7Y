# 代码生成时间: 2025-09-23 20:51:03
import cherrypy
from cherrypy.lib import sessions

# 配置CherryPy Sessions
conf = {
    "/": {
        "tools.sessions.on": True,
        "tools.sessions.timeout": 60,
    }
}

class UserPermissionSystem:
    """用户权限管理系统。"""

    def __init__(self):
        # 初始化权限列表
        self.permissions = {}

    @cherrypy.expose
    def set_permission(self, user_id, permission):
        """设置用户权限。"""
        if user_id not in self.permissions:
            self.permissions[user_id] = set()
        self.permissions[user_id].add(permission)
        return f"Permission set for user {user_id}: {permission}"

    @cherrypy.expose
    def remove_permission(self, user_id, permission):
        """移除用户权限。"""
        if user_id in self.permissions and permission in self.permissions[user_id]:
            self.permissions[user_id].remove(permission)
            return f"Permission removed for user {user_id}: {permission}"
        else:
            raise cherrypy.HTTPError(404, f"Permission or user not found for user_id: {user_id}")

    @cherrypy.expose
    def check_permission(self, user_id, permission):
        """检查用户是否有特定权限。"""
        has_permission = permission in self.permissions.get(user_id, set())
        return f"User {user_id} has permission '{permission}': {has_permission}"

    @cherrypy.expose
    def list_permissions(self, user_id):
        """列出用户的所有权限。"""
        if user_id in self.permissions:
            return f"Permissions for user {user_id}: {self.permissions[user_id]}"
        else:
            raise cherrypy.HTTPError(404, f"User not found for user_id: {user_id}")

if __name__ == '__main__':
    # 初始化CherryPy应用
    cherrypy.quickstart(UserPermissionSystem(), config=conf)