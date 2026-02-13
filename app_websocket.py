import time
import base64
from PIL import Image
import torch
import numpy as np
from utils.augmentations import letterbox
from utils.general import (non_max_suppression, scale_coords)
from models.experimental import attempt_load
import io
import socketio

# 创建Socket.IO服务器
sio = socketio.Server(max_http_buffer_size=10000000)
app = socketio.WSGIApp(sio)

@sio.event
def connect(sid, environ):
    print('Client connected:', sid)

@sio.event
def disconnect(sid):
    print('Client disconnected:', sid)

@sio.event
def frame(sid, data):
    base64_img0 = data
    print('Received base64 image data (log 100):', base64_img0[:100])
    '''
    sio.emit('net_delay', [], to=sid)
    start_time = time.time()
    coords_list=process_image(base64_img0)
    # 记录结束时间
    end_time = time.time()
    # 计算执行时间（以毫秒为单位）
    execution_time_ms = (end_time - start_time) * 1000
    print(f"ALL Recognition Time Consuming: {execution_time_ms:.2f} ms")
    print('Have inferenced a picture and the result is:',coords_list)
    '''
    # 将列表发送回客户端
    response_list = [[1, 2, 8, 4], [3, 0, 0, 8]]   #example
    sio.emit('inference_result', response_list, to=sid)

# 置信率
conf_thres = 0.2
# 默认0.45效果较好
iou_thres = 0.5
# 权重文件名
weights = 'best.pt'

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(device)
# 判断设备类型并仅使用一张GPU进行测试
half = device != 'cpu'
# 载入模型
model = attempt_load(weights, device=device)
# 将模型的stride赋给stride变量 32
stride = max(int(model.stride.max()), 32)  # model stride
model.half()  # to FP16

def process_image(img):
    # 解码 Base64 数据为二进制图像数据
    #image_data = base64.b64decode(img)
    # 将二进制图像数据转换为 PIL 图像对象
    image = Image.open(io.BytesIO(img))
    # 将 PIL 图像对象转换为 NumPy 数组
    img0 = np.array(image)
    # 记录识别对象坐标
    tars = []
    # 将图像缩放到指定尺寸
    img = letterbox(img0, stride=stride)[0]
    # 函数将一个内存不连续存储的数组转换为内存连续存储的数组,使得运行速度更快
    img = np.ascontiguousarray(img)
    # 把数组转换成张量,且二者共享内存
    img = torch.from_numpy(img).to(device)
    img = img.half() if half else img.float()
    # 压缩数据维度
    img /= 255  # 0 - 255 to 0.0 - 1.0
    if len(img.shape) == 3:
        img = img[None]
    # 对tensor进行转置
    img = img.permute(0, 3, 1, 2)
    # Inference 模型推理
    pred = model(img, augment=False, visualize=False)[0]
    # NMS 非极大值抑制 即只输出概率最大的分类结果
    pred = non_max_suppression(pred, conf_thres, iou_thres)
    # 处理预测识别结果
    for i, det in enumerate(pred):  # per image
        if len(det):
            # Rescale boxes from img_size to im0 size
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], img0.shape).round()
            # 框选出检测结果
            for *xyxy, conf, cls in reversed(det):
                # 添加识别对象坐标
                tars.append([int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])])

    return tars

if __name__ == "__main__":
    from eventlet import wsgi
    import eventlet

    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 8001)), app)
