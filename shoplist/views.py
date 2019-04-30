# -*- coding: utf-8 -*-
from datetime import datetime
from shoplist import app, db
from flask import request  # redirect, url_for,flash
from flask import jsonify, json
from flask import make_response
from sqlalchemy import and_

from shoplist.models import Storage, GoodsOrder, Cart, Order
from shoplist.utils import search_product


@app.route('/')
def index():
    return "hello"


# 查询商品信息 finish
# GET /product/query/<int:product_id>
# return {goods_id:{goods_name:,goods_num:,goods_price:}}
@app.route("/storage/<int:product_id>", methods=["GET"])
@app.route("/storage", methods=["GET"])
def product(product_id=None):
    if product_id is not None:
        goods = Storage.query.get(product_id)
        if goods is None:
            return jsonify({'status': 0})
    else:
        goods = Storage.query.all()
    goods_json = {}
    one_goods = {'goods_name': goods.goods_name, 'goods_num': goods.goods_num, 'goods_price': goods.goods_price}
    goods_json[str(goods.id)] = one_goods
    goods_json['status'] = 1
    return jsonify(goods_json)


# 按关键词查询货物
# POST /product/search {"search":[[{"key":,"op":,"value":}]]}
# return {goods_id:{goods_name:,goods_num:,goods_price:},}
@app.route("/product", methods=["POST"])
def search():
    if request.is_json:
        wanted_product = request.get_json()['search']
        storage_product = Storage.query.filter(search_product(wanted_product)).all()
        return_product = {}
        for i in storage_product:
            one_product = {'goods_name': i.goods_name, 'goods_num': i.goods_num, 'goods_price': i.goods_price}
            return_product[str(i.id)] = one_product
        resp = make_response(json.dumps(return_product))
        resp.headers["content-type"] = 'application/json;charset=utf-8'
        return resp
    else:
        return "wrong input,please enter a json query", 201


# 增加一类商品 finish
# POST {"goods_name":,"goods_num","goods_price"}
# return
# 如果商品项有缺失，返回状态值0及缺失项：{'status'：0，'error':}
# 如果商品成功上传，则返回状态值1及添加商品在库存中的id：{'status':1, 'goods_id':}
@app.route("/storage", methods=["POST"])
def create_product():
    try:
        new_product = request.get_json()
        new_goods = Storage(goods_name=new_product['goods_name'], goods_num=new_product['goods_num'],
                            goods_price=new_product['goods_price'])
        db.session.add(new_goods)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 0, 'error': str(e)}), 404
    return jsonify({'status': 1, 'goods_id': new_goods.id}), 200


# 更新商品信息(包括增加减少数量)
# PATCH /product/update/<int:product_id> {"add_num":10, "name":"iphone"}/{"minus_num":10, "name":"iphone"}
#
@app.route("/storage/<int:product_id>", methods=["PATCH"])
def updateproduct(product_id):
    # {"add_num":10, "name":"iphone"}
    if request.is_json:
        update_product = request.get_json()
        goods_in_storage = Storage.query.get(product_id)
        if goods_in_storage is not None:
            if "add_num" in update_product:
                goods_in_storage.goods_num += update_product['add_num']
            elif "minus_num" in update_product:
                goods_in_storage.goods_num += update_product['minus_num']
            else:
                return jsonify({'status': 0})
            # goods_in_storage['add_num'] += update_product['add_num']
            db.session.commit()
            return jsonify({'status': 1})
        else:
            return jsonify({'status': 0})


# 移除一类商品
@app.route("/storage/<int:product_id>", methods=["DELETE"])
def remove_product(product_id):
    goods_in_storage = Storage.query.get(product_id)
    if goods_in_storage is not None:
        db.session.delete(goods_in_storage)
        db.session.commit()
        return jsonify({'status': 1})
    else:
        return jsonify({'status': 0})


@app.route("/cart", methods=["POST"])
def add_cart():
    """
    由前端传来包括'customer_id', 'goods_id','bought_num'的json序列，将该json解析加入cart数据库
    :return:
    """
    if request.is_json:  # try except
        data = request.get_json()
        customer_id = data['customer_id']
        goods_id = data['goods_id']
        bought_num = data['bought_num']
        # 当购物车中货物ID与顾客ID均匹配时，需要购买货物数量增加，否则创建该货物并添加数量。
        bought_goods = Cart.query.filter(and_(Cart.customer_id == customer_id, Cart.goods_id == goods_id)).first()
        if bought_goods:
            bought_goods.bought_num += bought_num
            db.session.commit()
        else:
            buying_goods = Cart(customer_id=customer_id, goods_id=goods_id, bought_num=bought_num)
            db.session.add(buying_goods)
            db.session.commit()
        return jsonify(status=1)
    else:
        return jsonify(status=0)

        # # bought_goods = Carts.query.filter_by(title=movie.title).first()
        # customer_id = request.cookies['customer']
        # return repr(customer_id)


# TODO carts直接返回当前购物车中所有商品
@app.route("/cart/<int:customer_id>", methods=["GET"])
def carts(customer_id):
    cart = Cart.query.filter_by(customer_id=customer_id).all()
    all_product_in_cart = []
    if len(cart) != 0:
        for one_product in cart:
            product_info = {'goods_name': one_product.goods_info.goods_name,
                            'goods_price': one_product.goods_info.goods_price,
                            'bought_num': one_product.bought_num,
                            'goods_id': one_product.goods_id}
            all_product_in_cart.append(product_info)
    return jsonify({'all_product_in_cart': all_product_in_cart})


# todo 更新购物车
@app.route("/cart/<int:customer_id>", methods=['PATCH'])
def update_cart(customer_id):
    if request.is_json:
        data = request.get_json()
        goods_id = data['goods_id']
        bought_num = data['goods_num']
    else:
        return jsonify(status=0)

    goods = Cart.query.filter(and_(Cart.customer_id==customer_id, Cart.goods_id==goods_id)).first()
    goods.bought_num = bought_num
    db.session.commit()
    return jsonify(status=1)


# todo 删除购物车商品
@app.route("/cart/<int:customer_id>", methods=['DELETE'])
def delete_cart(customer_id):
    if request.is_json:
        data = request.get_json()
        goods_id = data['goods_id']
    else:
        return jsonify(status=0)
    goods = Cart.query.filter(and_(Cart.customer_id==customer_id, Cart.goods_id==goods_id)).first()
    db.session.delete(goods)
    db.session.commit()
    return jsonify(status=1)


# todo 删除购物车所有商品
@app.route("/cart/<int:customer_id>", methods=['PUT'])
def remove_cart(customer_id):
    goods = Cart.query.filter(and_(Cart.customer_id==customer_id)).all()
    for one_goods in goods:
        db.session.delete(one_goods)
    db.session.commit()
    return jsonify(status=1)

# todo 添加购物车到订单系统
@app.route('/order', methods=['POST'])
def cart_to_order():
        # GET '/carts/order/<int:customer_id>'
    # return {'status':0, 'lack':[goods_id]} 仓储不足{'status':0, 'wrong':"空购物车"} 空购物车
    #        {'status': 1} 商品已经添加到订单
    # 先按cart中货物查询所有库存货物数量，如果库存不足返回不足的货物
    # 如果所有货物足够，则生成一个Order表{order_info,customer_id}
    # 然后将购物车货物添加到GoodsOrder表{order_id,goods_name,bought_num,goods_price}，并从库存里面减去货物数量
    # 清空该用户customer_id的购物车
    customer_id = request.get_json()['customer_id']
    data = Cart.query.filter_by(customer_id=customer_id).all()
    lack = []
    if data:
        for cart_product in data:
            if cart_product.bought_num > cart_product.goods_info.goods_num:
                lack.append(cart_product.goods_id)
            else:
                cart_product.goods_info.goods_num -= cart_product.bought_num
    else:
        return jsonify({'status': 0, 'wrong': "empty cart"})

    if len(lack) == 0:
        new_order = Order(customer_id=customer_id, order_time=datetime.now())
        db.session.add(new_order)
        db.session.commit()

        for order_product in data:
            order_detail = GoodsOrder(goods_name=order_product.goods_info.goods_name,
                                      bought_num=order_product.bought_num,
                                      goods_price=order_product.goods_info.goods_price,
                                      order_id=new_order.id)
            db.session.add(order_detail)
        db.session.query(Cart).filter(Cart.customer_id == customer_id).delete()
        db.session.commit()
        return jsonify({"status": 1})
    else:
        return jsonify({"status": 0, "lack_goods_id": lack})


# 查看订单
@app.route('/order/<int:customer_id>', methods=["GET"])
def order(customer_id):
    # 接口/order/<int:customer_id>，方法 GET
    # 返回json列表[{'order_id':int,
    # 'odrer_time':datetime,
    # 'products':[{goods_name,goods_price,bought_num},]},]
    orders = Order.query.filter_by(customer_id=customer_id).all()
    all_orders = []

    if len(orders) != 0:
        for one_order in orders:
            products = []
            order_info = {'order_id': one_order.id, 'order_time': one_order.order_time}
            for one_product in one_order.order_info:
                product_info = {'goods_name': one_product.goods_name, 'goods_price': one_product.goods_price,
                                'bought_num': one_product.bought_num}
                products.append(product_info)
            order_info['products'] = products
            all_orders.append(order_info)
    return jsonify({'all_orders': all_orders})


if __name__ == "__main__":
    app.run()