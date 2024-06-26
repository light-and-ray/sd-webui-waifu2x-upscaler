import gradio as gr
from modules import scripts_postprocessing, shared, script_callbacks
import copy
from waifu2x.main import getModel, processImageWithSplitter, getCarnV2Model

if hasattr(scripts_postprocessing.ScriptPostprocessing, 'process_firstpass'):  # webui >= 1.7
    from modules.ui_components import InputAccordion
else:
    InputAccordion = None


class Waifu2xExtras(scripts_postprocessing.ScriptPostprocessing):
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
            scale = gr.Radio(value='4x', choices=["2x", "4x", "8x", "16x"],
                        label="Scale", type="index")
            style = gr.Radio(value="Anime", choices=["Anime", "Photo", "CarnV2"], label="Style")

        style.change(fn=lambda x: gr.update(visible=(x!="CarnV2")),
            inputs=[style], outputs=[noise], show_progress=False)

        args = {
            'enable': enable,
            'noise' : noise,
            'scale' : scale,
            'style' : style,
        }
        return args

    def process_firstpass(self, pp: scripts_postprocessing.PostprocessedImage, **args):
        pp.shared.target_width = pp.image.width * 2 ** (args['scale'] + 1)
        pp.shared.target_height = pp.image.height * 2 ** (args['scale'] + 1)

    def process(self, pp: scripts_postprocessing.PostprocessedImage, **args):
        if args['enable'] == False:
            return

        if args['style'] == "CarnV2":
            model = getCarnV2Model()
        else:
            model = getModel(args['noise'], args['style'])
        for _ in range(args['scale'] + 1):
            pp.image = processImageWithSplitter(model, pp.image)
            if shared.state.interrupted: break

        info = copy.copy(args)
        del info['enable']
        info['noise'] = ["None", "Low", "Medium", "High"][info['noise']]
        info['scale'] = ["2x", "4x", "8x", "16x"][info['scale']]
        if args['style'] == "CarnV2":
            del info['noise']
        pp.info[self.name] = str(info)


def on_ui_settings():
    shared.opts.add_option(
        "show_waifu2x_accordion",
        shared.OptionInfo(
            False,
            "Show Waifu2x accordion in extras tab",
            gr.Checkbox,
            section=('upscaling', "Upscaling")
        ).needs_reload_ui()
    )

script_callbacks.on_ui_settings(on_ui_settings)

if not shared.opts.data.get('show_waifu2x_accordion', False):
    del Waifu2xExtras

