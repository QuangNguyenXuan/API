import base64
from flask import Flask, jsonify, request
import torchvision.transforms as transforms
from PIL import Image
import machine_learning_module
import io

app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # file = request.files['file']
        # img_bytes = file.read()
        # tensor = transforms.ToTensor()(Image.open(io.BytesIO(img_bytes)))
        # class_result = machine_learning_module.predict_by_image(tensor)

        file = request.form.get('file')
        image_string = base64.b64decode(file)
        print("data received from mobile:***********************\n", image_string)
        tensor = transforms.ToTensor()(Image.open(io.BytesIO(image_string)))
        class_result = machine_learning_module.predict_by_image(tensor)

        return jsonify({'class_name': class_result})


if __name__ == '__main__':
    app.run()
