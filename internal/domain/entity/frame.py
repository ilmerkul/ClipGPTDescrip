import torch


class FrameFaiss(object):
    def __init__(self, id: int, embedding: torch.Tensor):
        self.id = id
        self.embedding = embedding
