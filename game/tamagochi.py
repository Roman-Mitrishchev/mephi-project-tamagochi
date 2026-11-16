"""Модуль с логикой питомца."""

from abc import ABC, abstractmethod
from random import random

from .constants import (
    CRITICAL_ENERGY,
    CRITICAL_HUNGER,
    DEFAULT_TAMAGOCHI_NAME,
    ENERGY_DAMAGE,
    FEED_ENERGY_COST,
    HUNGER_DAMAGE,
    INITIAL_ACTIONS,
    INITIAL_ENERGY,
    INITIAL_FATIGUE,
    INITIAL_HP,
    INITIAL_HUNGER,
    INITIAL_SICK_STATE,
    MAX_STAT_VALUE,
    MIN_STAT_VALUE,
    PLAY_ENERGY_COST,
    PLAY_FATIGUE_INCREASE,
    PLAY_HUNGER_INCREASE,
    REST_HUNGER_INCREASE,
    REST_RECOVERY,
    SICK_REST_RECOVERY,
    SICKNESS_CHANCE,
    SICKNESS_DAMAGE,
    SICKNESS_FATIGUE_INCREASE,
    SICKNESS_HUNGER_THRESHOLD,
    UPDATE_ENERGY_DECREASE,
    UPDATE_FATIGUE_INCREASE,
    UPDATE_HUNGER_INCREASE,
)
from .exceptions import InvalidAction, TamagochiIsGone
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

    def __init__(self, name: str = DEFAULT_TAMAGOCHI_NAME) -> None:
        """Создаёт питомца с начальными характеристиками.

        Args:
            name: Имя питомца.
        """
        self._name = name
        self._hunger = INITIAL_HUNGER
        self._fatigue = INITIAL_FATIGUE
        self._hp = INITIAL_HP
        self._energy = INITIAL_ENERGY
        self._sick = INITIAL_SICK_STATE
        self._actions = INITIAL_ACTIONS

    @property
    def name(self) -> str:
        """Возвращает имя питомца."""
        return self._name

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
        if not self.is_alive():
            raise TamagochiIsGone("Питомец погиб. Игра окончена.")

    def _limit(self, value: int) -> int:
        """Ограничивает показатель допустимым диапазоном."""
        return max(MIN_STAT_VALUE, min(MAX_STAT_VALUE, value))

    def feed(self, food: Food) -> None:
        """Уменьшает голод и расходует часть энергии.

        Args:
            food: Еда, которой кормят питомца.
        """
        self._ensure_alive()
        self._hunger = self._limit(self._hunger - food.satiety)
        self._energy = self._limit(self._energy - FEED_ENERGY_COST)
        self.update()

    def play(self) -> None:
        """Уменьшает голод и энергию, повышает усталость."""
        self._ensure_alive()
        self._hunger = self._limit(self._hunger + PLAY_HUNGER_INCREASE)
        self._energy = self._limit(self._energy - PLAY_ENERGY_COST)
        self._fatigue = self._limit(self._fatigue + PLAY_FATIGUE_INCREASE)
        self.update()

    def rest(self) -> None:
        """Восстанавливает энергию и снижает усталость."""
        self._ensure_alive()
        recovery = REST_RECOVERY if not self._sick else SICK_REST_RECOVERY
        self._energy = self._limit(self._energy + recovery)
        self._fatigue = self._limit(self._fatigue - recovery)
        self._hunger = self._limit(self._hunger + REST_HUNGER_INCREASE)
        self.update()

    def heal(self, medicine: Medicine) -> None:
        """Восстанавливает здоровье и расходует одно применение лекарства.

        Args:
        medicine: Используемое лекарство.
        """
        self._ensure_alive()

        if medicine.is_empty():
            raise InvalidAction("Лекарство закончилось")

        self.update()
        self._ensure_alive()

        healing = medicine.use()
        self._hp = self._limit(self._hp + healing)
        self._sick = False

    def update(self) -> None:
        """Изменяет характеристики и проверяет вероятность заболевания."""
        self._ensure_alive()
        self._actions += 1
        self._hunger = self._limit(self._hunger + UPDATE_HUNGER_INCREASE)
        self._fatigue = self._limit(self._fatigue + UPDATE_FATIGUE_INCREASE)
        self._energy = self._limit(self._energy - UPDATE_ENERGY_DECREASE)
        if self._hunger >= CRITICAL_HUNGER:
            self._hp = self._limit(self._hp - HUNGER_DAMAGE)
        if self._energy <= CRITICAL_ENERGY:
            self._hp = self._limit(self._hp - ENERGY_DAMAGE)
        if self._sick:
            self._hp = self._limit(self._hp - SICKNESS_DAMAGE)
            self._fatigue = self._limit(
                self._fatigue + SICKNESS_FATIGUE_INCREASE
            )
        elif (
            self._hunger >= SICKNESS_HUNGER_THRESHOLD
            and random() < SICKNESS_CHANCE
        ):
            self._sick = True
