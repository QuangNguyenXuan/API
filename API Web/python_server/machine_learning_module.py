import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms

classes = ["Ants", "Bees"];


class CustomModel(torch.nn.Module):
    def __init__(self, model_path=None):
        super().__init__()

        # Building the model
        self.model = torchvision.models.resnet18(weights='IMAGENET1K_V1')
        for param in self.model.parameters():
            param.requires_grad = False

        num_ftrs = self.model.fc.in_features
        self.model.fc = nn.Linear(num_ftrs, 2)

        weights = torch.load(model_path, map_location=torch.device('cpu'))
        self.model.load_state_dict(weights)
        self.model.to('cpu')
        self.model.eval()

        # We need to make the transformations sequential
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


def predict_by_image(tensor):
    outputs = my_model.forward(tensor)
    _, y_hat = outputs.max(1)
    return classes[int(y_hat.item())]


my_model = CustomModel('my_pytorch_model.pt')
