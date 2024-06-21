"""Скрипт для двух калькуляторов: для подсчёта денег и калорий."""
import datetime
from datetime import *


class Record:
    """Класс для хранения информации в формате записи."""

    def __init__(self, amount: int, comment: str,
                 date: str = str(datetime.today().strftime('%d.%m.%Y'))):
        self.amount = amount
        self.comment = comment
        self.date = datetime.strptime(date, '%d.%m.%Y')


class Calculator:
    """Родительский класс для калькуляторов каллорий и денег."""

    def __init__(self, limit: int):
        self.today = datetime.today().day  # Хранение текущей даты
        self.limit = limit  # Дневной лимит трат/ ккал.
        self.records = []  # Список для записей.
        self.today_stats = 0
        self.week_stats = {}

    def add_record(self, rec: Record):
        """Метод позволяет добавить новую запись в список records.
        Также, метод подсчитывает суточные и недельные траты."""

        if self.today != datetime.today().day:  # Хранение записей за неделю
            self.week_stats.pop(abs(self.today) - 7)
            self.today = datetime.today().day

        self.records.append(rec)  # Добавление записи в список

        if abs((date.today().day - rec.date.day)) <= 7:  # Недельные записи
            self.week_stats.setdefault(rec.date.day, 0)
            self.week_stats[rec.date.day] += rec.amount

        self.today_stats = self.week_stats[self.today]  # Суточное значение

    def get_today_stats(self):
        """Метод возвращает суточное значение."""
        return self.week_stats[self.today]

    def get_week_stats(self):
        """Метод возвращает недельное значение."""
        return sum(self.week_stats.values())


class CaloriesCalculator(Calculator):
    """Класс: калькулятор каллорий. Наследует все методы класса Calculator
    и обладает методом get_calories_remained."""

    def get_calories_remained(self):
        if self.today_stats < self.limit:
            return (f"Сегодня можно съесть что-нибудь ещё, но с общей"
                    f" калорийностью не более "
                    f"{self.limit - self.today_stats} кКал")
        else:
            return f"Хватит есть!"


class CashCalculator(Calculator):
    """Класс: денежный калькулятор. Наследует все методы класса Calculator
    и обладает методом get_today_cash_remained."""

    USD_RATE, EURO_RATE = 89, 95

    def get_today_cash_remained(self, currency: str):
        encod = {'rub': (1, 'руб'), 'usd': (CashCalculator.USD_RATE, 'USD'),
                 'eur': (CashCalculator.EURO_RATE, 'Euro')}
        if self.today_stats < self.limit:
            return (f"На сегодня осталось "
                    f"{(self.limit - self.today_stats) * encod[currency][0]}"
                    f" {encod[currency][1]}")
        elif self.today_stats == self.limit:
            return f"Денег нет, держиcь."
        else:
            return (f"Денег нет, держись: твой долг "
                    f"- {(self.today_stats - self.limit) * encod[currency][0]}"
                    f" {encod[currency][1]}")
