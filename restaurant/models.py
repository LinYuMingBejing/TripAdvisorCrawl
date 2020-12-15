from sqlalchemy import Column, Float, Index, String, Text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class TripAdvisor(Base):
    __tablename__ = 'ta'
    __table_args__ = (
        Index('restaurant_unique', 'title', 'address', unique=True),
    )

    id = Column(INTEGER(10), primary_key=True)
    title = Column(String(256, 'utf8mb4_unicode_ci'), nullable=False)
    res_type = Column(String(256, 'utf8mb4_unicode_ci'), nullable=False)
    rating_count = Column(INTEGER(11))
    info_url = Column(Text)
    cellphone = Column(String(256, 'utf8mb4_unicode_ci'))
    address = Column(String(256, 'utf8mb4_unicode_ci'))
    street = Column(String(256, 'utf8mb4_unicode_ci'))
    city = Column(String(256, 'utf8mb4_unicode_ci'))
    area = Column(String(256, 'utf8mb4_unicode_ci'))
    rating = Column(Float(asdecimal=True))
    comment = Column(Text)
    open_time = Column(String(256, 'utf8mb4_unicode_ci'))