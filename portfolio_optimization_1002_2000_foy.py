# 代码生成时间: 2025-10-02 20:00:43
import cherrypy
from math import sqrt

# 投资组合优化的参数和结果存储类
class PortfolioOptimization:
    def __init__(self):
        self.portfolios = []

    # 计算投资组合的标准差
    def calculate_std_dev(self, portfolio):
        portfolio_variance = sum((portfolio[i] * portfolio[i] for i in range(len(portfolio))))
        return sqrt(portfolio_variance)

    # 添加投资组合
    def add_portfolio(self, portfolio):
        if len(portfolio) < 2:
            raise ValueError('投资组合至少需要两种资产')
        self.portfolios.append(portfolio)

    # 获取最优投资组合
    def get_optimal_portfolio(self):
        # 这里简化处理，返回标准差最小的投资组合
        optimal_portfolio = min(self.portfolios, key=self.calculate_std_dev)
        return optimal_portfolio

# 暴露HTTP端点
class PortfolioOptimizationService:
    @cherrypy.expose
    def index(self):
        return "欢迎使用投资组合优化服务"

    # 添加投资组合的HTTP端点
    @cherrypy.expose
    def add_portfolio(self, portfolio_data):
        try:
            portfolio = [float(asset) for asset in portfolio_data.split(',')]
            opt = PortfolioOptimization()
            opt.add_portfolio(portfolio)
            return "投资组合添加成功"
        except ValueError as e:
            return f"添加投资组合失败：{e}"

    # 获取最优投资组合的HTTP端点
    @cherrypy.expose
    def get_optimal_portfolio(self):
        try:
            opt = PortfolioOptimization()
            # 假设opt.portfolios已经被填充
            optimal_portfolio = opt.get_optimal_portfolio()
            return f"最优投资组合：{optimal_portfolio}"
        except ValueError as e:
            return f"获取最优投资组合失败：{e}"

if __name__ == '__main__':
    conf = {
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': 8080,
        },
    }
    cherrypy.quickstart(PortfolioOptimizationService(), '/', config=conf)