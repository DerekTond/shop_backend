from datetime import datetime
from random import randint
from shoplist.models import GoodsOrder,Order


def f1():
    x= 88
    def f2():
        print(x)
    return f2

def test(num):
    in_num = num
    def nested(label):
        global in_num
        in_num+=1
        print(label,in_num)
    return nested



class Person:
    pass

def make_person():

    return Person()
def test_list():
    empty_list = []
    dicta = {}
    for i in empty_list:
        lalala = []
        if i is None:
            print(2)
        else:
            print(1)
    dicta['test'] = lalala
    return dicta


def check_order():
    orders = Order.query.filter_by(id=11).first()
    for i in orders.order_info:
        print(i.goods_name,i.bought_num)

if __name__ == "__main__":
    1+None