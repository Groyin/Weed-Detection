from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from PIL import Image
import io

app = Flask(__name__)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # 打印所有请求头
        for header, value in request.headers.items():
            print(f'{header}: {value}')
        if 'file' not in request.files:
            return "No file part", 400
        file = request.files['file']
        if file.filename == '':
            return "No selected file", 400
        if file:
            # Convert the uploaded file to a PIL image
            images = file
            # Process the file here if needed
            response_data = [[1, 2, 3, 9], [7, 0, 0, 4]]
            return jsonify(response_data)
    return ''' '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000 , debug=True)
