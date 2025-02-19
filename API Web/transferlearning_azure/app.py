import base64
import io
import json

from torchvision import models
import torchvision.transforms as transforms
from PIL import Image
from flask import Flask, jsonify, request

# import Testing
import Testing

app = Flask(__name__)
imagenet_class_index = json.load(open('imagenet_class_index.json'))
model = models.densenet121(pretrained=True)
model.eval()


def transform_image(image_bytes):
    my_transforms = transforms.Compose([transforms.Resize(255),
                                        transforms.CenterCrop(224),
                                        transforms.ToTensor(),
                                        transforms.Normalize(
                                            [0.485, 0.456, 0.406],
                                            [0.229, 0.224, 0.225])])
    image = Image.open(io.BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)


def get_prediction(image_bytes):
    tensor = transform_image(image_bytes=image_bytes)
    outputs = model.forward(tensor)
    _, y_hat = outputs.max(1)
    predicted_idx = str(y_hat.item())
    return imagenet_class_index[predicted_idx]


@app.route('/home', methods=['GET'])
def home():
    return jsonify({'test':"test"})

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        print("vaof day")


        # file = request.form.get('file')
        # image_string = base64.b64decode(file)
        # print(image_string)
        # tensor = transforms.ToTensor()(Image.open(io.BytesIO(image_string)))
        # class_result = Testing.predictByImage(tensor)


        # print(len(img_bytes))

        # class_id, class_name = get_prediction(image_bytes=img_bytes)
        # tensor = transform_image(image_bytes=img_bytes)

        file = request.files['file']
        img_bytes = file.read()
        tensor = transforms.ToTensor()(Image.open(io.BytesIO(img_bytes)))
        class_result = Testing.predictByImage(tensor)
        return jsonify({'class_name': class_result})


if __name__ == '__main__':
    app.run()
