from app.warehouse.models import WarehouseSize
from app.warehouse.serializers import TenantStatisticSerializer


class TestTenantStatisticSerializer:
    def test_to_internal_value(self):
        data = {
            "task_id": "task_id",
            "duration": 25.3,
            "warehouse_size": "X-Small",
            "number_of_campaigns": 1
        }
        tenant_statistic = TenantStatisticSerializer().to_internal_value(data=data)
        assert tenant_statistic.task_id == "task_id"
        assert tenant_statistic.duration == 25.3
        assert tenant_statistic.warehouse_size == WarehouseSize.x_small
        assert tenant_statistic.number_of_campaigns == 1
