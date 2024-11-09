import clip
import torch


def encode_text(model, texts, device):
    texts = clip.tokenize(texts).to(device)

    with torch.no_grad():
        text_features = model.encode_text(texts)

    return text_features
