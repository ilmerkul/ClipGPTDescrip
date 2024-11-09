from internal.adapter.database.sql import AdapterVideo
from internal.transport.http.entity import Video as Video_handler, \
    Frame as Frame_handler
from internal.storage.database.entity import Video as Video_adapter
from internal.storage.database.entity import Frame as Frame_adapter

from typing import Sequence


class ServiceVideo(object):
    def __init__(self, adapter: AdapterVideo):
        self.adapter = adapter

    def create(self, video: Video_handler, frames: Sequence[Frame_handler]):
        frames_adapter = []
        for frame in frames:
            # TODO send data to S3 and get hash
            frame_hash = "hnb135rt7y3r13"
            frame_adapter = Frame_adapter(hash=frame_hash)
            frames_adapter.append(frame_adapter)
        # TODO send data to S3 and get hash
        video_hash = "hnb135rt7y3r13"
        video_adapter: Video_adapter = Video_adapter(id=video.id,
                                                     hash=video_hash,
                                                     description=video.description,
                                                     frames=frames_adapter)
        self.adapter.create(video_adapter)

    def get_by_id(self, id: int) -> Video_handler:
        video_adapter = self.adapter.get_by_id(id)
        # TODO get video data from S3
        data = bytearray()
        video_handler = Video_handler(id=video_adapter.id, data=data,
                                      description=video_adapter.description)
        return video_handler
