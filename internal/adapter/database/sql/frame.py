from sqlalchemy import Engine, select
from sqlalchemy.orm import Session
from internal.storage.database.entity import Frame

from typing import List, Sequence


class AdapterFrame(object):
    def __init__(self, db: Engine):
        self.db = db

    def create_multiple(self, frames: List[Frame]):
        with Session(self.db) as session:
            session.add_all(frames)
            session.commit()

    def get_by_ids(self, ids: List[int]) -> Sequence[Frame]:
        with Session(self.db) as session:
            stmt = select(Frame).where(Frame.id.in_(ids))
            frames = session.scalars(stmt).all()
        return frames

    def get_all(self) -> Sequence[Frame]:
        with Session(self.db) as session:
            stmt = select(Frame)
            frames = session.scalars(stmt).all()
        return frames

    def delete(self, id: int):
        with Session(self.db) as session:
            frame: Frame = session.get(Frame, id)
            session.delete(frame)
            session.commit()
