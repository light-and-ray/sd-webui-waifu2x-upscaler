# Waifu2x upscaler for A1111 sd_webui

Waifu2x is an open-source NN upscaler from 2015. You can install it for nostalgia purpose, or if you need fast NN upscaler. Similar to "preserve details 2.0" in photoshop. But nevertheless new gen upscalers are a way better and faster, e.g. [4x-Nomos8k-span-otf-medium](https://openmodeldb.info/models/4x-Nomos8k-span-otf-medium) - 10 times faster then Waifu in 4x, and quality is comparable to DAT in many cases

![](/images/preview.png)
![](/images/upscalers.png)

`Waifu2x+ model CarnV2` is a tuned and modified model with extra features. Has 4 times more parameters 2,149,607 vs 552,480

<details>
<summary>Alternative UI</summary>

You can enable Waifu2x accordion in the settings if you want. Disabled by default

![](/images/accordion.png)

</details>

Resources:
- PyTorch implementation, which is in the base of this extension: https://github.com/yu45020/Waifu2x
- Original project: https://github.com/nagadomi/waifu2x
