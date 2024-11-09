import torch


def encode_image(model, preprocess, images, device):
    images = preprocess(images).unsqueeze(0).to(device)

    with torch.no_grad():
        image_features = model.encode_image(images).squeeze()

    return image_features
