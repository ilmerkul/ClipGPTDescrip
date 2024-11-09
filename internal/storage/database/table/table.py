from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import ForeignKey

metadata_obj = MetaData()

video_table = Table(
    "video",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("hash", String(32), nullable=False),
    Column("description", String),
)

frame_table = Table(
    "frame",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("video_id", ForeignKey("video.id"), nullable=False),
    Column("hash", String(64), nullable=False),
)
