from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from internal.transport.http.handler import HandlerUsecase

from typing import Annotated
from fastapi import File


class App(object):
    def __init__(self, app: FastAPI, handler_usecase: HandlerUsecase):
        self.app = app
        self.handler_usecase = handler_usecase

    def register_handlers(self):
        app = self.app

        @app.get("/")
        async def main():
            content = """
            <body>
            <form action="/index_video/" enctype="multipart/form-data" method="post">
            <input name="file" type="file">
            <input type="submit">
            </form>
            </body>
            """
            return HTMLResponse(content=content)

        @app.get("/video/index")
        def video_index(video: Annotated[bytes, File()], description: str):
            self.handler_usecase.video_index(video, description)

        @app.get("/video/request")
        def video_request(q: str):
            return self.handler_usecase.usecase.video_request(q)
