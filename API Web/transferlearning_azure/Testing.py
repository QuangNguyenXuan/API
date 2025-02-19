import torch
import torch.nn as nn
import torchvision
from torchvision import transforms
import time
import os
from PIL import Image

# from app import transform_image

classes = ["Ants", "Bees"];
#Let's create our class with our customize forward method


class my_Model(torch.nn.Module):
    def __init__(self, model_path=None):
        super().__init__()

        #Building the model
        self.model = torchvision.models.resnet18(weights='IMAGENET1K_V1')
        for param in self.model.parameters():
            param.requires_grad = False

        num_ftrs = self.model.fc.in_features
        self.model.fc = nn.Linear(num_ftrs, 2)

        weights = torch.load(model_path, map_location=torch.device('cpu'))
        self.model.load_state_dict(weights)
        self.model.to('cpu')
        self.model.eval()

        #We need to make the transformations sequential
        self.transforms = torch.nn.Sequential(
            transforms.Resize([256], antialias=True),
            transforms.CenterCrop(224),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        )

    def forward(self, tensor):
        img = self.transforms(tensor)
        img = img.unsqueeze(0)
        img = img.to('cpu')
        return self.model(img)

my_model = my_Model('my_pytorch_model.pt')

def predictByImage(tensor):
    outputs = my_model.forward(tensor)
    _, y_hat = outputs.max(1)
    return classes[int(y_hat.item())]

# pil_img = Image.open("ants.jpg")
# tensor = transforms.ToTensor()(pil_img)
# tensor = transform_image(image_bytes=pil_img.tobytes())
# print(predictByImage())