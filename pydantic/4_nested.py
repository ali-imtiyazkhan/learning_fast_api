from pydantic import BaseModel
from typing import List

class Address(BaseModel):
    street: str
    city: str
    postcode: str

class Order(BaseModel):
    order_id: int
    items: List[str]
    ship_to: Address   # nested model

# Dict is auto-converted to Address
order = Order(
    order_id=1,
    items=["book", "pen"],
    ship_to={"street": "10 Elm St",
             "city": "London",
             "postcode": "EC1A 1BB"}
)
print(order.ship_to.city)  #  "London"
print(order.model_dump())   #  full dict