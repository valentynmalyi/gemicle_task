from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import TenantStatisticSerializer
from .services import WarehouseService


class WarehouseStrategyView(APIView):
    # noinspection PyMethodMayBeStatic
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = TenantStatisticSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        service = WarehouseService(data=serializer.validated_data)
        return Response(data=service.get_data())
