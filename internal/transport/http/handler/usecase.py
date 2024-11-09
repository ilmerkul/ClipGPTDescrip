from internal.domain.service import ServiceUsecase
from internal.transport.http.entity import Video as Video_handler

from typing import Annotated
from fastapi import File


class HandlerUsecase(object):
    def __init__(self, usecase: ServiceUsecase):
        self.usecase = usecase

    def video_index(self, video: Annotated[bytes, File()], description: str):
        video_handler = Video_handler(id=0, data=video,
                                      description=description)
        self.usecase.video_index(video_handler)

    def video_request(self, q: str):
        return self.usecase.video_request(q)
