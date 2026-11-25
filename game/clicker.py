"""Модуль с интерфейсом и реализацией кликера"""

from abc import ABC, abstractmethod
from random import randint


class AbstractClicker(ABC):
    """Интерфейс для кликера"""

    @abstractmethod
    def __init__(self) -> None:
        """Абстрактный метод инициализации"""
        raise NotImplementedError

    @abstractmethod
    def click(self) -> None:
        """Абстрактный метод клика для накапливания монет"""
        raise NotImplementedError

    @property
    @abstractmethod
    def income_per_click(self) -> int:
        """Абстрактное свойство для доступа к количеству монет за клик"""
        raise NotImplementedError


class RandomClicker(AbstractClicker):
    """Кликер со случайным доходом за клик."""

    def __init__(self, min_income: int = 10, max_income: int = 20) -> None:
        """Задаёт диапазон дохода за клик."""
        self._min_income = min_income
        self._max_income = max_income
        self._income_per_click = 0

    def click(self) -> None:
        """Выбирает случайный доход за клик."""
        self._income_per_click = randint(self._min_income, self._max_income)

    @property
    def income_per_click(self) -> int:
        """Возвращает доход за последний клик."""
        return self._income_per_click
