
from datetime import datetime
from sqlmodel import SQLModel, Field, Column, JSON
import sqlalchemy.dialects.postgresql as pg

class AnalyzedString(SQLModel, table=True):
    __tablename__ = "analyzed_strings"

    id: str = Field(
        sa_column=Column(pg.TEXT, primary_key=True, nullable=False)  # SHA-256 hash as ID
    )
    value: str
    properties: dict = Field(sa_column=Column(JSON, nullable=False))
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.utcnow)
    )
    def __repr__(self):
        return f"<AnalyzedString id={self.id!r}, value={self.value!r}>"
