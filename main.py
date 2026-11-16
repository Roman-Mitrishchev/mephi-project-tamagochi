"""Точка входа в консольную игру."""

from game.constants import STATUS_TEMPLATE

from game.clicker import SimpleRandomClicker
from game.exceptions import GameError
from game.game import SimpleGame
from game.models import Food, Medicine
from game.tamagochi import SimpleTamagochi


def main() -> None:
    """Создаёт игровые объекты и запускает игровой цикл."""
    all_food = [
        Food(name="Бургер", satiety=20, price=40),
        Food(name="Салат", satiety=10, price=20),
        Food(name="Яблоко", satiety=10, price=15),
    ]
    all_medicine = [
        Medicine(
            name="Ибупрофен",
            price=30,
            heal_hp=20,
            number_of_uses=2,
        )
    ]

    tamagochi = SimpleTamagochi()
    clicker = SimpleRandomClicker(10, 20)
    game = SimpleGame(
        tamagochi,
        clicker,
        all_food=all_food,
        all_medicine=all_medicine,
    )

    print(f"Добро пожаловать! Ваш питомец — {tamagochi.name}.")
    actions = {
        "1": ("Работа", game.work),
        "2": ("Купить еду", game.buy_food),
        "3": ("Купить лекарство", game.buy_medicine),
        "4": ("Покормить", game.feed_tamagochi),
        "5": ("Вылечить", game.heal_tamagochi),
        "6": ("Играть", game.play_with_tamagochi),
        "7": ("Отдых", game.rest_tamagochi),
    }

    while tamagochi.is_alive():
        print(f"\nСумка с едой: {game.food}")
        print(f"Сумка с лекарствами: {game.medicine}")
        print(STATUS_TEMPLATE.format(**game.get_status()))
        if tamagochi.is_sick():
            print("Питомец болеет. Отдых менее эффективен.")
        for key, (label, _) in actions.items():
            print(f"{key}. {label}")
        print("0. Выход")

        choice = input("Выберите действие: ").strip()
        if choice == "0":
            print("Вы завершили игру.")
            break
        if choice not in actions:
            print("Неверная команда.")
            continue

        try:
            result = actions[choice][1]()
            if choice == "1":
                print(f"Вы заработали {result} монет.")
            else:
                print(f"Действие выполнено: {actions[choice][0].lower()}.")
        except GameError as error:
            print(error)


if __name__ == "__main__":
    main()
