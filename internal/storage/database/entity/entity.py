from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing import List
from .base import Base


class Video(Base):
    __tablename__ = "video"
    id: Mapped[int] = mapped_column(primary_key=True)
    hash: Mapped[str] = mapped_column(String(32))
    description: Mapped[str] = mapped_column(String(100))
    frames: Mapped[List["Frame"]] = relationship(back_populates="video")

    def __repr__(self):
        return f"Video(id={self.id!r}, hash={self.hash!r}, description={self.description[:10]!r}...)"


class Frame(Base):
    __tablename__ = "Frame"
    id: Mapped[int] = mapped_column(primary_key=True)
    hash: Mapped[str] = mapped_column(String(64))
    video_id: Mapped[int] = mapped_column(ForeignKey("video.id"))
    video: Mapped[Video] = relationship(back_populates="frames")

    def __repr__(self):
        return f"Frame(id={self.id!r}, hash={self.hash!r}, video_id={self.video_id!r})"
