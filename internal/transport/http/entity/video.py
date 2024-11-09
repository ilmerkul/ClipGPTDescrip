class Video(object):
    def __init__(self, id: int, data: bytes, description: str):
        self.id = id
        self.data = data
        self.description = description
