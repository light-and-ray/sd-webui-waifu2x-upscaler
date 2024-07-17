import os
from pathlib import Path
from PIL import Image
import torch
import torch.nn as nn
import numpy as np
from modules import devices, shared
from tqdm import tqdm

from .yu45020.utils.prepare_images import ImageSplitter
from .yu45020.Models import UpConv_7, CARN_V2, network_to_half


FILE_PATH = str(Path(__file__).parent.absolute())

def tensorToPil(img):
    normalized_out = img.squeeze(0).permute(1, 2, 0) * 255
    numpy_image = np.clip(normalized_out.numpy(), 0, 255).astype(np.uint8)
    result = Image.fromarray(numpy_image)
    del normalized_out, numpy_image
    return result


def processImageWithSplitter(model, img: Image.Image):
    img = img.convert('RGB')
    # overlapping split
    # if input image is too large, then split it into overlapped patches
    # details can be found at [here](https://github.com/nagadomi/waifu2x/issues/238)
    img_splitter = ImageSplitter(seg_size=64, scale_factor=2, boarder_pad_size=3)
    img_patches = img_splitter.split_img_tensor(img, scale_method=None, img_pad=0)
    with torch.no_grad():
        out = []
        for i in tqdm(img_patches):
            if shared.state.interrupted: return img
            i = i.to(devices.device)
            out.append(model(i))
            del i
    img_upscale = img_splitter.merge_img_tensor(out)
    result = tensorToPil(img_upscale)
    del img_upscale, out
    return result



_models_cache = {}

def getModel(noise: int, style: str):
    global _models_cache
    fileName = os.path.join(style.lower(), f'noise{noise}_scale2.0x_model.json')

    if fileName not in _models_cache:
        model = UpConv_7()
        modelDir = os.path.join(FILE_PATH, 'yu45020', 'model_check_points', 'Upconv_7')
        weightsPath = os.path.join(modelDir, fileName)
        model.load_pre_train_weights(weightsPath)
        model = model.to(devices.device)
        _models_cache[fileName] = model

    return _models_cache[fileName]



_model_carnV2 = None

def getCarnV2Model():
    global _model_carnV2
    if _model_carnV2 is None:
        model = CARN_V2(color_channels=3, mid_channels=64, conv=nn.Conv2d,
                                single_conv_size=3, single_conv_group=1,
                                scale=2, activation=nn.LeakyReLU(0.1),
                                SEBlock=True, repeat_blocks=3, atrous=(1, 1, 1))

        model = network_to_half(model)
        modelDir = os.path.join(FILE_PATH, 'yu45020', 'model_check_points', 'CARN_V2')
        weightsPath = os.path.join(modelDir, 'CARN_model_checkpoint.pt')
        model.load_state_dict(torch.load(weightsPath, map_location='cpu'))
        model = model.to(devices.device)
        _model_carnV2 = model

    return _model_carnV2


