from internal.app import App
from fastapi import FastAPI
from omegaconf import OmegaConf
from internal.transport.http.handler import HandlerUsecase
from internal.domain.service import ServiceUsecase, ServiceFrame, ServiceVideo
from internal.adapter.database.sql import AdapterVideo, AdapterFrame
from internal.storage.database.sql import new_db

if __name__ == '__main__':
    fast_api_app = FastAPI()
    config = OmegaConf.load("../../config/config.yaml")

    adapter_video = AdapterVideo(db=new_db(config.ConfigDSN))
    adapter_frame = AdapterFrame(db=new_db(config.ConfigDSN))

    service_video = ServiceVideo(adapter=adapter_video)
    service_frame = ServiceFrame(adapter=adapter_frame)

    usecase = ServiceUsecase(service_video=service_video,
                             service_frame=service_frame)

    handler_usecase = HandlerUsecase(usecase=usecase)

    app = App(app=fast_api_app, handler_usecase=handler_usecase)
    app.register_handlers()
