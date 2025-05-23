from datetime import datetime
from pathlib import Path

import pytest

from visit_counter import Browser, VisitCounter, VisitCounterData
from week_day_enum import WeekDay


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
        "hour_count": {},
        "days_of_week": {day: [] for day in WeekDay},
        "browsers": {},
        "unique_ips_by_browser": {browser: set() for browser in Browser},
        "unique_ips": {
            "total": {"176.30.122.233", "123.321.2.335", "190.123.23.22", "197.64.34.223", "121.34.555.212"},
            "2025-04-12": {"176.30.122.233", "123.321.2.335"},
            "2024-03": {"190.123.23.22", "197.64.34.223"},
            "2024": {"190.123.23.22", "197.64.34.223"},
        },
    }


class TestVisitCounter:
    def test_update(self, visit_counter: VisitCounter) -> None:
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

    def test_get_day_count(self, visit_counter: VisitCounter) -> None:
        assert visit_counter.get_day_count(datetime(2025, 4, 12)) == 5

        visit_counter.update(datetime(2025, 4, 12), "176.59.195.170")

        assert visit_counter.get_day_count(datetime(2025, 4, 12)) == 6

    def test_get_month_count(self, visit_counter: VisitCounter) -> None:
        assert visit_counter.get_month_count(datetime(2025, 4, 12)) == 5

        visit_counter.update(datetime(2025, 4, 12), "176.59.195.170")

        assert visit_counter.get_month_count(datetime(2025, 4, 12)) == 6

    def test_get_year_count(self, visit_counter: VisitCounter) -> None:
        assert visit_counter.get_year_count(datetime(2025, 4, 12)) == 5

        visit_counter.update(datetime(2025, 4, 12), "176.59.195.170")

        assert visit_counter.get_year_count(datetime(2025, 4, 12)) == 6

    def test_get_total_count(self, visit_counter: VisitCounter) -> None:
        assert visit_counter.get_total_count() == 30

        visit_counter.update(datetime(2025, 4, 12), "176.59.195.170")

        assert visit_counter.get_total_count() == 31

    def test_get_unique_day_count(self, visit_counter: VisitCounter) -> None:
        assert visit_counter.get_unique_day_count(datetime(2025, 4, 12)) == 2

        visit_counter.update(datetime(2025, 4, 12), "176.59.195.170")

        assert visit_counter.get_unique_day_count(datetime(2025, 4, 12)) == 3

    def test_get_unique_month_count(self, visit_counter: VisitCounter) -> None:
        assert visit_counter.get_unique_month_count(datetime(2025, 4, 12)) == 0

        visit_counter.update(datetime(2025, 4, 12), "176.59.195.170")

        assert visit_counter.get_unique_month_count(datetime(2025, 4, 12)) == 1

    def test_get_unique_year_count(self, visit_counter: VisitCounter) -> None:
        assert visit_counter.get_unique_year_count(datetime(2024, 4, 12)) == 2

        visit_counter.update(datetime(2024, 4, 12), "176.59.195.170")

        assert visit_counter.get_unique_year_count(datetime(2024, 4, 12)) == 3

    def test_get_unique_total_count(self, visit_counter: VisitCounter) -> None:
        assert visit_counter.get_unique_total_count() == 5

        visit_counter.update(datetime(2024, 4, 12), "176.59.195.170")

        assert visit_counter.get_unique_total_count() == 6

    def test_get_hour_count(self, visit_counter: VisitCounter) -> None:
        assert visit_counter.get_hour_count(12) == 0

        visit_counter.update(datetime(2025, 4, 12, 12), "176.59.195.170")

        assert visit_counter.get_hour_count(12) == 1
        assert visit_counter.get_hour_count(10) == 0

    def test_get_browser_count(self, visit_counter: VisitCounter) -> None:
        assert visit_counter.get_browser_count(Browser.CHROME) == 0

        visit_counter.update(
            datetime(2025, 4, 12),
            "176.59.195.170",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        )

        assert visit_counter.get_browser_count(Browser.CHROME) == 1
        assert visit_counter.get_browser_count(Browser.FIREFOX) == 0

    def test_get_browsers_stats(self, visit_counter: VisitCounter) -> None:
        stats = visit_counter.get_browsers_stats()
        assert all(count == 0 for count in stats.values())

        visit_counter.update(
            datetime(2025, 4, 12),
            "176.59.195.170",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        )

        stats = visit_counter.get_browsers_stats()
        assert stats[Browser.CHROME] == 1
        assert sum(stats.values()) == 1

    def test_get_weekdays_count(self, visit_counter: VisitCounter) -> None:
        assert visit_counter.get_weekdays_count(0) == 0

        visit_counter.update(datetime(2025, 4, 14), "176.59.195.170")

        assert visit_counter.get_weekdays_count(0) == 1
        assert visit_counter.get_weekdays_count(1) == 0

    def test_get_unique_weekdays_count(self, visit_counter: VisitCounter) -> None:
        assert visit_counter.get_unique_weekdays_count(0) == 0

        visit_counter.update(datetime(2025, 4, 14), "176.59.195.170")
        visit_counter.update(datetime(2025, 4, 14), "176.59.195.170")

        assert visit_counter.get_unique_weekdays_count(0) == 1

        visit_counter.update(datetime(2025, 4, 14), "176.59.195.171")

        assert visit_counter.get_unique_weekdays_count(0) == 2
