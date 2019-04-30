import click
from shoplist import app, db
from shoplist.models import Storage


@click.command()
def forge():
    db.create_all()

    fake_goods = [
        {'goods_name': '肖申克的救赎', 'goods_num': 1994, 'goods_price': 233},
        {'goods_name': '霸王别姬', 'goods_num': 1993, 'goods_price': 52},
        {'goods_name': '这个杀手不太冷', 'goods_num': 1994, 'goods_price': 23},
        {'goods_name': '阿甘正传', 'goods_num': 1994, 'goods_price': 5},
        {'goods_name': '美丽人生', 'goods_num': 1997, 'goods_price': 7},
        {'goods_name': '泰坦尼克号', 'goods_num': 1997, 'goods_price': 21},
        {'goods_name': '千与千寻', 'goods_num': 2001, 'goods_price': 1994},
    ]

    for thing in fake_goods:
        goods = Storage(goods_name=thing['goods_name'], goods_num=thing['goods_num'],goods_price=thing['goods_price'])
        db.session.add(goods)

    db.session.commit()
    click.echo('Done')


if __name__ == "__main__":
    forge()



