from enum import Enum


class WeekDay(Enum):
    """
    Класс для получения дня недели по числу
    """

    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

    def __str__(self) -> str:
        """
        возвращает строковое представление дня недели
        """
        return self.name
