"""Модуль с логикой управления игрой."""

from abc import ABC, abstractmethod
from copy import copy
from typing import Any

from .clicker import AbstractClicker
from .constants import STARTING_COINS
from .exceptions import (
    InvalidAction,
    NotEnoughItems,
    NotEnoughMoney,
)
from .models import Food, Medicine
from .tamagochi import AbstractTamagochi


class AbstractGame(ABC):
    """Интерфейс игровой сущности."""

    @abstractmethod
    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine],
    ) -> None:
        """Инициализирует игру и её ресурсы."""
        raise NotImplementedError

    @abstractmethod
    def work(self) -> int:
        """Выполняет работу и возвращает заработанные монеты."""
        raise NotImplementedError

    @abstractmethod
    def buy_food(self) -> None:
        """Покупает выбранную еду."""
        raise NotImplementedError

    @abstractmethod
    def buy_medicine(self) -> None:
        """Покупает лекарство."""
        raise NotImplementedError

    @abstractmethod
    def feed_tamagochi(self) -> None:
        """Кормит питомца."""
        raise NotImplementedError

    @abstractmethod
    def heal_tamagochi(self) -> None:
        """Лечит питомца."""
        raise NotImplementedError

    @abstractmethod
    def rest_tamagochi(self) -> None:
        """Отправляет питомца отдыхать."""
        raise NotImplementedError

    @abstractmethod
    def play_with_tamagochi(self) -> None:
        """Играет с питомцем."""
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """Возвращает состояние игры."""
        raise NotImplementedError

    @property
    @abstractmethod
    def food(self) -> list[Food]:
        """Возвращает инвентарь еды."""
        raise NotImplementedError

    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        """Возвращает инвентарь лекарств."""
        raise NotImplementedError


class SimpleGame(AbstractGame):
    """Управляет экономикой, инвентарём и действиями игрока."""

    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine],
    ) -> None:
        """Создаёт игру с питомцем, кликером и каталогом предметов.

        Args:
            tamagochi: Экземпляр питомца.
            clicker: Экземпляр кликера.
            all_food: Каталог доступной еды.
            all_medicine: Каталог доступных лекарств.
        """
        self._tamagochi = tamagochi
        self._clicker = clicker
        self._all_food = list(all_food)
        self._all_medicine = list(all_medicine)
        self._food: list[Food] = []
        self._medicine: list[Medicine] = []
        self._coins = STARTING_COINS

    @property
    def food(self) -> list[Food]:
        """Возвращает копию сумки с едой."""
        return list(self._food)

    @property
    def medicine(self) -> list[Medicine]:
        """Возвращает копию сумки с лекарствами."""
        return list(self._medicine)

    def _choose_item(self, items: list[Any], item_type: str) -> int:
        """Запрашивает у пользователя номер предмета.

        Args:
            items: Список доступных предметов.
            item_type: Название типа предметов.

        Returns:
            Индекс выбранного предмета.

        Raises:
            NotEnoughItems: Если предметов нет.
            InvalidAction: Если введён некорректный номер.
        """
        if not items:
            raise NotEnoughItems(f"Нет доступных предметов: {item_type}.")
        for number, item in enumerate(items, start=1):
            print(f"{number}. {item}")
        try:
            index = int(input(f"Выберите {item_type}: ")) - 1
        except ValueError as error:
            raise InvalidAction("Нужно ввести номер предмета.") from error
        if index < 0 or index >= len(items):
            raise InvalidAction("Предмет с таким номером отсутствует.")
        return index

    def work(self) -> int:
        """Начисляет доход кликера и обновляет состояние питомца.

        Returns:
            Количество заработанных монет.
        """
        self._clicker.click()
        income = self._clicker.income_per_click
        self._coins += income
        self._tamagochi.update()
        return income

    def buy_food(self) -> None:
        """Покупает выбранный продукт из каталога еды."""
        index = self._choose_item(self._all_food, "еду")
        item = self._all_food[index]
        if self._coins < item.price:
            raise NotEnoughMoney("Недостаточно монет для покупки еды.")
        self._coins -= item.price
        self._food.append(item)

    def buy_medicine(self) -> None:
        """Покупает выбранное лекарство из каталога."""
        index = self._choose_item(self._all_medicine, "лекарство")
        item = self._all_medicine[index]
        if self._coins < item.price:
            raise NotEnoughMoney("Недостаточно монет для покупки лекарства.")
        self._coins -= item.price
        self._medicine.append(copy(item))

    def feed_tamagochi(self) -> None:
        """Использует выбранную еду из инвентаря."""
        index = self._choose_item(self._food, "еду из сумки")
        item = self._food[index]
        self._tamagochi.feed(item)
        self._food.pop(index)

    def heal_tamagochi(self) -> None:
        """Использует выбранное лекарство из инвентаря."""
        index = self._choose_item(self._medicine, "лекарство")
        item = self._medicine[index]
        self._tamagochi.heal(item)
        if item.is_empty():
            self._medicine.pop(index)

    def rest_tamagochi(self) -> None:
        """Обновляет состояние питомца после отдыха."""
        self._tamagochi.rest()

    def play_with_tamagochi(self) -> None:
        """Обновляет состояние питомца после игры."""
        self._tamagochi.play()

    def get_status(self) -> dict[str, Any]:
        """Возвращает показатели питомца и количество монет."""
        status: dict[str, Any] = self._tamagochi.status.copy()
        status["coins"] = self._coins
        status["alive"] = self._tamagochi.is_alive()
        status["is_sick"] = self._tamagochi.is_sick()
        return status
