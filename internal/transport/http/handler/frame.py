from internal.domain.service import ServiceFrame


class HandlerFrame(object):
    def __init__(self, service: ServiceFrame):
        self.service = service
