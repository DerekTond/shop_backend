from random import randint
from faker import Faker

from shoplist import app, db
from shoplist.models import Storage, Cart, GoodsOrder


fake_info = Faker('zh_CN')


def fake_storage(num):
    # 数量10-20，价格50-100
    for i in range(num):
        goods_name = fake_info.name()
        goods_num = randint(10, 20)
        goods_price = randint(50,100)
        fake_product = Storage(goods_name=goods_name, goods_num=goods_num,goods_price=goods_price)
        db.session.add(fake_product)
    db.session.commit()


def fake_cart(num):
    for i in range(num):
        pass



if __name__ == '__main__':
    # fake_storage(10)
    for i in Storage.query.all():
        print(i.id,i.goods_name, i.goods_num,i.goods_price)