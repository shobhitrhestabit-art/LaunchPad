"""
CLIP Embedder (Day 3 – Image RAG)

This module is responsible ONLY for:
- Loading the CLIP model
- Creating image embeddings
- Creating text embeddings (from OCR text)

No file I/O
No databases
Reusable everywhere
"""

from pathlib import Path
from typing import List

import torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor


class CLIPEmbedder:
    def __init__(self, model_name: str = "openai/clip-vit-base-patch32"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.model = CLIPModel.from_pretrained(model_name).to(self.device)
        self.processor = CLIPProcessor.from_pretrained(model_name)

        self.model.eval()

    def embed_image(self, image_path: Path) -> List[float]:
        """
        Generate embedding for a single image.
        """
        image = Image.open(image_path).convert("RGB")

        inputs = self.processor(
            images=image,
            return_tensors="pt"
        ).to(self.device)

        with torch.no_grad():
            features = self.model.get_image_features(**inputs)

        features = features / features.norm(p=2, dim=-1, keepdim=True)
        return features[0].cpu().tolist()

    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for text (OCR output).
        """
        if not text.strip():
            text = " "  # CLIP does not accept empty input

        inputs = self.processor(
            text=[text],
            return_tensors="pt",
            padding=True,
            truncation=True
        ).to(self.device)

        with torch.no_grad():
            features = self.model.get_text_features(**inputs)

        features = features / features.norm(p=2, dim=-1, keepdim=True)
        return features[0].cpu().tolist()
