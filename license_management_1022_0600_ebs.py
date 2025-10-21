# 代码生成时间: 2025-10-22 06:00:22
import cherrypy
from cherrypy.lib import sessions
from cherrypy._cpdispatch import Dispatcher
from cherrypy.lib.auth import basic_auth
import os
import json

# 配置会话
sessions.SESSION_COOKIE_NAME = 'license_mgmt_session'

# 配置CherryPy
class LicenseManagement(Dispatcher):
    # 首页
    @cherrypy.expose
    def index(self):
        return 'Welcome to License Management System!'

    # 许可证列表页面
    @cherrypy.expose
    def licenses(self):
        # 获取许可证数据
        try:
            with open('licenses.json', 'r') as file:
                licenses = json.load(file)
        except FileNotFoundError:
            return 'License data not found!'
        
        return json.dumps(licenses)

    # 添加许可证
    @cherrypy.expose
    @basic_auth('admin', 'password123')  # 基本认证
    def add_license(self, license_data):
        try:
            with open('licenses.json', 'r') as file:
                licenses = json.load(file)
        except FileNotFoundError:
            licenses = []
        
        try:
            license = json.loads(license_data)
            licenses.append(license)
            with open('licenses.json', 'w') as file:
                json.dump(licenses, file, indent=4)
            return 'License added successfully!'
        except json.JSONDecodeError:
            return 'Invalid JSON format!'

    # 更新许可证
    @cherrypy.expose
    @basic_auth('admin', 'password123')  # 基本认证
    def update_license(self, license_id, license_data):
        try:
            with open('licenses.json', 'r') as file:
                licenses = json.load(file)
        except FileNotFoundError:
            return 'License data not found!'
        
        try:
            license = json.loads(license_data)
            if license_id < len(licenses):
                licenses[license_id] = license
                with open('licenses.json', 'w') as file:
                    json.dump(licenses, file, indent=4)
                return 'License updated successfully!'
            else:
                return 'License ID not found!'
        except json.JSONDecodeError:
            return 'Invalid JSON format!'

    # 删除许可证
    @cherrypy.expose
    @basic_auth('admin', 'password123')  # 基本认证
    def delete_license(self, license_id):
        try:
            with open('licenses.json', 'r') as file:
                licenses = json.load(file)
        except FileNotFoundError:
            return 'License data not found!'
        
        if license_id < len(licenses):
            del licenses[license_id]
            with open('licenses.json', 'w') as file:
                json.dump(licenses, file, indent=4)
            return 'License deleted successfully!'
        else:
            return 'License ID not found!'

# 配置CherryPy服务器
if __name__ == '__main__':
    conf = {
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': 8080,
        },
    }
    cherrypy.quickstart(LicenseManagement(), '/', conf)