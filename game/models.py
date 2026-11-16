"""Модуль с моделями игровых предметов."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Food:
    """Модель еды."""

    name: str
    satiety: int
    price: int

    def __repr__(self) -> str:
        """Возвращает строковое представление еды."""
        return (
            f"{self.name} стоимость: {self.price}, "
            f"утоляет голод на {self.satiety} единиц"
        )


@dataclass
class Medicine:
    """Модель лекарства с ограниченным количеством применений."""

    name: str
    price: int
    heal_hp: int
    number_of_uses: int
    uses: int = 0

    def use(self) -> int:
        """Увеличивает счётчик использований и возвращает величину лечения."""
        self.uses += 1
        return self.heal_hp

    def is_empty(self) -> bool:
        """Проверяет, исчерпано ли количество применений лекарства."""
        return self.uses >= self.number_of_uses

    def __repr__(self) -> str:
        """Возвращает строковое представление лекарства."""
        remaining = self.number_of_uses - self.uses
        return (
            f"{self.name} стоимость: {self.price}, лечит на "
            f"{self.heal_hp} HP, использований: "
            f"{remaining}/{self.number_of_uses}"
        )
