from pymongo import MongoClient
from bson.binary import UuidRepresentation


def get_collection():
    client = MongoClient('mongodb://localhost:27017/',
                         UuidRepresentation = 'standard')
    db = client['week-18-db']
    collection = db['pizza-orders']
    return collection


# data_mongo = {"order_id": 'order.order_id',
#                   "pizza_type": 'order.pizza_type',
#                   "size": 'order.size',
#                   "quantity": 'order.quantity',
#                   "is_delivery": 'order.is_delivery',
#                   "special_instructions": 'order.special_instructions',
#                   "status": "PREPARING"}
# inser = collection.insert_one(data_mongo)
# result = collection.find_one()
# print(result)