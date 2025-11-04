# 代码生成时间: 2025-11-04 08:22:10
import cherrypy
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.externals import joblib  # 用于保存和加载模型

"""
时间序列预测器
"""

class TimeSeriesPredictor:
    """时间序列预测器类"""
    def __init__(self):
        self.model = None
        self.training_data = None
        self.training_labels = None
        self.testing_data = None
        self.testing_labels = None

    def fit_model(self, data):
        """训练模型"""
        try:
            self.training_data, self.testing_data, \
                self.training_labels, self.testing_labels = train_test_split(data[:, 0], data[:, 1], test_size=0.2, random_state=42)
            self.model = LinearRegression()
            self.model.fit(self.training_data.reshape(-1, 1), self.training_labels)
            self.save_model()
        except Exception as e:
            raise ValueError("训练模型失败: " + str(e))

    def predict(self, data):
        """预测函数"""
        try:
            if self.model is None:
                raise ValueError("模型未训练")
            prediction = self.model.predict(data.reshape(-1, 1))
            return prediction
        except Exception as e:
            raise ValueError("预测失败: " + str(e))

    def save_model(self):
        """保存模型"""
        try:
            joblib.dump(self.model, 'time_series_predictor_model.pkl')
        except Exception as e:
            raise ValueError("保存模型失败: " + str(e))

    def load_model(self):
        """加载模型"""
        try:
            self.model = joblib.load('time_series_predictor_model.pkl')
        except Exception as e:
            raise ValueError("加载模型失败: " + str(e))

class TimeSeriesPredictorService:
    """时间序列预测服务"""
    def __init__(self):
        self.predictor = TimeSeriesPredictor()

    @cherrypy.expose
    def fit(self, data):
        """训练模型并返回训练结果"""
        try:
            np_data = np.array(data.split(','))
            self.predictor.fit_model(np_data)
            return "模型训练成功"
        except Exception as e:
            return str(e)

    @cherrypy.expose
    def predict(self, data):
        """预测并返回预测结果"""
        try:
            np_data = np.array([float(i) for i in data.split(',')])
            prediction = self.predictor.predict(np_data)
            return str(prediction[0])
        except Exception as e:
            return str(e)

if __name__ == '__main__':
    config = {
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': 8080
        }
    }
    cherrypy.quickstart(TimeSeriesPredictorService(), '/', config)