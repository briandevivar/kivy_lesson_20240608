from dataclasses import dataclass


# MODEL CLASS:: OOP
@dataclass
class ToysModel:
    id: int
    name: str
    description: str
    price: float
    seller: str
    created: str
    updated: str
