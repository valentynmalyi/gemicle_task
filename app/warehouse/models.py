from dataclasses import dataclass, field
from enum import StrEnum


class WarehouseSize(StrEnum):
    x_small = "X-Small"
    small = "Small"
    medium = "Medium"
    large = "Large"
    x_large = "X-Large"
    x2_large = "2X-Large"
    x3_large = "3X-Large"


class WarehouseSizeMultiplierFactory:
    map = {
        WarehouseSize.x_small: 1,
        WarehouseSize.small: 2,
        WarehouseSize.medium: 4,
        WarehouseSize.large: 8,
        WarehouseSize.x_large: 16,
        WarehouseSize.x2_large: 32,
        WarehouseSize.x3_large: 64,
    }

    @classmethod
    def get(cls, warehouse_size: WarehouseSize):
        return cls.map[warehouse_size]


@dataclass
class TenantStatistic:
    task_id: str
    duration: float
    warehouse_size: WarehouseSize
    number_of_campaigns: int
    normalized_duration: int = field(default=0)
