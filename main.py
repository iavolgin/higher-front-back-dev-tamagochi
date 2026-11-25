from game.clicker import RandomClicker
from game.exceptions import NotEnoughMoney, TamagochiIsGone
from game.game import AbstractGame, TamagochiGame
from game.models import Food, Medicine
from game.tamagochi import Tamagochi


def main() -> None:
    """Создаёт и запускает игру."""
    all_food = [
        Food(name='Бургер', satiety=20, price=40),
        Food(name='Салат', satiety=10, price=20),
        Food(name='Яблоко', satiety=10, price=15),
    ]

    all_medicine = [
        Medicine(name='Ибупрофен', price=30, heal_hp=20, number_of_uses=2),
    ]

    game = TamagochiGame(
        Tamagochi(),
        RandomClicker(),
        all_food=all_food,
        all_medicine=all_medicine,
    )
    try:
        run_game(game)
    except (EOFError, KeyboardInterrupt):
        print("\nВыход из игры.")


def run_game(game: AbstractGame) -> None:
    """Показывает состояние питомца и выполняет команды игрока."""
    actions = {
        "1": ("Пойти на работу", game.work),
        "2": ("Купить еду", game.buy_food),
        "3": ("Купить лекарство", game.buy_medicine),
        "4": ("Покормить", game.feed_tamagochi),
        "5": ("Вылечить", game.heal_tamagochi),
        "6": ("Играть", game.play_with_tamagochi),
        "7": ("Отдых", game.rest_tamagochi),
    }

    print("Добро пожаловать в Тамагочи-кликер!")

    while True:
        status = game.get_status()
        _show_status(game, status)
        if not status["is_alive"]:
            break

        for number, (label, _) in actions.items():
            print(f"{number}. {label}")
        print("0. Выход")

        choice = input("Выберите действие: ").strip()
        if choice == "0":
            return
        if choice not in actions:
            print("Неверная команда")
            continue

        _, action = actions[choice]
        try:
            income = action()
        except NotEnoughMoney as error:
            print(error)
            continue
        except TamagochiIsGone:
            break

        if income is not None:
            print(f"Вы заработали {income} монет")

    print("Питомец погиб. Игра окончена.")


def _show_status(game: AbstractGame, status: dict[str, int | bool]) -> None:
    """Показывает инвентарь и состояние питомца."""
    print(f"\nСумка с едой: {game.food}")
    print(f"Сумка с лекарствами: {game.medicine}")
    print(
        f"\nСтатус: голод {status['hunger']}, "
        f"усталость {status['fatigue']}, здоровье {status['hp']}, "
        f"энергия {status['energy']}, монет {status['coins']}\n"
    )
    if status["is_alive"] and status["is_sick"]:
        print("=======Тамагочи болеет======")
        print("=======Отдых действует менее эффективно=======")


if __name__ == "__main__":
    main()
