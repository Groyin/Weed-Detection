import requests
import time


url = 'http://192.168.31.118:5000/upload'
file_path = 'plantain (1).JPG'  # Replace with your image path


with open(file_path, 'rb') as img:
    files = {'file': img.read()}
    # 记录开始时间
    start_time = time.time()
    response = requests.post(url, files=files)

if response.status_code == 200:
    # 记录结束时间
    end_time1 = time.time()
    # 计算执行时间（以毫秒为单位）
    execution_time_ms1 = (end_time1 - start_time) * 1000
    print(f"Net Delay Time Consuming: {execution_time_ms1:.2f} ms")
    print('Server Response:', response.json())
else:
    print('Failed to upload image')
