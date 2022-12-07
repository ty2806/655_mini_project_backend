import torch
from torchvision import transforms
from PIL import Image

class Classifier():
    def __init__(self):
        # load a reset-18 model from torch.hub
        self.model = torch.hub.load('pytorch/vision:v0.10.0', 'resnet18', pretrained=True)
        self.model.eval()

    # read an image from a file and run the cnn model, return the top1 classification result
    def classify(self, filename):
        # read image
        input_image = Image.open(filename)

        # setup preprocess on input images
        preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        input_tensor = preprocess(input_image)
        input_batch = input_tensor.unsqueeze(0)

        # run the cnn model
        with torch.no_grad():
            output = self.model(input_batch)

        # take softmax to output tensor
        probabilities = torch.nn.functional.softmax(output[0], dim=0)
        
        # read imagenet label names
        with open("imagenet_classes.txt", "r") as f:
            categories = [s.strip() for s in f.readlines()]

        # get top5 results from output tensor
        top5_prob, top5_catid = torch.topk(probabilities, 5)
        top5 = []
        for i in range(top5_prob.size(0)):
            top5.append([categories[top5_catid[i]], top5_prob[i].item()])
        
        print(top5)
        return top5[0][0]
