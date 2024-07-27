import os

import torch
from PyQt5.QtCore import QThread, pyqtSignal

import sys


# from yolov5.utils.torch_utils import select_device

class yoloThread(QThread):
    send_msg = pyqtSignal(str)
    send_result = pyqtSignal(str)

    def __init__(self):
        super(yoloThread, self).__init__()
        self.weight = '../yolov5/weight/yolov5s.pt'
        self.current_weight = '../yolov5/weight/best.pt'
        self.source = ''
        self.conf_thres = 0.25
        self.iou_thres = 0.45
        self.save_fold = '../../../pyqt5/result'

    @torch.no_grad
    def run(self, imgsize=640, device='', source='', half=False):
        try:
            print(source)
            # device = select_device(device)
            # half &= device.type != 'cpu'
            #
            # model = attempt_load(self.weight, map_location=device)
            # self.send_msg.emit('成功')
            cmd = "E:\IDE\Anaconda3\envs\yolov5_pyqt5\python.exe " + \
                  "E:\Code\Python\yolov5_pyqt5\yolov5\detect.py " + \
                  "--weight " + self.current_weight + \
                  "  --source " + source + "  --name  " + self.save_fold
            os.system(cmd)
            save_name = source.split('/')[-1]
            print(save_name)
            self.send_result.emit(save_name)
            self.send_msg.emit('成功')
        except Exception as e:
            self.send_msg(e)
