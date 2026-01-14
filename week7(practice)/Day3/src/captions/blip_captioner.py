"""
BLIP Caption Generator
Generates a natural language description of an image.
"""

from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration


class BlipCaptioner:
    def __init__(self, model_name: str = "Salesforce/blip-image-captioning-base"):
        self.processor = BlipProcessor.from_pretrained(model_name)
        self.model = BlipForConditionalGeneration.from_pretrained(model_name)

    def generate_caption(self, image_path: str) -> str:
        image = Image.open(image_path).convert("RGB")

        inputs = self.processor(image, return_tensors="pt")
        output = self.model.generate(**inputs, max_length=50)

        caption = self.processor.decode(output[0], skip_special_tokens=True)
        return caption
