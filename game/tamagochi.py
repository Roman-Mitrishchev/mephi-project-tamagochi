"""Модуль с логикой питомца."""

from abc import ABC, abstractmethod
from random import random

from .models import Food, Medicine


class AbstractTamagochi(ABC):
    """Интерфейс логики питомца."""

    @abstractmethod
    def feed(self, food: Food) -> None:
        """Кормит питомца выбранной едой."""
        raise NotImplementedError

    @abstractmethod
    def play(self) -> None:
        """Играет с питомцем."""
        raise NotImplementedError

    @abstractmethod
    def rest(self) -> None:
        """Восстанавливает силы питомца."""
        raise NotImplementedError

    @abstractmethod
    def heal(self, medicine: Medicine) -> None:
        """Лечит питомца выбранным лекарством."""
        raise NotImplementedError

    @property
    @abstractmethod
    def status(self) -> dict[str, int]:
        """Возвращает текущие показатели питомца."""
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """Проверяет, жив ли питомец."""
        raise NotImplementedError

    @abstractmethod
    def is_sick(self) -> bool:
        """Проверяет, болен ли питомец."""
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        """Обновляет состояние питомца после игрового действия."""
        raise NotImplementedError


class SimpleTamagochi(AbstractTamagochi):
    """Питомец с показателями голода, здоровья, энергии и усталости."""

    MAX_VALUE = 100
    MIN_VALUE = 0

    def __init__(self, name: str = "Бублик") -> None:
        """Создаёт питомца с начальными характеристиками.

        Args:
            name: Имя питомца.
        """
        self.name = name
        self._hunger = 20
        self._fatigue = 10
        self._hp = 100
        self._energy = 90
        self._sick = False
        self._actions = 0

    @property
    def status(self) -> dict[str, int]:
        """Возвращает копию словаря с характеристиками питомца."""
        return {
            "hunger": self._hunger,
            "fatigue": self._fatigue,
            "hp": self._hp,
            "energy": self._energy,
        }

    def is_alive(self) -> bool:
        """Возвращает True, если здоровье питомца выше нуля."""
        return self._hp > 0

    def is_sick(self) -> bool:
        """Возвращает текущее состояние здоровья питомца."""
        return self._sick

    def _ensure_alive(self) -> None:
        """Проверяет, можно ли продолжать взаимодействие с питомцем."""
        from .exceptions import TamagochiIsGone

        if not self.is_alive():
            raise TamagochiIsGone("Питомец погиб. Игра окончена.")

    def _limit(self, value: int) -> int:
        """Ограничивает показатель допустимым диапазоном."""
        return max(self.MIN_VALUE, min(self.MAX_VALUE, value))

    def feed(self, food: Food) -> None:
        """Уменьшает голод и расходует часть энергии.

        Args:
            food: Еда, которой кормят питомца.
        """
        self._ensure_alive()
        self._hunger = self._limit(self._hunger - food.satiety)
        self._energy = self._limit(self._energy - 5)
        self.update()

    def play(self) -> None:
        """Уменьшает голод и энергию, повышает усталость."""
        self._ensure_alive()
        self._hunger = self._limit(self._hunger + 10)
        self._energy = self._limit(self._energy - 15)
        self._fatigue = self._limit(self._fatigue + 15)
        self.update()

    def rest(self) -> None:
        """Восстанавливает энергию и снижает усталость."""
        self._ensure_alive()
        recovery = 25 if not self._sick else 10
        self._energy = self._limit(self._energy + recovery)
        self._fatigue = self._limit(self._fatigue - recovery)
        self._hunger = self._limit(self._hunger + 5)
        self.update()

    def heal(self, medicine: Medicine) -> None:
        """Восстанавливает здоровье и расходует одно применение лекарства.

        Args:
            medicine: Используемое лекарство.
        """
        self._ensure_alive()
        if medicine.is_empty():
            from .exceptions import NotEnoughItems

            raise NotEnoughItems("Лекарство закончилось.")
        self._hp = self._limit(self._hp + medicine.heal_hp)
        medicine.uses += 1
        self._sick = False
        self.update()

    def update(self) -> None:
        """Изменяет характеристики и проверяет вероятность заболевания."""
        if not self.is_alive():
            return
        self._actions += 1
        self._hunger = self._limit(self._hunger + 3)
        self._fatigue = self._limit(self._fatigue + 2)
        self._energy = self._limit(self._energy - 2)
        if self._hunger >= 90:
            self._hp = self._limit(self._hp - 5)
        if self._energy <= 10:
            self._hp = self._limit(self._hp - 3)
        if self._sick:
            self._hp = self._limit(self._hp - 2)
            self._fatigue = self._limit(self._fatigue + 5)
        elif self._hunger >= 70 and random() < 0.15:
            self._sick = True
