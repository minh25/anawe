from pymongo import MongoClient, UpdateOne
import queue

db = MongoClient("mongodb+srv://giftza:giftza@cluster0.qquas.mongodb.net/test?retryWrites=true&w=majority").test

bulk = []


def push_bulk(detail_product):
    bulk.append(UpdateOne({'product_code': detail_product['product_code']},
                          {'$set': detail_product},
                          upsert=True))


def push_mongo(detail_products=queue.Queue()):
    while detail_products.qsize() > 0:
        detail_product = detail_products.get()
        push_bulk(detail_product)

    db.product2.bulk_write(bulk)


def main():
    q = queue.Queue()

    for _ in range(30):
        q.put(
            {
                'url': 'https://www.giftza.co/campaigns/department/housewares/product/mug/tags/Holidays%20%26'
                       '%20Events/mom-pee-yourself?retailProductCode=DBD375D877A0B6-2A4918C9F9EE-MS0-TC1001-WHT',
                'product_code': '375D877A0B6-2A4918C9F9EE-MS0-TC1001-WHT',
                'product_price': '$20.95',
                'image_urls':
                    [
                        'https://cdn.32pt.com/public/sl-prod-od-0/images/retail-products/DBD375D877A0B6'
                        '/DBD375D877A0B6-2A4918C9F9EE-MS0-TC1001-WHT/front/thumb.jpg',
                        'https://cdn.32pt.com/public/sl-prod-od-0/images/retail-products/DBD375D877A0B6'
                        '/DBD375D877A0B6-2A4918C9F9EE-MS0-TC1001-WHT/back/thumb.jpg '
                    ],
                'product_name': 'Mom Pee Yourself Mug',
                'campaign_details': 'LIMITED EDITION <br/> Safe and secure checkout via:\xa0 TIP: SHARE it with your '
                                    'friends, order together and save on shipping. Click "Buy Now" to order '
                                    'TODAY\ufeff '
            }
        )

    push_mongo(q)


if __name__ == '__main__':
    main()
