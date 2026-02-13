import socketio
import time
import base64

# 图片文件路径
image_path = 'plantain (1).JPG'

# 将图片转换为base64字符串
with open(image_path, 'rb') as image_file:
    #encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    encoded_string = image_file.read()

# 创建Socket.IO客户端
sio = socketio.Client()

@sio.event
def connect():
    print("Connected to server")

@sio.event
def disconnect():
    print("Disconnected from server")

@sio.event
def connect_error(data):
    print("Failed to connect to server")

@sio.event
def inference_result(data):
    # 记录结束时间
    end_time2 = time.time()
    # 计算执行时间（以毫秒为单位）
    execution_time_ms2 = (end_time2 - start_time) * 1000
    print('2')
    print(f"ALL Time Consuming: {execution_time_ms2:.2f} ms")
    print("Received coords_list from server:", data)

@sio.event
def net_delay(data):
    # 记录结束时间
    end_time1 = time.time()
    # 计算执行时间（以毫秒为单位）
    execution_time_ms1 = (end_time1 - start_time) * 1000
    print('3')
    print(f"Net Delay Time Consuming: {execution_time_ms1:.2f} ms")


sio.connect('http://192.168.31.118:8001')

time.sleep(5)
# 记录开始时间
start_time = time.time()
print('1')
sio.emit('frame', encoded_string)

sio.wait()








