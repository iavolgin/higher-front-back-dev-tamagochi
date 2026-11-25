"""Модуль с интерфейсом и реализацией класса игры"""

from abc import ABC, abstractmethod
from dataclasses import replace

from .clicker import AbstractClicker
from .exceptions import NotEnoughMoney, TamagochiIsGone
from .models import Food, Medicine
from .tamagochi import AbstractTamagochi


class AbstractGame(ABC):
    """Интерфейс для логики игры"""

    @abstractmethod
    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine],
    ) -> None:
        """
        Абстрактный метод инициализации класса игры

        :param tamagochi: экземпляр тамагочи
        :param clicker: экземпляр кликера
        :param all_food: все доступные варианты еды
        :param all_medicine: все доступные варианты лекарств
        """
        raise NotImplementedError

    @abstractmethod
    def work(self) -> int:
        """
        Абстрактный метод для логики действия "работа

        :return: количество заработанных монет
        """
        raise NotImplementedError

    @abstractmethod
    def buy_food(self) -> None:
        """Абстрактный метод для покупки еды"""
        raise NotImplementedError

    @abstractmethod
    def buy_medicine(self) -> None:
        """Абстрактный метод для покупки лекарства"""
        raise NotImplementedError

    @abstractmethod
    def feed_tamagochi(self) -> None:
        """Абстрактный метод для кормления тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def heal_tamagochi(self) -> None:
        """Абстрактный метод для лечения тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def rest_tamagochi(self) -> None:
        """Абстрактный метод для отдыха тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def play_with_tamagochi(self) -> None:
        """Абстрактный метод для игры с тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> dict[str, int | bool]:
        """
        Абстрактный метод для получения статуса (всех характеристик) тамагочи

        :return: словарь со всеми характеристиками тамагочи
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def food(self) -> list[Food]:
        """
        Абстрактное свойство для доступа к сумке с едой

        :return: список с имеющимися (купленными) объектами еды
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        """
        Абстрактное свойство для доступа к сумке с лекарствами

        :return: список с имеющимися (купленными) объектами лекарств
        """
        raise NotImplementedError


class TamagochiGame(AbstractGame):
    """Управляет ходами, магазином и инвентарём."""

    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine],
    ) -> None:
        """Создаёт игру с пустым инвентарём."""
        self._tamagochi = tamagochi
        self._clicker = clicker
        self._all_food = all_food.copy()
        self._all_medicine = all_medicine.copy()
        self._coins = 0
        self._food: list[Food] = []
        self._medicine: list[Medicine] = []

    def work(self) -> int:
        """Начисляет монеты и возвращает заработок."""
        self._ensure_alive()
        self._clicker.click()
        income = self._clicker.income_per_click
        self._coins += income
        self._tamagochi.update()
        return income

    def buy_food(self) -> None:
        """Покупает выбранную порцию еды."""
        self._ensure_alive()
        index = self._choose_index(self._all_food)
        if index is None:
            return

        food = self._all_food[index]
        self._pay(food.price)
        self._food.append(food)
        self._tamagochi.update()

    def buy_medicine(self) -> None:
        """Покупает отдельную упаковку выбранного лекарства."""
        self._ensure_alive()
        index = self._choose_index(self._all_medicine)
        if index is None:
            return

        medicine = replace(self._all_medicine[index], uses=0)
        if medicine.is_empty():
            print("В упаковке пусто.")
            return

        self._pay(medicine.price)
        self._medicine.append(medicine)
        self._tamagochi.update()

    def feed_tamagochi(self) -> None:
        """Кормит питомца выбранной порцией."""
        self._ensure_alive()
        index = self._choose_index(self._food)
        if index is None:
            return

        self._tamagochi.feed(self._food[index])
        self._food.pop(index)
        self._tamagochi.update()

    def heal_tamagochi(self) -> None:
        """Лечит питомца одной дозой лекарства."""
        self._ensure_alive()
        index = self._choose_index(self._medicine)
        if index is None:
            return

        medicine = self._medicine[index]
        self._tamagochi.heal(medicine)
        medicine.uses += 1
        if medicine.is_empty():
            self._medicine.pop(index)
        self._tamagochi.update()

    def rest_tamagochi(self) -> None:
        """Даёт питомцу отдохнуть."""
        self._ensure_alive()
        self._tamagochi.rest()
        self._tamagochi.update()

    def play_with_tamagochi(self) -> None:
        """Играет с питомцем."""
        self._ensure_alive()
        self._tamagochi.play()
        self._tamagochi.update()

    def get_status(self) -> dict[str, int | bool]:
        """Возвращает показатели питомца и баланс."""
        return {
            **self._tamagochi.status,
            "coins": self._coins,
            "is_sick": self._tamagochi.is_sick(),
            "is_alive": self._tamagochi.is_alive(),
        }

    @property
    def food(self) -> list[Food]:
        """Возвращает купленную еду."""
        return self._food.copy()

    @property
    def medicine(self) -> list[Medicine]:
        """Возвращает купленные лекарства."""
        return [replace(medicine) for medicine in self._medicine]

    def _ensure_alive(self) -> None:
        """Прерывает действие, если питомец погиб."""
        if not self._tamagochi.is_alive():
            raise TamagochiIsGone("Здоровье питомца упало ниже нуля")

    def _pay(self, price: int) -> None:
        """Списывает стоимость покупки."""
        if self._coins < price:
            raise NotEnoughMoney("Не хватает монет для покупки.")
        self._coins -= price

    def _choose_index(
        self, items: list[Food] | list[Medicine]
    ) -> int | None:
        """Возвращает индекс выбранного предмета."""
        if not items:
            print("Нет доступных предметов.")
            return None

        for number, item in enumerate(items, start=1):
            print(f"{number}. {item}")

        try:
            number = int(input("Выберите номер или 0 для отмены: "))
        except ValueError:
            print("Введите целое число.")
            return None

        if number == 0:
            return None
        if 1 <= number <= len(items):
            return number - 1

        print("Неверный номер.")
        return None
