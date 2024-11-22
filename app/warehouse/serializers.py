from rest_framework.serializers import CharField, FloatField, IntegerField, Serializer

from .models import TenantStatistic, WarehouseSize


class TenantStatisticSerializer(Serializer):
    task_id = CharField()
    duration = FloatField()
    warehouse_size = CharField(max_length=20)
    number_of_campaigns = IntegerField()

    def to_internal_value(self, data):
        return TenantStatistic(
            task_id=data["task_id"],
            duration=data["duration"],
            warehouse_size=WarehouseSize(data["warehouse_size"]),
            number_of_campaigns=data["number_of_campaigns"]
        )
