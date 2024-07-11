from sqlalchemy import Column, Integer, String
from . import Base

class Brands(Base):
    __tablename__ = "brands"

    brand_id = Column(Integer, primary_key=True)
    brand_name = Column("Brand Name", String)

    def __repr__(self):
        return f"Brand Name: {self.brand_name}"
