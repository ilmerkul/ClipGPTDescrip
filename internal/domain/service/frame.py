from internal.adapter.database.sql.frame import AdapterFrame
from internal.storage.database.entity import Frame as Frame_adapter
from internal.transport.http.entity import Frame as Frame_handler
from internal.domain.entity import FrameFaiss
import torch
from faiss import Index

from typing import List


class ServiceFrame(object):
    def __init__(self, adapter: AdapterFrame):
        self.adapter = adapter

    def create_multiple(self, frames: List[Frame_handler]):
        frames_adapter = []
        for frame in frames:
            # TODO send data to S3 and get hash
            frame_hash = "hnb135rt7y3r13"
            frame_adapter = Frame_adapter(hash=frame_hash)
            frames_adapter.append(frame_adapter)
        self.adapter.create_multiple(frames_adapter)

    def get_by_ids(self, ids: List[int]) -> List[Frame_handler]:
        frames_adapter = self.adapter.get_by_ids(ids)
        frames_handler = []
        for frame in frames_adapter:
            # TODO request to S3
            frame_handler = Frame_handler(id=frame.id, data=bytearray([1, 0]))
            frames_handler.append(frame_handler)

        return frames_handler

    def get_all_faiss(self, faiss_index: Index):
        frames_adapter = self.adapter.get_all()
        frames_faiss = []
        for frame in frames_adapter:
            # TODO request to S3
            # TODO get embedding
            frame_faiss = FrameFaiss(id=frame.id, embedding=torch.tensor([]))
            frames_faiss.append(frame_faiss)

        frames_faiss.sort(key=lambda x: x.id)
        faiss_index.add(list(map(lambda x: x.embedding, frames_faiss)))
