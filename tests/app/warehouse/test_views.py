from unittest.mock import Mock, patch

from app.warehouse.serializers import TenantStatisticSerializer
from app.warehouse.services import WarehouseStrategyService
from app.warehouse.views import WarehouseStrategyView


class TestWarehouseStrategyView:
    def test_post(self):
        request = Mock()
        serializer_cls = Mock()
        serializer = serializer_cls.return_value
        service_cls = Mock()
        view = WarehouseStrategyView()
        with (
            patch(f"{WarehouseStrategyView.__module__}.{TenantStatisticSerializer.__name__}", serializer_cls),
            patch(f"{WarehouseStrategyView.__module__}.{WarehouseStrategyService.__name__}", service_cls),
        ):
            response = view.post(request=request)
        serializer_cls.assert_called_once_with(data=request.data, many=True)
        serializer.is_valid.assert_called_once_with(raise_exception=True)
        service_cls.assert_called_once_with(data=serializer.validated_data)
        assert response.data == service_cls.return_value.get_data.return_value
