"""Модуль с интерфейсом и реализациями класса тамагочи"""

from abc import ABC, abstractmethod

from .exceptions import TamagochiIsGone
from .models import Food, Medicine


class AbstractTamagochi(ABC):
    """Интерфейс логики тамагочи"""

    @abstractmethod
    def feed(self, food: Food) -> None:
        """
        Абстрактный метод для кормления тамагочи

        :param food: объект еды для кормления
        """
        raise NotImplementedError

    @abstractmethod
    def play(self) -> None:
        """Абстрактный метод для игры с тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def rest(self) -> None:
        """Абстрактный метод для отдыха тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def heal(self, medicine: Medicine) -> None:
        """
        Абстрактный метод для лечения тамагочи

        :param medicine: лекарство для лечения
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def status(self) -> dict[str, int]:
        """
        Абстрактное свойство для доступа ко всем состояниям тамагочи

        :return: словарь со всеми состояниями тамагочи
        """
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """
        Абстрактный метод для проверки жив ли тамагочи

        :return: True если жив, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def is_sick(self) -> bool:
        """
        Абстрактный метод для проверки, не заболел ли тамагочи

        :return: True если тамагочи болеет, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        """
        Абстрактный метод для обновления состояний тамагочи.
        Должен использоваться после каждого взаимодействия с тамагочи
        """
        raise NotImplementedError


class Tamagochi(AbstractTamagochi):
    """Питомец, состояние которого меняется за каждый игровой ход."""

    _MAX_STAT = 100
    _SICKNESS_THRESHOLD = 70

    def __init__(self) -> None:
        """Создаёт сытого, здорового и отдохнувшего питомца."""
        self._hunger = 0
        self._fatigue = 0
        self._hp = self._MAX_STAT
        self._energy = self._MAX_STAT

    def feed(self, food: Food) -> None:
        """Уменьшает голод питомца."""
        self._ensure_alive()
        self._hunger = max(0, self._hunger - food.satiety)

    def play(self) -> None:
        """Повышает голод и усталость, расходует энергию."""
        self._ensure_alive()
        self._hunger = min(self._MAX_STAT, self._hunger + 5)
        self._fatigue = min(self._MAX_STAT, self._fatigue + 10)
        self._energy = max(0, self._energy - 15)

    def rest(self) -> None:
        """Снижает усталость и восстанавливает энергию."""
        self._ensure_alive()
        rest_divisor = 2 if self.is_sick() else 1
        self._fatigue = max(0, self._fatigue - 20 // rest_divisor)
        self._energy = min(self._MAX_STAT, self._energy + 26 // rest_divisor)

    def heal(self, medicine: Medicine) -> None:
        """Восстанавливает здоровье питомца."""
        self._ensure_alive()
        self._hp = min(self._MAX_STAT, self._hp + medicine.heal_hp)

    @property
    def status(self) -> dict[str, int]:
        """Возвращает снимок голода, усталости, здоровья и энергии."""
        return {
            "hunger": self._hunger,
            "fatigue": self._fatigue,
            "hp": self._hp,
            "energy": self._energy,
        }

    def is_alive(self) -> bool:
        """Проверяет, жив ли питомец."""
        return self._hp >= 0

    def is_sick(self) -> bool:
        """Проверяет, болен ли питомец."""
        return max(self._hunger, self._fatigue) >= self._SICKNESS_THRESHOLD

    def update(self) -> None:
        """Обновляет состояние питомца за ход."""
        self._ensure_alive()
        self._hunger = min(self._MAX_STAT, self._hunger + 3)
        self._fatigue = min(self._MAX_STAT, self._fatigue + 3)
        self._energy = max(0, self._energy - 2)
        if self.is_sick():
            self._hp -= 10
            self._fatigue = min(self._MAX_STAT, self._fatigue + 4)

    def _ensure_alive(self) -> None:
        """Прерывает действие, если питомец погиб."""
        if not self.is_alive():
            raise TamagochiIsGone("Здоровье питомца упало ниже нуля")
