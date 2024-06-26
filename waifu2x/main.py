import os
from pathlib import Path
from PIL import Image
import torch
import numpy as np
import torchvision.transforms.functional as F

from modules import devices

from .yu45020.utils.prepare_images import ImageSplitter
from .yu45020.Models import UpConv_7

FILE_PATH = str(Path(__file__).parent.absolute())

def tensorToPil(img):
    normalized_out = img.squeeze(0).permute(1, 2, 0) * 255
    numpy_image = np.clip(normalized_out.numpy(), 0, 255).astype(np.uint8)
    return Image.fromarray(numpy_image)


def processImageWithSplitter(model, img: Image.Image):
    img = img.convert('RGB')
    # overlapping split
    # if input image is too large, then split it into overlapped patches
    # details can be found at [here](https://github.com/nagadomi/waifu2x/issues/238)
    img_splitter = ImageSplitter(seg_size=64, scale_factor=2, boarder_pad_size=3)
    img_patches = img_splitter.split_img_tensor(img, scale_method=None, img_pad=0)
    with torch.no_grad():
        out = []
        for i in img_patches:
            i = i.to(devices.device)
            out.append(model(i))
    img_upscale = img_splitter.merge_img_tensor(out)
    return tensorToPil(img_upscale)


def getModel(noise: int, style: str):
    if style == 'Photo':
        style = 'photo'
    else:
        style = 'anime'

    fileName = f'noise{noise}_scale2.0x_model.json'

    model = UpConv_7()
    modelDir = os.path.join(FILE_PATH, 'yu45020', 'model_check_points', 'Upconv_7')
    weightsPath = os.path.join(modelDir, style, fileName)
    model.load_pre_train_weights(weightsPath)
    model = model.to(devices.device)
    return model


