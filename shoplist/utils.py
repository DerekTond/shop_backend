from sqlalchemy import and_, or_,text
from shoplist.models import Storage
# TODO -------------  解决查询中的and和or  --------------#
# TODO -------------  解析单个字典  --------------#


def transform_op(op_str):
    if op_str == "eq":
        return "=="
    elif op_str =="lt":
        return "<"
    elif op_str =="le":
        return "<="
    elif op_str =="gt":
        return ">"
    elif op_str =="ge":
        return ">="


def transform_value(value):
    if isinstance(value, str):
        value = "\"%s\"" % value
        return value
    else:
        return str(value)


def parse_dict(one_dict):
    variety = one_dict["key"]
    operation = transform_op(one_dict["op"])
    value = transform_value(one_dict["value"])
    parser_str = "".join([variety, operation, value])
    return text(parser_str)


# -------------  解析单个字典  --------------#

#  -------------  解析一个列表（列表中字典取and）  --------------#
def intersection(parse_list):
    intersect_dict = [parse_dict(i) for i in parse_list]
    return and_(*intersect_dict)

# -------------  解析一个列表（列表中取and）  --------------#

# -------------  解析一个列表（列表中的元素间取or）  --------------#


def search_product(a_list):
    union_list = [intersection(i) for i in a_list]
    return or_(*union_list)

# TODO -------------  解决查询中的or   --------------#


# TODO -------------  查询库存函数   --------------#
def check_storage(product_id):
    product = Storage.query.get(product_id)
    return product.goods_num

import json
if __name__ == "__main__":
    a = [[{
        "key": "goods_name",
        "op": "eq",
        "value": "王涛"
        },{
        "key": "goods_name",
        "op": "eq",
        "value": "王涛"
        }],
        [{
            "key": "goods_name",
            "op": "eq",
            "value": "王涛"
        }, {
            "key": "goods_name",
            "op": "eq",
            "value": "王涛"
        }]]
    print(search_product(a))