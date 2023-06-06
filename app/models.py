from sqlalchemy import Column, Integer, Numeric, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

from .database import Base

class Products(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True, nullable=False)
    product_name = Column(String, nullable=False)
    product_price = Column(Numeric, nullable=False)
    product_quantity = Column(Integer, nullable=False)
    product_created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id_fk = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    user = relationship('Users')

class Users(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, nullable=False)
    user_name = Column(String, nullable=False)
    user_email = Column(String, nullable=False, unique=True)
    user_password = Column(String, nullable=False)
    user_created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Customers(Base):
    __tablename__ = 'customers'
    customer_id = Column(Integer, primary_key=True, nullable=False)
    customer_name = Column(String, nullable=False)
    customer_email = Column(String, nullable=False, unique=True)
    customer_created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id_fk = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    user = relationship('Users')

class Receipt(Base):
    __tablename__ = 'receipts'
    receipt_id = Column(Integer, primary_key=True, nullable=False)
    user_id_fk = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    user = relationship('Users')
    receipt_items = relationship('ReceiptItems', back_populates='receipt')
    @property
    def total(self):
        return sum(item.price * item.quantity for item in self.receipt_items)

class ReceiptItems(Base):
    __tablename__ = 'receipt_items'
    id = Column(Integer, primary_key=True, nullable=False)
    receipt_id_fk = Column(Integer, ForeignKey('receipts.receipt_id', ondelete='CASCADE'), nullable=False)
    product_id_fk = Column(Integer, ForeignKey('products.product_id', ondelete='CASCADE'), nullable=False)
    # customer_id_fk = Column(Integer, ForeignKey('customers.customer_id', ondelete='CASCADE'), nullable=False)
    product_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric, nullable=False)
    receipt = relationship('Receipt', back_populates='receipt_items')
    product = relationship('Products', lazy='joined')
    # customer = relationship('Customers', lazy='joined')
