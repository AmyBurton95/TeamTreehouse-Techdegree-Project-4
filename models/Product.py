from sqlalchemy import Column, Integer, String
from . import Base


class Product(Base):
    __tablename__ = "product"

    product_id = Column(Integer, primary_key=True)
    product_name = Column("Product Name", String)
    product_price = Column("Price", Integer)
    product_quantity = Column("Quantity", Integer)
    date_updated = Column("Date Updated", Integer)

    def __repr__(self):
        return f'''Product Name: {self.product_name}, "Quantity: {self.product_quantity}, 
        Price: {self.product_price}, Date Updated: {self.date_updated}'''
