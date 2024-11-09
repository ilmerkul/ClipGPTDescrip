from sqlalchemy import Engine, select
from sqlalchemy.orm import Session
from internal.storage.database.entity import Video


class AdapterVideo(object):
    def __init__(self, db: Engine):
        self.db = db

    def create(self, video: Video):
        with Session(self.db) as session:
            session.add(video)
            session.commit()

    def get_by_id(self, id: int):
        with Session(self.db) as session:
            stmt = select(Video).where(Video.id.in_([id]))
            video: Video = session.scalar(stmt)
        return video

    def delete(self, id: int):
        with Session(self.db) as session:
            video: Video = session.get(Video, id)
            session.delete(video)
            session.commit()
