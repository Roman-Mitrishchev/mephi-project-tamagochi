"""Исключения игры."""


class GameError(Exception):
    """Базовое исключение для ошибок игровой логики."""


class TamagochiIsGone(GameError):
    """Возникает при попытке взаимодействовать с погибшим питомцем."""


class NotEnoughMoney(GameError):
    """Возникает при недостатке монет для покупки."""


class InvalidAction(GameError):
    """Возникает при попытке выполнить недопустимое действие."""
    

class NotEnoughItems(GameError):
    """Возникает при попытке использовать предмет, которого нет в инвентаре."""
    
