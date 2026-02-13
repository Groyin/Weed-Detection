import requests
import time
import cv2

url = 'http://192.168.31.118:5000/upload'
video_path = 'cscs.mp4'

# 打开视频文件
cap = cv2.VideoCapture(video_path) # 参数0表示默认摄像头
'''
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()
'''

frame_count = 0
while True:
    # 记录开始时间
    start_time = time.time()
    # 逐帧读取视频
    ret, frame = cap.read()

    # 如果读取帧失败，退出循环
    if not ret:
        break

    # 将帧编码为JPEG格式
    _, img_encoded = cv2.imencode('.jpg', frame)

    # 将JPEG图像转换为字节数据
    img_bytes = img_encoded.tobytes()

    # 将图片字节数据发送POST请求
    files = {'file': img_bytes}
    data = {'device': 0 ,'frame': frame_count}
    response = requests.post(url, files=files,data=data)

    if response.status_code == 200:
        # 记录结束时间
        end_time1 = time.time()
        # 计算执行时间（以毫秒为单位）
        execution_time_ms1 = (end_time1 - start_time) * 1000
        post_result=response.json()
        inference_result=post_result['result']
        print(f"ALL Delay Time Consuming: {execution_time_ms1:.2f} ms")
        print(f"Frame {frame_count} uploaded successfully.")
        print('Inference Result:', inference_result)
    else:
        print(f"Error uploading frame {frame_count}. Status code: {response.status_code}")



    frame_count += 1

# 释放视频对象
cap.release()
print("Video processing complete.")