from modules import modelloader, devices, errors
from modules.shared import opts
from modules.upscaler import Upscaler, UpscalerData
from modules.upscaler_utils import upscale_with_model

from waifu2x.main import processImageWithSplitter, getModel

class Waifu2xFields():
    def __init__(self, style: str, noise: int):
        self.style = style
        self.noise = noise


    def getName(self):
        noiseStr = ''
        if self.noise == 0:
            noiseStr = 'none'
        elif self.noise == 1:
            noiseStr = 'low'
        elif self.noise == 2:
            noiseStr = 'medium'
        elif self.noise == 3:
            noiseStr = 'hight'

        return f'Waifu2x {self.style.lower()} denoise {noiseStr}'


data = [
    Waifu2xFields('Anime', 0),
    Waifu2xFields('Anime', 1),
    Waifu2xFields('Anime', 2),
    Waifu2xFields('Anime', 3),
    Waifu2xFields('Photo', 0),
    Waifu2xFields('Photo', 1),
    Waifu2xFields('Photo', 2),
    Waifu2xFields('Photo', 3),
]

class BaseClass(Upscaler):
    def __init__(self, dirname, waifu2xFields: Waifu2xFields = None):
        if waifu2xFields is None:
            self.scalers = []
            return
        self.waifu2xFields = waifu2xFields
        self.name = "Waifu2x"
        self.scalers = [UpscalerData(self.waifu2xFields.getName(), None, self, 2)]
        super().__init__()

    def do_upscale(self, img, selected_model):
        model = getModel(self.waifu2xFields.noise, self.waifu2xFields.style)
        return processImageWithSplitter(model, img)


class Class0(BaseClass, Upscaler):
    def __init__(self, dirname):
        super().__init__(dirname, data[0])
class Class1(BaseClass, Upscaler):
    def __init__(self, dirname):
        super().__init__(dirname, data[1])
class Class2(BaseClass, Upscaler):
    def __init__(self, dirname):
        super().__init__(dirname, data[2])
class Class3(BaseClass, Upscaler):
    def __init__(self, dirname):
        super().__init__(dirname, data[3])
class Class4(BaseClass, Upscaler):
    def __init__(self, dirname):
        super().__init__(dirname, data[4])
class Class5(BaseClass, Upscaler):
    def __init__(self, dirname):
        super().__init__(dirname, data[5])
class Class6(BaseClass, Upscaler):
    def __init__(self, dirname):
        super().__init__(dirname, data[6])
class Class7(BaseClass, Upscaler):
    def __init__(self, dirname):
        super().__init__(dirname, data[7])