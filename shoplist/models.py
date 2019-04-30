# -*- coding: utf-8 -*-
from datetime import datetime
from shoplist import db


# Storage——商品库存，包含ID、商品名、商品数量、商品价格
class Storage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goods_name = db.Column(db.String(50))
    goods_num = db.Column(db.Integer)
    goods_price = db.Column(db.Integer)


# Cart——购物车应该包含ID、已购商品ID（外键）、已购商品数量、购买用户
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goods_id = db.Column(db.Integer,db.ForeignKey('storage.id'))
    goods_info = db.relationship('Storage')
    bought_num = db.Column(db.Integer)
    customer_id = db.Column(db.Integer)


# GoodsOrder——订单貨物詳情应该包含订单ID、商品ID、已购商品数量及价格
class GoodsOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    goods_name = db.Column(db.String(80))
    bought_num = db.Column(db.Integer)
    goods_price = db.Column(db.Integer)


# Order——订单，包含ID、顾客ID、订单时间
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer)
    order_time = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    order_info = db.relationship('GoodsOrder')

if __name__ == '__main__':
    db.drop_all()
    db.create_all()