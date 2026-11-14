"""Модуль с реализацией игрового кликера."""

from abc import ABC, abstractmethod
from random import randint


class AbstractClicker(ABC):
    """Интерфейс кликера."""

    @abstractmethod
    def __init__(self) -> None:
        """Инициализирует кликер."""
        raise NotImplementedError

    @abstractmethod
    def click(self) -> None:
        """Выполняет клик и начисляет игровой доход."""
        raise NotImplementedError

    @property
    @abstractmethod
    def income_per_click(self) -> int:
        """Возвращает доход за последний клик."""
        raise NotImplementedError


class SimpleRandomClicker(AbstractClicker):
    """Кликер со случайным доходом в заданном диапазоне."""

    def __init__(self, min_income: int, max_income: int) -> None:
        """Создаёт кликер с минимальным и максимальным доходом.

        Args:
            min_income: Минимальное количество монет за клик.
            max_income: Максимальное количество монет за клик.

        Raises:
            ValueError: Если диапазон дохода задан некорректно.
        """
        if min_income < 0 or max_income < min_income:
            raise ValueError("Некорректный диапазон дохода.")
        self._min_income = min_income
        self._max_income = max_income
        self._income_per_click = 0

    @property
    def income_per_click(self) -> int:
        """Возвращает доход, полученный при последнем клике."""
        return self._income_per_click

    def click(self) -> None:
        """Случайным образом определяет доход за один клик."""
        self._income_per_click = randint(
            self._min_income,
            self._max_income,
        )
