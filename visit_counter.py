import json
import os
from datetime import datetime
from typing import TypedDict, cast


class VisitCounterData(TypedDict):
    """
    аннотация словаря из метода _get_empty_data() для mypy
    """

    total_count: int
    day_count: dict[str, int]
    month_count: dict[str, int]
    year_count: dict[str, int]
    unique_ips: dict[str, set[str]]


class VisitCounter:
    def __init__(self, data: VisitCounterData | None = None, filename: str = "statistics.json") -> None:
        self._filename = filename
        self._data = data or self._load_or_initialize_data()

    @property
    def filename(self) -> str:
        return self._filename

    @property
    def data(self) -> VisitCounterData:
        return self._data

    def update(self, date: datetime, ip: str) -> None:
        """
        обновляет счетчики посещений
        при каждом обращении к серверу по указанному дню
        """
        day_str = date.strftime("%Y-%m-%d")
        month_str = date.strftime("%Y-%m")
        year_str = date.strftime("%Y")

        self.data["total_count"] += 1
        self.data["day_count"][day_str] = self.data["day_count"].get(day_str, 0) + 1
        self.data["month_count"][month_str] = self.data["month_count"].get(month_str, 0) + 1
        self.data["year_count"][year_str] = self.data["year_count"].get(year_str, 0) + 1

        self.data["unique_ips"]["total"].add(ip)
        self.data["unique_ips"][day_str] = self.data["unique_ips"].get(day_str, set()) | {ip}
        self.data["unique_ips"][month_str] = self.data["unique_ips"].get(month_str, set()) | {ip}
        self.data["unique_ips"][year_str] = self.data["unique_ips"].get(year_str, set()) | {ip}

        self._save_data()

    def get_day_count(self, date: datetime) -> int:
        """
        возвращает кол-во посещений за указанный день
        """
        day_str = date.strftime("%Y-%m-%d")
        return self.data["day_count"].get(day_str, 0)

    def get_month_count(self, date: datetime) -> int:
        """
        возвращает кол-во посещений за указанный месяц
        """
        month_str = date.strftime("%Y-%m")
        return self.data["month_count"].get(month_str, 0)

    def get_year_count(self, date: datetime) -> int:
        """
        возвращает кол-во посещений за указанный год
        """
        year_str = date.strftime("%Y")
        return self.data["year_count"].get(year_str, 0)

    def get_total_count(self) -> int:
        """
        возвращает кол-во посещений за все время
        """
        return self.data.get("total_count", 0)

    def get_unique_day_count(self, date: datetime) -> int:
        """
        возвращает кол-во уникальных посещений за указанный день
        """
        day_str = date.strftime("%Y-%m-%d")
        return len(self.data["unique_ips"].get(day_str, set()))

    def get_unique_month_count(self, date: datetime) -> int:
        """
        возвращает кол-во уникальных посещений за указанный месяц
        """
        month_str = date.strftime("%Y-%m")
        return len(self.data["unique_ips"].get(month_str, set()))

    def get_unique_year_count(self, date: datetime) -> int:
        """
        возвращает кол-во уникальных посещений за указанный год
        """
        year_str = date.strftime("%Y")
        return len(self.data["unique_ips"].get(year_str, set()))

    def get_unique_total_count(self) -> int:
        """
        возвращает кол-во уникальных посещений за все время
        """
        return len(self.data["unique_ips"].get("total", set()))

    def _get_empty_data(self) -> VisitCounterData:
        """
        возвращает словарь для первичной инициализации
        """
        return {
            "total_count": 0,
            "day_count": {},
            "month_count": {},
            "year_count": {},
            "unique_ips": {
                "total": set(),
            },
        }

    def _save_data(self) -> None:
        """
        подготавливает словарь для записи в формате json,
        заменяя мноожества на списки
        """
        data_to_save = {
            "total_count": self.data["total_count"],
            "day_count": self.data["day_count"],
            "month_count": self.data["month_count"],
            "year_count": self.data["year_count"],
            "unique_ips": {k: list(v) for k, v in self.data["unique_ips"].items()},
        }

        with open(self.filename, 'w') as f:
            json.dump(data_to_save, f, indent=4)

    def _load_or_initialize_data(self) -> VisitCounterData:
        """
        заполняет словарь данными из json файла если он существует,
        иначе инициализирует словарь
        """
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                data = json.load(f)
                data["unique_ips"] = {k: set(v) for k, v in data["unique_ips"].items()}

                return cast(VisitCounterData, data)
        return self._get_empty_data()
