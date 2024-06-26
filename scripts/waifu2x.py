import gradio as gr
from modules import scripts_postprocessing
import copy
from waifu2x.main import getModel, processImageWithSplitter

if hasattr(scripts_postprocessing.ScriptPostprocessing, 'process_firstpass'):  # webui >= 1.7
    from modules.ui_components import InputAccordion
else:
    InputAccordion = None


class ColorCorrectionExtras(scripts_postprocessing.ScriptPostprocessing):
    name = "Waifu2x Upscale"
    order = 1010

    def ui(self):
        global METHODS
        with (
            InputAccordion(False, label=self.name) if InputAccordion
            else gr.Accordion(self.name, open=False)
            as enable
        ):
            if not InputAccordion:
                enable = gr.Checkbox(False, label="Enable")
            noise = gr.Radio(value='Medium', choices=["None", "Low", "Medium", "High"],
                        label="Noise reduction", type="index")
            style = gr.Radio(value="Anime", choices=["Anime", "Photo"], label="Style")

        args = {
            'enable': enable,
            'noise' : noise,
            'style' : style
        }
        return args

    def process_firstpass(self, pp: scripts_postprocessing.PostprocessedImage, **args):
        pp.shared.target_width = pp.image.width * 2
        pp.shared.target_height = pp.image.height * 2

    def process(self, pp: scripts_postprocessing.PostprocessedImage, **args):
        if args['enable'] == False:
            return

        model = getModel(args['noise'], args['style'])
        pp.image = processImageWithSplitter(model, pp.image)

        info = copy.copy(args)
        del info['enable']
        pp.info[self.name] = str(info)

