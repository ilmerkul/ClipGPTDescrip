from internal.domain.service import ServiceVideo


class HandlerVideo(object):
    def __init__(self, service: ServiceVideo):
        self.service = service
