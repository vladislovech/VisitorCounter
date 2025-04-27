from datetime import datetime
from pathlib import Path

import pytest

from visit_counter import VisitCounter, VisitCounterData


@pytest.fixture
def visit_counter(test_user_info: VisitCounterData, tmp_path: Path) -> VisitCounter:
    counter = VisitCounter(test_user_info, str(tmp_path / "statistics.json"))
    return counter


@pytest.fixture()
def test_user_info() -> VisitCounterData:
    return {
        "total_count": 30,
        "day_count": {"2025-04-12": 5, "2024-03-15": 15},
        "month_count": {"2025-04": 5, "2024-03": 15},
        "year_count": {"2025": 5, "2024": 15},
        "unique_ips": {
            "total": {"176.30.122.233", "123.321.2.335", "190.123.23.22", "197.64.34.223", "121.34.555.212"},
            "2025-04-12": {"176.30.122.233", "123.321.2.335"},
            "2024-03": {"190.123.23.22", "197.64.34.223"},
            "2024": {"190.123.23.22", "197.64.34.223"},
        },
    }


def test_update(visit_counter: VisitCounter) -> None:
    visit_counter.update(datetime(2025, 4, 12), "176.59.195.170")

    assert visit_counter.data["total_count"] == 31
    assert visit_counter.data["day_count"]["2025-04-12"] == 6
    assert visit_counter.data["day_count"]["2024-03-15"] == 15
    assert visit_counter.data["month_count"]["2025-04"] == 6
    assert visit_counter.data["month_count"]["2024-03"] == 15
    assert visit_counter.data["year_count"]["2025"] == 6
    assert visit_counter.data["year_count"]["2024"] == 15

    assert len(visit_counter.data["unique_ips"]["total"]) == 6
    assert len(visit_counter.data["unique_ips"]["2025-04-12"]) == 3
    assert len(visit_counter.data["unique_ips"]["2025-04"]) == 1
    assert len(visit_counter.data["unique_ips"]["2024-03"]) == 2
    assert len(visit_counter.data["unique_ips"]["2024"]) == 2


def test_get_day_count(visit_counter: VisitCounter) -> None:
    assert visit_counter.get_day_count(datetime(2025, 4, 12)) == 5

    visit_counter.update(datetime(2025, 4, 12), "176.59.195.170")

    assert visit_counter.get_day_count(datetime(2025, 4, 12)) == 6


def test_get_month_count(visit_counter: VisitCounter) -> None:
    assert visit_counter.get_month_count(datetime(2025, 4, 12)) == 5

    visit_counter.update(datetime(2025, 4, 12), "176.59.195.170")

    assert visit_counter.get_month_count(datetime(2025, 4, 12)) == 6


def test_get_year_count(visit_counter: VisitCounter) -> None:
    assert visit_counter.get_year_count(datetime(2025, 4, 12)) == 5

    visit_counter.update(datetime(2025, 4, 12), "176.59.195.170")

    assert visit_counter.get_year_count(datetime(2025, 4, 12)) == 6


def test_get_total_count(visit_counter: VisitCounter) -> None:
    assert visit_counter.get_total_count() == 30

    visit_counter.update(datetime(2025, 4, 12), "176.59.195.170")

    assert visit_counter.get_total_count() == 31


def test_get_unique_day_count(visit_counter: VisitCounter) -> None:
    assert visit_counter.get_unique_day_count(datetime(2025, 4, 12)) == 2

    visit_counter.update(datetime(2025, 4, 12), "176.59.195.170")

    assert visit_counter.get_unique_day_count(datetime(2025, 4, 12)) == 3


def test_get_unique_month_count(visit_counter: VisitCounter) -> None:
    assert visit_counter.get_unique_month_count(datetime(2025, 4, 12)) == 0

    visit_counter.update(datetime(2025, 4, 12), "176.59.195.170")

    assert visit_counter.get_unique_month_count(datetime(2025, 4, 12)) == 1


def test_get_unique_year_count(visit_counter: VisitCounter) -> None:
    assert visit_counter.get_unique_year_count(datetime(2024, 4, 12)) == 2

    visit_counter.update(datetime(2024, 4, 12), "176.59.195.170")

    assert visit_counter.get_unique_year_count(datetime(2024, 4, 12)) == 3


def test_get_unique_total_count(visit_counter: VisitCounter) -> None:
    assert visit_counter.get_unique_total_count() == 5

    visit_counter.update(datetime(2024, 4, 12), "176.59.195.170")

    assert visit_counter.get_unique_total_count() == 6
