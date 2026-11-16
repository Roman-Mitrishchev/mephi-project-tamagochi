"""Модуль пользовательских исключений игры."""


class TamagochiIsGone(Exception):
    """Возникает при попытке взаимодействовать с погибшим питомцем."""


class NotEnoughMoney(Exception):
    """Возникает при недостатке монет для покупки."""


class InvalidAction(Exception):
    """Возникает при невозможности выполнить игровое действие."""


class GameError(Exception):
    """Базовое исключение для ошибок игровой логики."""


class TamagochiIsGone(GameError):
    """Питомец погиб."""


class NotEnoughMoney(GameError):
    """Не хватает монет для покупки."""
    
