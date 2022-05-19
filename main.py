from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from enum import Enum

app = FastAPI()

""" Gibt eine ID zurück, welche noch nicht belegt ist in orders """
def getFreeOrderId():
    freeIndex = 0
    for index in orders:
        if index == freeIndex:
            freeIndex += 1

    return freeIndex


class PizzaSize(Enum):
    small = 1
    medium = 2
    large = 3


class Order(BaseModel):
    pizza_name: str
    size: PizzaSize
    customer_fullname: str
    address: str
    comment: str = "Keine Anmerkung"
    
orders = {
    0: Order(pizza_name="Tonno", size=PizzaSize.small, customer_fullname="Jhonni Joel", address="Am Baum 3", comment="HALOOOO"),
    1: Order(pizza_name="Magaritaaa", size=PizzaSize.large, customer_fullname="Peter Joel", address="Am Baum 3", comment="HALOOOO"),
    2: Order(pizza_name="Salami", size=PizzaSize.medium, customer_fullname="Anja Müller", address="Am Baum 5")
}

@app.get("/orders/")
def getOrders():
    return orders


@app.get("/orders/{order_id}")
def getOrderById(order_id: int):
    if orders.get(order_id) != None:
        return orders[order_id]
    else:
        return { "message": 'Keine Bestellung mit der angegebenen ID gefunden.' }

@app.post("/orders/")
def createOrder(item: Order, response: Response):
    item_dict = item.dict()
    id = getFreeOrderId()

    orders[id] = item_dict

    response.status_code = status.HTTP_201_CREATED

    return {"id": id, "message": "Bestellung erfolgreich hinzugefügt."}

@app.put("/orders/{order_id}")
def updateOrder(order_id: int, item: Order):
    if orders.get(order_id) != None:
        item_dict = item.dict()
        orders[order_id] = item_dict
        return {"id": order_id, **item_dict}
    else:
        return { "message": 'Keine Bestellung mit der angegebenen ID gefunden.' }

@app.delete("/orders/{order_id}")
def deleteOrder(order_id: int, response: Response):
    if orders.get(order_id) != None:
        del orders[order_id]

        return {"id": order_id, "message":"Erfolgreich gelöscht"}
    else:
        return { "message": 'Keine Bestellung mit der angegebenen ID gefunden.' }

"""
Test Daten:

{
    "pizza_name": "Tonno",
    "size": 1,
    "customer_fullname": "Toni Pepperoni",
    "address": "Burgstraße 14",
    "comment": "Ohne Zwiebel bitte"
}

Header: Content-Type: application/json

Start cmd: uvicorn main:app --reload

"""