"""Исключения игры."""


class GameError(Exception):
    """Базовое исключение для ошибок игровой логики."""


class TamagochiIsGone(GameError):
    """Возникает при попытке взаимодействовать с погибшим питомцем."""


class NotEnoughMoney(GameError):
    """Возникает при недостатке монет для покупки."""
    
