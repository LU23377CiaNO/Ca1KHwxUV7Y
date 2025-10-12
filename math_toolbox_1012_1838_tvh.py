# 代码生成时间: 2025-10-12 18:38:43
import cherrypy

# 定义一个类，用于提供数学计算工具集
class MathToolbox:
    """
    数学计算工具集，提供加、减、乘、除等基本数学运算功能。
    """

    def add(self, a, b):
        """
        加法运算
        :param a: 第一个加数
        :type a: float
        :param b: 第二个加数
        :type b: float
        :return: 两个数的和
        :rtype: float
        """
        return a + b

    def subtract(self, a, b):
        """
        减法运算
        :param a: 被减数
        :type a: float
        :param b: 减数
        :type b: float
        :return: 两个数的差
        :rtype: float
        """
        return a - b

    def multiply(self, a, b):
        """
        乘法运算
        :param a: 第一个乘数
        :type a: float
        :param b: 第二个乘数
        :type b: float
        :return: 两个数的积
        :rtype: float
        """
        return a * b

    def divide(self, a, b):
        """
        除法运算
        :param a: 被除数
        :type a: float
        :param b: 除数
        :type b: float
        :return: 两个数的商
        :rtype: float
        :raises ValueError: 当除数为0时抛出异常
        """
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a / b

    def power(self, a, b):
        """
        幂运算
        :param a: 底数
        :type a: float
        :param b: 指数
        :type b: float
        :return: 幂运算的结果
        :rtype: float
        """
        return a ** b


# 定义config字典，用于配置CherryPy服务器
config = {
    'global': {
        'server.socket_host': '0.0.0.0',  # 监听所有可用的IP地址
        'server.socket_port': 8080,       # 设置端口号为8080
    }
}

# 定义暴露的路由和对应的方法
class Root:
    def index(self):
        """
        主页函数，返回欢迎信息。
        """
        return "Welcome to the Math Toolbox!"

    def add(self, a, b):
        """
        加法运算请求处理函数
        """
        return str(MathToolbox().add(float(a), float(b)))

    def subtract(self, a, b):
        """
        减法运算请求处理函数
        """
        return str(MathToolbox().subtract(float(a), float(b)))

    def multiply(self, a, b):
        """
        乘法运算请求处理函数
        """
        return str(MathToolbox().multiply(float(a), float(b)))

    def divide(self, a, b):
        """
        除法运算请求处理函数
        """
        try:
            return str(MathToolbox().divide(float(a), float(b)))
        except ValueError as e:
            return str(e)

    def power(self, a, b):
        """
        幂运算请求处理函数
        """
        return str(MathToolbox().power(float(a), float(b)))

# 设置暴露的路由和对应的方法
exposed_methods = {
    'add': Root.add,
    'subtract': Root.subtract,
    'multiply': Root.multiply,
    'divide': Root.divide,
    'power': Root.power,
}

# 设置暴露的方法的参数，这里使用*args和**kwargs来接受任意数量的参数
exposed_methods_args = {
    'add': ['a', 'b'],
    'subtract': ['a', 'b'],
    'multiply': ['a', 'b'],
    'divide': ['a', 'b'],
    'power': ['a', 'b'],
}

# 设置暴露的方法的属性，这里设置允许GET和POST请求
exposed_methods_props = {
    'add': {'methods': ['GET', 'POST']},
    'subtract': {'methods': ['GET', 'POST']},
    'multiply': {'methods': ['GET', 'POST']},
    'divide': {'methods': ['GET', 'POST']},
    'power': {'methods': ['GET', 'POST']},
}

if __name__ == '__main__':
    # 配置CherryPy服务器
    cherrypy.config.update(config)
    # 配置路由和对应的方法
    cherrypy.quickstart(Root(), '/', exposed_methods, exposed_methods_args, exposed_methods_props)