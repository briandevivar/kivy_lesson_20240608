# FULLSTACKDEVTUTORIALS.COM
# TOPIC: KIVYMD AND SQLITE3
# LECTURER: BRIAN DE VIVAR
# DATE: JUNE 08, 2024
# YT: https://www.youtube.com/channel/UC3veSIv6YTZ6rK6UEOFmFmg
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
