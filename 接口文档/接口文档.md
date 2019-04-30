# 购物车子系统

# 1 概述

   购物车子系统是一个包含商品浏览、商品查询、加入购物车、查询购物车、删除购物车、加入订单、查询订单功能的全流程后端系统。系统主要包含了库存、购物车、订单三部分。

# 2 总体设计

### 2.1 逻辑设计

逻辑时序图如下：
![1555939117960.png](https://i.loli.net/2019/04/23/5cbe88d3391ab.png)
### 2.2 数据库设计

数据库关系图
![1555941457078.png](https://i.loli.net/2019/04/23/5cbe88d3497f5.png)


商品仓库数据库storage


| 序列 | 编码        | 列名   | 格式        |
| ---- | ----------- | ------ | ----------- |
| 1    | id          | 主键   | bigint      |
| 2    | goods_name  | 商品名 | varchar(80) |
| 3    | goods_num   | 数量   | int         |
| 4    | goods_price | 价格   | int         |



购物车数据库cart

| 序列 | 编码        | 列名     | 格式   |
| ---- | ----------- | -------- | ------ |
| 1    | id          | 主键     | bigint |
| 2    | goods_id    | 商品id   | bigint |
| 3    | bought_num  | 购买数量 | int    |
| 4    | customer_id | 客户id   | bigint |
| 5    | goods_info  | 商品信息 |        |

订单数据库order

| 序列 | 编码        | 列名     | 格式     |
| ---- | ----------- | -------- | -------- |
| 1    | id          | 主键     | bigint   |
| 2    | customer_id | 客户id   | bigint   |
| 3    | order_time  | 订单时间 | datetime |
| 4    | order_info  | 订单详情 |          |



订单货物详情goodsorder

| 序列 | 编码        | 列名     | 格式        |
| ---- | ----------- | -------- | ----------- |
| 1    | id          | 主键     | bigint      |
| 2    | order_id    | 订单id   | bigint      |
| 3    | goods_name  | 商品名   | varchar(80) |
| 4    | bought_num  | 购买数量 | int         |
| 5    | goods_price | 购买价格 | int         |

顾客customer

| 序列 | 编码 | 列名   | 格式        |
| ---- | ---- | ------ | ----------- |
| 1    | id   | 主键   | bigint      |
| 2    | name | 用户名 | varchar(80) |


# 3 API

## 3.1 库存

### 3.1.1 按货物id查询商品
> GET   /storage/\<int:product_id\>
>
> return {status:\<int\>,
>        goods_id:{goods_name:\<str\>,
>        goods_num:\<int\>,
>       goods_price:\<int\>}}

* 例子1

    查询库存中存在的货物id

    ~~~python
    /storage/1 GET
    ~~~

    ~~~json
    return
        {
        "1": {
            "goods_name": "王涛",
            "goods_num": 12,
            "goods_price": 96
        },
        "status": 1
        }
    ~~~
 
* 例子2

  查询库存中没有的货物id

    ~~~
    /storage/99 GET
    ~~~

    ~~~json
    return
        {
            "status": 0
        }
    ~~~

### 3.1.2 按关键词搜索商品

> POST   /product
>
> body -> {"search":[[{"key":,"op":,"value":}]]}
>
> 传入json的key为'search'，value是一个两层数组，
> 数组内元素为一个字典，字典包含3个kv值，分别为'key'、'op'、'value'。
> 其中'key'可以对应商品的所有属性(goods_name、goods_num、goods_price);'op'对应操作('eq'对应==、'gt'对应>、'ge'对应>=、'lt'对应<、'le'对应<=);'value'对应数值，当'key'为goods_name时，值应为字符串类型。数组外层取or运算，内层取and运算。
>
> return {goods_id:{goods_name:,goods_num:,goods_price:},}

* 例子1

    查询数量>11且价格>90的商品，或名为'李兰英'的商品

    ~~~JSON
    /product POST

    {
        "search": [
            [
                {
                    "key": "goods_num",
                    "op": "gt",
                    "value": 11
                },
                {
                    "key": "goods_price",
                    "op": "gt",
                    "value": 90
                }
            ],
            [
                {
                    "key": "goods_name",
                    "op": "eq",
                    "value": "李兰英"
                }
            ]
        ]
    }
    ~~~

    ~~~json
    return
    {
        "1": {
            "goods_name": "王涛",
            "goods_num": 12,
            "goods_price": 96
        },
        "5": {
            "goods_name": "李兰英",
            "goods_num": 2,
            "goods_price": 97
        },
        "6": {
            "goods_name": "刘芳",
            "goods_num": 13,
            "goods_price": 97
        },
        "8": {
            "goods_name": "王丹丹",
            "goods_num": 14,
            "goods_price": 91
        },
        "11": {
            "goods_name": "cb121a",
            "goods_num": 18931,
            "goods_price": 181
        },
        "12": {
            "goods_name": "法师",
            "goods_num": 18,
            "goods_price": 99
        }
    }
    ~~~

### 3.1.3 添加新商品

> POST  /storage
> 
> body -> {"goods_name":\<str\>,"goods_num":\<int\>,"goods_price":\<int\>}
> 
> return -> {'status':\<int\>, 'goods_id':\<int\>}

如果新增商品缺少字段(价格、数量)会返回status:0及缺失字段

* 例子1

  添加货物

    ~~~json
    /storage POST

    {
        "goods_name": "马斯塔",
        "goods_num": 10,
        "goods_price": 99
    }
    ~~~

    ~~~json
    return
    {
        "goods_id": 13,
        "status": 1
    }
    ~~~

* 例子2

  添加的货物缺少数量字段

    ~~~json
    /storage POST

    {
        "goods_name": "马斯塔",
        "goods_price": 99
    }
    ~~~

    ~~~json
    return
    {
        "error": "'goods_num'",
        "status": 0
    }  
    ~~~

### 3.1.4 更新商品信息

> PATCH /storage/\<int:product_id\>
> 
> body -> {"add_num":\<int\>}/{"minus_num":\<int\>}
> 
> return -> {"status":1}

* 例子1

  增加货物

    ~~~json
    /storage/1 PATCH

    {
        "add_num":10
    }
    ~~~

    ~~~json
    return
    {
    "status": 1
    }
    ~~~

* 例子2

  减少货物

    ~~~json
    /storage/1 PATCH

    {
        "minus_num":10
    }
    ~~~

    ~~~json
    return
    {
    "status": 1
    }
    ~~~

* 例子3

  没有此货物id

    ~~~json
    /storage/99 PATCH

    {
        "minus_num":10
    }
    ~~~

    ~~~json
    return
    {
    "status": 0
    }
    ~~~

### 3.1.5 移除商品

>1 DELETE /storage/\<int:product_id\>
>
> return -> {"status":\<int\>}
> 
> 当货物id不存在则返回{'status'：0}

* 例子1

  根据id删除货物

    ~~~json
    /storage/1 DELETE
    ~~~

    ~~~json
    return
    {
    "status": 1
    }
    ~~~

## 3.2 购物车

### 3.2.1 添加商品至购物车

> POST  /cart
> 
> body -> {"customer_id":\<int\>,"goods_id":\<int\>,"bought_num":\<int\>}
> 
> return -> {'status':\<int\>}

将添加至购物车，需要客户id"customer_id",商品id"goods_id"，以及购买数量"bought_num"

* 例子1

  添加商品

    ~~~json
    /cart POST

    {
        "customer_id": 4,
        "goods_id": 6,
        "bought_num": 1
    }
    ~~~

    ~~~json
    return
    {
        "status": 1
    }
    ~~~

### 3.2.2 查看购物车

> GET  /cart/\<int\>
> 
> return -> 
> ~~~
> {
>    "all_product_in_cart": [
>        {
>            "bought_num": <int>,
>            "goods_id": <int>,
>            "goods_name": <str>,
>            "goods_price": <int>
>        }
>    ]
>}
>~~~
>
> 查看购物车，需要客户id"customer_id"，会返回一个key为 "all_product_in_cart"，value为列表，数组元素为该客户购物车中所有商品，如果没有商品则返回一个空列表

* 例子1

  查看购物车

    ~~~json
    /cart/1 GET

    {
        "customer_id": 4,
        "goods_id": 6,
        "bought_num": 1
    }
    ~~~

    ~~~json
    return
    {
        "all_product_in_cart": [
            {
                "bought_num": 2,
                "goods_id": 6,
                "goods_name": "刘芳",
                "goods_price": 97
            }
        ]
    }
    ~~~

### 3.2.3 更新购物车商品数量

> PATCH /carts/\<int:customer_id\> 
> 
> body -> {"goods_id":\<int\>,"goods_num":\<int\>}
> 
> return -> {"status":1}
> 
> 传入商品id及商品数量，会直接将购物车中数量进行更新，并返回状态码

* 例子1

  更新购物车

    ~~~json
    /cart/4 PATCH

    {
        "goods_id": 6,
        "goods_num": 3
    }
    ~~~

    ~~~json
    return
    {
        "status":1
    }
    ~~~

### 3.2.4 删除购物车商品

> DELETE /cart/\<int:customer_id\> 
> 
> body -> {"goods_id":\<int\>}
> 
> return -> {"status":1}
> 
> 传入商品id及，会直接将购物车中该商品删除，并返回状态码

* 例子1

  删除购物车中商品

    ~~~json
    /cart/4 DELETE

    {
        "goods_id": 6
    }
    ~~~

    ~~~json
    return
    {
        "status":1
    }
    ~~~

### 3.2.5 清空购物车

> PUT /cart/\<int:customer_id\>
> 
> return -> {"status":1}
> 
> 直接将客户购物车中所有商品删除，并返回状态码

* 例子1

  删除购物车中商品

    ~~~json
    /cart/4 PUT
    ~~~

    ~~~json
    return
    {
        "status":1
    }
    ~~~


## 3.3 订单

### 3.3.1 将购物车商品提交到订单

> POST /order
> 
> body -> {"customer_id":4}
> 
> return
> 
> ①购物车为空
> {
>    "status": 0,
>    "wrong": "empty cart"
> }
> 
> ②购物车成功提交到订单
>  {  "status": 1
>  }
> 
> ③{
>    "lack_goods_id": [
>        <int>
>    ],
>    "status": 0
>}

* 例子1

  成功提交购物车到订单

    ~~~json
    /order POST

    {"customer_id":4}
    ~~~

    ~~~json
    return
    {
        "status":1
    }
    ~~~

* 例子2

  购物车为空

    ~~~json
    /order POST

    {"customer_id":4}
    ~~~

    ~~~json
    return
    {
        "status":0,
        "wrong":"empty cart"
    }
    ~~~

* 例子3

  仓储不足,返回数量不足的商品id

    ~~~json
    /order POST

    {"customer_id":4}
    ~~~

    ~~~json
    return
    {
        "status":0,
        "lack":[6]
    }
    ~~~
### 3.3.2 查看订单

> GET  /oder/\<int\>
> 
> return -> 
> ~~~
> {
>    "all_orders": [
>        {
>            "order_id": <int>,
>            "order_time": <datetime>,
>            "products": [
>                {
>                    "bought_num": <int>,
>                    "goods_name": <str>,
>                    "goods_price": <int>
>                }
>            ]
>        }
>    ]
>}
>~~~
>
> 查看订单，需要客户id"customer_id"，会返回一个key为 "all_orders"，value为列表，数组元素为该客户所有订单，订单包括订单id，订单时间及此次订单购买的商品列表。如果没有订单则返回一个空列表。

* 例子1

  查看订单

    ~~~json
    /order/2 GET

    ~~~

    ~~~json
    return
    {
        "all_orders": [
            {
                "order_id": 4,
                "order_time": "Sat, 20 Apr 2019 15:43:05 GMT",
                "products": [
                    {
                        "bought_num": 5,
                        "goods_name": "李兰英",
                        "goods_price": 97
                    }
                ]
            }
        ]
    }
    ~~~