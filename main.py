import datetime as dt

#При объявлении аргументов в инициализации функции(особенно, внутри классов) лучше указывать типы аргументов при помощи библиотеки typing
#Это поможет при разработке в команде и/или с большими проектами, где может быть очень много классов и функций

class Record:
    #Стандартное значение для параметра date лучше всего устанавливать None, поскольку пустая строка вызывает двусмысленность
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        #У кода ниже довольно низкая читаемость ее можно заменить на
        #if date is None:
        #    self.date = dt.datetime.now().date()
        #else:
        #    self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        #Для лучшей читаемости, однострочное присвоение лучше переносить в начало
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        #Имеет смысл делать проверку типа через assert и isinstance например
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        #Рекомендуется именовать переменные с маленькой буквы.
        #С большой буквы именуются названия классов. Пример корректного наименования ниже.
        #for record in self.records:
        for Record in self.records:
            #Тут, помимо рекомендации выше еще полезно было бы вынести dt.datetime.now().date() в переменную
            if Record.date == dt.datetime.now().date():
                #Тут стоит использовать оператор +=, чтобы получилось так today_stats += record.amount
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            if (
                #Тут лучше положить (today - record.date).days в переменную
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        if x > 0:
            #Лучше не использовать перенос со слешем
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            #Скобки тут лишние
            return('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.
    #Тут нет смысла передавать USD_RATE и EURO_RATE поскольку
    #имена аргументов внутри функции совпадают с переменными "снаружи"(определенными внутри данного класса),
    #поэтому лучше тогда их вызывать как self.USD_RATE внутри функции.

    #Для повышения мобильности этого функционала можно вынести получение курсов в отдельную сущность,
    #которая будет это хэндлить, например - в другую функцию внутри текущего класса,
    #которая выдает по типу из currency соответствующий курс
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        #Тут код выполняет две функции: конвертация валюты и расчет средств в остатке.
        #Первую функциональность лучше вынести в отдельную функцию,
        #чтобы данная функция не выполняла слишком много действий(которые еще и могут повторяться в будущем)
        currency_type = currency# Присвоение не имеет смысла, поскольку дальше эта переменная будет переписана другим значением
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd':
            cash_remained /= USD_RATE
            # лучше сохранять постоянство нотации типов валют, например используя ISO формат как тут
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            # лучше сохранять постоянство нотации типов валют(например EUR)
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # Скорее всего подразумевалось присвоение(которое не несет смысла), вместо него - сравнение
            cash_remained == 1.00
            # лучше сохранять постоянство нотации типов валют(например RUB)
            currency_type = 'руб'
        #Тут лучше сделать пробел между двумя логическими блоками инструкций
        if cash_remained > 0:
            #Округление тут следует провести вне ветвления(над if cash_remained > 0:)
            #Нет особого смысла разбивать строку надвое
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        #Эту ветвь лучше было вынести в конструкцию else ниже
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            #Тут следует избежать переноса через обратный слэш и использовать один метод форматирования строк(у метода f'' лучше читаемость)
            #Округление тут следует провести вне ветвления(над if cash_remained > 0:)
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    def get_week_stats(self):
        super().get_week_stats()
