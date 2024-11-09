from .video import ServiceVideo
from .frame import ServiceFrame
import torch

from src.keyframe import KFPropose, KFCluster
from src.encode import encode_image, encode_text
import faiss
import clip
import numpy as np
from PIL import Image
import os

from internal.transport.http.entity import Video as Video_handler

size_embedding = 512
k = 4
device = "cuda" if torch.cuda.is_available() else "cpu"


class ServiceUsecase(object):
    def __init__(self, service_video: ServiceVideo,
                 service_frame: ServiceFrame):
        self.service_video = service_video
        self.service_frame = service_frame
        self.kf_propose = KFPropose()
        self.kf_cluster = KFCluster()
        self.index = faiss.IndexFlatIP(size_embedding)
        self.model, self.preprocess = clip.load("ViT-B/32", device=device)

    def get_frame_embedding(self, frames: list[np.ndarray]):
        images = []
        for frame in frames:
            image = np.uint8(frame)
            images.append(Image.fromarray(image))

        frames_embedding = []
        for image in images:
            frames_embedding.append(
                encode_image(self.model, self.preprocess, image, device))

        return frames_embedding

    def video_index(self, video: Video_handler):
        path = "C:\\Users\\pynex\\Projects\\github\\ClipGPTDescrip"
        video_path = os.path.join(path, 'data\\video\\binary.mp4')
        frame_path = os.path.join(path, 'data\\frame')
        with open(video_path, 'wb') as wfile:
            wfile.write(video.data)

        frames = self.kf_propose.propose_frames(video_path)

        frames = self.kf_cluster.select_best_frames(frames)

        self.kf_propose.save_frames(frames, frame_path)

        frames_embedding = self.get_frame_embedding(frames)

        frames_embedding = torch.stack(frames_embedding, dim=0)

        self.index.add(frames_embedding)

    def video_request(self, q: str):
        request_embedding = encode_text(self.model, [q], device)

        D, I = self.index.search(request_embedding, k)

        return {"D": D.tolist(), "I": I.tolist()}
