from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel, Field
from typing import Optional
import uuid
from mongo.connection import get_collection


class Order(BaseModel):
    order_id: uuid.uuid4
    pizza_type: str = Field(...)
    size: str
    quantity: int
    is_delivery: bool
    special_instructions: Optional[str] = None


app = FastAPI()

@app.post("/uploadfile")
def uploading_file(order: Order):
    data_mongo = {"order_id": order.order_id,
                  "pizza_type": order.pizza_type,
                  "size": order.size,
                  "quantity": order.quantity,
                  "is_delivery": order.is_delivery,
                  "special_instructions": order.special_instructions,
                  "status": "PREPARING"}
    collection = get_collection()
    inserted = collection.insert_one(data_mongo)
    data_mongo['_id'] = str(data_mongo['_id'])
    return {"message": "data inserted into mongo",
            "data": data_mongo}


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port="8000")