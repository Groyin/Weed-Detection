import cv2
import socketio
import base64

# 打开摄像头
cap = cv2.VideoCapture(0)  # 参数0表示默认摄像头

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

sio = socketio.Client()

@sio.event
def connect():
    print("Connected to Socket.IO server")

@sio.event
def disconnect():
    print("Disconnected from Socket.IO server")

@sio.event
def inference_result(data):
    print(f"Inference result: {data}")
    # 这里的data已经是Python对象（坐标列表）
    coords = data
    print(f"Coordinates: {coords}")

#sio.connect('http://<edge-device-ip>:8080')
sio.connect('http://localhost:8080')
sio.wait()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    _, buffer = cv2.imencode('.jpg', frame)
    jpeg_data = base64.b64encode(buffer).decode('utf-8')

    sio.emit('frame', jpeg_data)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
sio.disconnect()
