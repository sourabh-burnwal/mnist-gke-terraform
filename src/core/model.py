import cv2
import torch
from torchvision import transforms


class Classification:
    def __init__(self):
        self.ort_session = None
        self.model = None
        # self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.device="cpu"
        print("Using: ", self.device)

        # Define a transform to normalize the data
        self.transform = transforms.Compose([transforms.ToTensor(),
                                             transforms.Normalize((0.5,), (0.5,)),
                                             ])

    def load_pt_model(self, model_path):
        self.model = torch.load(model_path, map_location=self.device)

    def pre_process(self, img_path):
        image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        image = cv2.resize(image, (28, 28))
        # print("Image size", image.shape)
        image_tensor = self.transform(image)
        # print(image_tensor.shape)
        image_tensor = image_tensor.view(1, 784)
        print(type(image_tensor), image_tensor.shape)
        return image_tensor

    def predict(self, image_path: str):
        image_tensor = self.pre_process(image_path)
        out = self.model(image_tensor.cuda())
        # print(out)
        ps = torch.exp(out)
        probab = list(ps.detach().cpu().numpy()[0])
        pred_label = probab.index(max(probab))
        # print(pred_label)
        return pred_label
