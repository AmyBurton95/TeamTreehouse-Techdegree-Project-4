from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship


engine = create_engine("sqlite:///inventory.db", echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Brands(Base):
    __tablename__ = "brand"

    id = Column(Integer, primary_key=True)
    brand_name = Column("Brand Name", String)
    logs = relationship("Product", back_populates="brand",
                        cascade="all, delete, delete-orphan")

    def __repr__(self):
        return f"Brand Name: {self.brand_name}"


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    product_name = Column("Product Name", String)
    product_price = Column("Price", Integer)
    product_quantity = Column("Quantity", Integer)
    date_updated = Column("Date Updated", Integer)
    brand_id = Column(Integer, ForeignKey("brand.id"))
    brand = relationship("Brands", back_populates="logs")

    def __repr__(self):
        return f'''Product Name: {self.product_name}, "Quantity: {self.product_quantity}, 
        Price: {self.product_price}, Date Updated: {self.date_updated}, Brand ID: {self.brand_id}'''

