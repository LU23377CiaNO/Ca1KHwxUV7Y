# 代码生成时间: 2025-10-09 02:52:22
import cherrypy
from cherrypy.lib import static
import cv2
import numpy as np
from PIL import Image
import io
import json
import logging

# 设置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 物体检测算法类
class ObjectDetectionService:
    def __init__(self):
        self.model = cv2.dnn.readNetFromCaffe(
            'deploy.prototxt',
            'res10_300x300_ssd_iter_140000.caffemodel'
        )

    @cherrypy.expose
    def detect(self, image_path):
        """
        物体检测接口
        :param image_path: 图片路径
        :return: 检测结果，包含物体名称和位置
        """
        try:
            # 读取图片
            image = cv2.imread(image_path)
            if image is None:
                raise FileNotFoundError(f'Image not found at {image_path}')

            # 转换图片到blob
            blob = cv2.dnn.blobFromImage(
                cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0)
            )

            # 设置网络输入
            self.model.setInput(blob)

            # 获取检测结果
            detections = self.model.forward()

            # 处理检测结果
            results = []
            for i in range(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > 0.2:
                    # 获取物体类别和位置
                    obj_class = int(detections[0, 0, i, 1])
                    x1 = int(detections[0, 0, i, 3] * image.shape[1])
                    y1 = int(detections[0, 0, i, 4] * image.shape[0])
                    x2 = int(detections[0, 0, i, 5] * image.shape[1])
                    y2 = int(detections[0, 0, i, 6] * image.shape[0])
                    results.append({
                        'class': obj_class,
                        'confidence': confidence,
                        'x1': x1,
                        'y1': y1,
                        'x2': x2,
                        'y2': y2
                    })

            return json.dumps(results)
        except Exception as e:
            logger.error(f'Error in detect: {e}')
            raise cherrypy.HTTPError(500, 'Failed to detect objects')

# 设置CherryPy服务器
class Root(object):
    @cherrypy.expose
    def index(self):
        return 'Object Detection Service'

    def detect(self):
        return ObjectDetectionService().detect

if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': 8080})
    cherrypy.quickstart(Root())