import os
import warnings
from typing import List
import torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor

os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "true"
warnings.filterwarnings("ignore")


class QueryEmbedder:
    def __init__(self, model_name: str = "openai/clip-vit-base-patch32"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.model = CLIPModel.from_pretrained(model_name).to(self.device)
        self.processor = CLIPProcessor.from_pretrained(
            model_name,
            use_fast=False
        )

        self.model.eval()

    def embed_text_query(self, query: str) -> List[float]:
        if not query or not query.strip():
            raise ValueError("Query text cannot be empty")

        inputs = self.processor(
            text=[query],
            return_tensors="pt",
            padding=True,
            truncation=True
        ).to(self.device)

        with torch.no_grad():
            features = self.model.get_text_features(**inputs)

        features = features / features.norm(p=2, dim=-1, keepdim=True)
        return features[0].cpu().tolist()

    def embed_image_query(self, image: Image.Image) -> List[float]:
        inputs = self.processor(
            images=image,
            return_tensors="pt"
        ).to(self.device)

        with torch.no_grad():
            features = self.model.get_image_features(**inputs)

        features = features / features.norm(p=2, dim=-1, keepdim=True)
        return features[0].cpu().tolist()
