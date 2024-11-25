from collections import defaultdict
from unittest.mock import Mock, patch

from app.warehouse.models import WarehouseSizeMultiplierFactory
from app.warehouse.services import DataProcessor, WarehouseSizeSelector, WarehouseStrategyService


class TestDataProcessor:
    def test_init(self):
        DataProcessor(data=[])

    def test_filter(self):
        statistic1 = Mock(number_of_campaigns=1)
        statistic2 = Mock(number_of_campaigns=0)
        processor = Mock(data=[], initial_data=[statistic1, statistic2])
        DataProcessor._filter(processor)
        assert processor.data == [statistic1]

    def test_normalize_data(self):
        statistic = Mock(duration=4)
        processor = Mock(data=[statistic])
        with patch.object(WarehouseSizeMultiplierFactory, WarehouseSizeMultiplierFactory.get.__name__, return_value=2):
            DataProcessor._normalize_data(processor)
        assert statistic.normalized_duration == 2.0

    def test_update_grouped_data(self):
        statistic1 = Mock(duration=1, task_id="1")
        statistic2 = Mock(duration=2, task_id="1")
        statistic3 = Mock(duration=1, task_id="2")
        processor = Mock(data=[statistic1, statistic2, statistic3], grouped_data=defaultdict(list))
        DataProcessor._update_grouped_data(processor)
        assert processor.grouped_data == {"1": [1, 2], "2": [1]}

    def test_update_median_data(self):
        processor = Mock(grouped_data={"1": [1, 2, 10000], "2": [1, 10, 12, 10000]}, median_data={})
        DataProcessor._update_median_data(processor)
        assert processor.median_data == {"1": 2, "2": 11.0}

    def test_process(self):
        processor = Mock()
        DataProcessor.process(processor)
        processor._filter.assert_called_once()
        processor._normalize_data.assert_called_once()
        processor._update_grouped_data.assert_called_once()
        processor._update_median_data.assert_called_once()


class TestWarehouseSizeSelector:
    def test_init(self):
        WarehouseSizeSelector(data_processor=Mock())

    def test_update_strategy(self):
        selector = Mock()
        selector.data_processor.median_data = {"1": 1, "2": 2}
        WarehouseSizeSelector.update_strategy(selector)
        assert selector._process_task_id.call_count == 2

    def test_process_task_id(self):
        selector = Mock(strategy={})
        selector._process_warehouse_size.side_effect = [False, True]
        selector.warehouse_size_list = [Mock(), Mock()]
        WarehouseSizeSelector._process_task_id(self=selector, task_id="1")
        assert selector.strategy == {}
        assert selector._process_warehouse_size.call_count == 2

    def test_process_task_id_set_default_warehouse(self):
        selector = Mock(strategy={})
        selector.warehouse_size_list = []
        WarehouseSizeSelector._process_task_id(self=selector, task_id="1")
        assert selector.strategy == {"1": selector.default_warehouse_size}

    def test_process_warehouse_size(self):
        warehouse_size = Mock()
        selector = Mock(duration_limit=3, strategy={})
        selector.data_processor.median_data = {"1": 5}
        with patch.object(
            WarehouseSizeMultiplierFactory,
            WarehouseSizeMultiplierFactory.get.__name__,
            return_value=2,
        ):
            actual = WarehouseSizeSelector._process_warehouse_size(
                self=selector, task_id="1", warehouse_size=warehouse_size
            )
        assert selector.strategy == {"1": warehouse_size}
        assert actual is True

    def test_process_warehouse_size_not_set(self):
        warehouse_size = Mock()
        selector = Mock(duration_limit=3, strategy={})
        selector.data_processor.median_data = {"1": 7}
        with patch.object(
            WarehouseSizeMultiplierFactory,
            WarehouseSizeMultiplierFactory.get.__name__,
            return_value=2,
        ):
            actual = WarehouseSizeSelector._process_warehouse_size(
                self=selector, task_id="1", warehouse_size=warehouse_size
            )
        assert selector.strategy == {}
        assert actual is False


class TestWarehouseStrategy:
    def test_init(self):
        WarehouseStrategyService(data=[])

    def test_get_data(self):
        service = Mock()
        actual = WarehouseStrategyService.get_data(service)
        service.warehouse_size_selector.data_processor.process.assert_called_once()
        service.warehouse_size_selector.update_strategy()
        assert actual == service.warehouse_size_selector.strategy
