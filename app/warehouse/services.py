from collections import defaultdict
from statistics import median
from typing import DefaultDict

from .models import TenantStatistic, WarehouseSize, WarehouseSizeMultiplierFactory


class DataProcessor:
    def __init__(self, data: list[TenantStatistic]):
        self.initial_data = data
        self.data: list[TenantStatistic] = []
        self.grouped_data: DefaultDict[str, list[float]] = defaultdict(list)
        self.median_data: dict[str, float] = {}

    def _filter(self) -> None:
        self.data.extend(
            statistic for statistic in self.initial_data
            if statistic.number_of_campaigns > 0
        )

    def _normalize_data(self) -> None:
        for row in self.data:
            row.normalized_duration = row.duration / WarehouseSizeMultiplierFactory.get(row.warehouse_size)

    def _update_grouped_data(self) -> None:
        for row in self.data:
            self.grouped_data[row.task_id].append(row.duration)

    def _update_median_data(self) -> None:
        for task_id, lst in self.grouped_data.items():
            self.median_data[task_id] = median(lst)

    def process(self) -> None:
        self._filter()
        self._normalize_data()
        self._update_grouped_data()
        self._update_median_data()


class WarehouseSizeSelector:
    duration_limit = 20
    warehouse_size_list: list[WarehouseSize] = [
        WarehouseSize.x_small,
        WarehouseSize.small,
        WarehouseSize.medium,
        WarehouseSize.large,
        WarehouseSize.x_large,
        WarehouseSize.x2_large,
    ]
    default_warehouse_size = WarehouseSize.x3_large

    def __init__(self, data_processor: DataProcessor):
        self.data_processor = data_processor
        self.strategy: dict[str, WarehouseSize] = {}

    def update_strategy(self) -> None:
        for task_id in self.data_processor.median_data:
            self._process_task_id(task_id=task_id)

    def _process_task_id(self, task_id: str) -> None:
        for warehouse_size in self.warehouse_size_list:
            if self._process_warehouse_size(task_id=task_id, warehouse_size=warehouse_size):
                break
        else:
            self.strategy[task_id] = self.default_warehouse_size

    def _process_warehouse_size(self, task_id: str, warehouse_size: WarehouseSize) -> bool:
        duration = (
            self.data_processor.median_data[task_id] /
            WarehouseSizeMultiplierFactory.get(warehouse_size=warehouse_size)
        )
        if self.duration_limit > duration:
            self.strategy[task_id] = warehouse_size
            return True
        return False


class WarehouseStrategyService:
    def __init__(self, data: list[TenantStatistic]):
        data_processor = DataProcessor(data=data)
        self.warehouse_size_selector = WarehouseSizeSelector(data_processor=data_processor)

    def get_data(self) -> dict[str, WarehouseSize]:
        self.warehouse_size_selector.data_processor.process()
        self.warehouse_size_selector.update_strategy()
        return self.warehouse_size_selector.strategy
