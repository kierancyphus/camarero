import logging
import torch
import torch.nn.functional as F
import io
from PIL import Image
from torchvision import transforms
from ts.torch_handler.base_handler import BaseHandler
import pickle


class CustomHandler(BaseHandler):
    """
    Custom handler for pytorch serve. This handler supports batch requests.
    For a deep description of all method check out the doc:
    https://pytorch.org/serve/custom_service.html
    """

    def __init__(self, *args, **kwargs):
        super().__init__()
        # TODO: update transform
        self.transform = transforms.Compose([
            transforms.Grayscale(),
            transforms.Resize(size=(64, 64)),
            transforms.toTensor()
        ])

    def preprocess_one_image(self, req):
        """
        Process one single image.
        """
        # get image from the request
        image = req.get("data")
        if image is None:
            image = req.get("body")
            # create a stream from the encoded image

        # These should already been in a 3d shape
        image = pickle.loads(image)
        image = self.transform(image)
        # add batch dim
        image = image.unsqueeze(0)
        return image

    def preprocess(self, requests):
        """
        Process all the images from the requests and batch them in a Tensor.
        """

        images = [self.preprocess_one_image(req) for req in requests]
        images = torch.cat(images)
        return images

    def inference(self, x):
        """
        Given the data from .preprocess, perform inference using the model.
        We return the predicted label for each image.
        """
        outs = self.model.forward(x)
        probs = F.softmax(outs, dim=1)
        preds = torch.argmax(probs, dim=1)
        return preds

    def postprocess(self, preds):
        """
        Given the data from .inference, postprocess the output.
        In our case, we get the human readable label from the mapping
        file and return a json. Keep in mind that the reply must always
        be an array since we are returning a batch of responses.
        """
        res = []
        # pres has size [BATCH_SIZE, 1]
        # convert it to list
        preds = preds.cpu().tolist()
        for pred in preds:
            label = self.mapping[str(pred)]
            res.append({'label': label, 'index': pred})
        return res
