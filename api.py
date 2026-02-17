from fastapi import FastAPI, UploadFile, File
import json
import uvicorn
from pydantic import BaseModel, Field
from typing import Optional
import uuid
from mongo.connection import get_collection
from kafka.producer import send_to_kafka


class Order(BaseModel):
    order_id: uuid.uuid4
    pizza_type: str = Field(...)
    size: str
    quantity: int
    is_delivery: bool
    special_instructions: Optional[str] = None


def get_mongo_data(order: Order):
    data_mongo = {"order_id": str(order.order_id),
                  "pizza_type": order.pizza_type,
                  "size": order.size,
                  "quantity": order.quantity,
                  "is_delivery": order.is_delivery,
                  "special_instructions": order.special_instructions,
                  "status": "PREPARING"}
    return data_mongo

app = FastAPI()

@app.post("/uploadfile")
def uploading_file(file: UploadFile = File(...)):
    collection = get_collection()
    order_load = json.load(file.file)
    order_load = [order_load]
    count = 0
    for order in order_load:
        data_mongo = get_mongo_data(order)
        inserted = collection.insert_one(data_mongo)
        data_mongo['_id'] = str(data_mongo['_id'])
        count += 1
        send_to_kafka(data_mongo)
    return {"message": "data inserted successfully",
            "total": f"{count} orders inserted"}


@app.get("/order/{order_id}")
def get_by_id(order_id):
    pass



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port="8000")