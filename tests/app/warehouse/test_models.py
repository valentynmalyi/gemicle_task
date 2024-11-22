from unittest.mock import Mock, patch

from app.warehouse.models import WarehouseSizeMultiplierFactory


class TestWarehouseSizeMultiplierFactory:
    def test_get(self):
        warehouse_size = Mock()
        with patch.object(WarehouseSizeMultiplierFactory, "map", {warehouse_size: 1}):
            assert WarehouseSizeMultiplierFactory.get(warehouse_size) == 1
