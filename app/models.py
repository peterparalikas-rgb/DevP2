"""Data models for the Vehicle Service API."""
from dataclasses import dataclass, field


@dataclass
class Vehicle:
    """Represents a single vehicle resource.

    Field types match the API contract:
        id       -> int
        nickName -> str
        vin      -> str
        make     -> str
        model    -> str
        year     -> str
        miles    -> int
    """

    id: int
    nickName: str
    vin: str
    make: str
    model: str
    year: str
    miles: int = 0

    def to_dict(self):
        """Serialize the vehicle to a JSON-ready dict."""
        return {
            "id": self.id,
            "nickName": self.nickName,
            "vin": self.vin,
            "make": self.make,
            "model": self.model,
            "year": self.year,
            "miles": self.miles,
        }
