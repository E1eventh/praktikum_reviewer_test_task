import datetime as dt


class Record:
    # Предпочтительнее использовать в значении по умолчанию None в случаях, когда
    # нужна дополнительная обработка такого аргумента.
    # Пример исправлений:
    # def __init__(self, amount, comment, date=None):
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        # При использовании многострочных выражений лучше отделять
        # отдельными строками разные логические части для наглядности
        # Пример исправлений:
        # self.date = (
        #     dt.datetime.now().date() if not date
        #     else dt.datetime.strptime(date, '%d.%m.%Y').date()
        # )
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        # Однородные операции рекомендуется писать в одном логическом блоке.
        # В данном случае у self.amount и self.comment идёт только присваивание
        # аргументов, когда у self.date - логическая обработка. Поэтому лучше
        # их писать вместе.
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # В цикле for имя, идущее после ключевого слово "for" и перед "in" -
        # это объявляемая переменная. В данном случае мы имеем конфликт имён
        # так как в коде уже находится класс с именем Record. Не рекомендуется
        # присваивать разным логическим единицам одинаковые имена во избежании
        # конфликтов и скрытых ошибок. Если имя конфликтует с зарезервированным,
        # то можно добавить нижнее подчёркивание после (например, если требуется,
        # можно создать переменную с именем "class_", которая не будет
        # конфликтовать с зарезервированным именем "class"). Так как Python
        # чувствителен к регистру, в данном случае в цикле можно переименовать
        # "Record" в "record".
        # Пример исправлений:
        # for record in self.records:
        #     if record.date == dt.datetime.now().date():
        #         today_stats = today_stats + record.amount
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                # Помимо отсутствия единообразия с остальным кодом (например,
                # на строке 77 используется другой подход к подобной операции),
                # в подобной записи есть ненужное повторение переменной,
                # которое можно избежать с помощью расширенного присваивания.
                # Пример исправлений:
                # today_stats += Record.amount
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            # Для большей лаконичности и читаемости можно подобные конструкции
            # заменять на цепочки сравнений. Например, 0 < a < 20 эквивалентно
            # 0 < a and a < 20 или a > 0 and a < 20
            # Пример исправлений:
            # if 0 <= (today - record.date).days < 7:
            # Так же, возможно, будет логичнее найти один раз дату, которая
            # была 7 дней назад, и проверять для каждой записи, была ли
            # эта запись сделана за последние 7 дней. В этом случае
            # будет меньше математических операций. Однако я бы рекомендовал
            # замерить быстродействие этих двух способов перед выбором.
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        if x > 0:
            # В требованиях к коду указано, что: "Бэкслеши для переносов
            # не применяются.". Так же отсутствует единообразие кода
            # (например, 18 строка). Так же на следующей строке используется
            # префикс "f", но никакого форматирования в ней не происходит.
            # Пример исправлений:
            # return (
            #     'Сегодня можно съесть что-нибудь'
            #     f' ещё, но с общей калорийностью не более {x} кКал'
            # )
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            # Для ключевого слова return не нужны круглые скобки, так как
            # return является statement'ом, а не функцией. Правильнее будет
            # писать без них
            # Пример исправлений:
            # return 'Хватит есть!'
            return('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # Во-первых, имя аргумента следует писать lowercase'ом.
    # Во-вторых, избыточное присваивание аргументов USD_RATE и EURO_RATE,
    # так как к ним можно обратиться по ключевому слову "self", потому что
    # они уже объявлены в классе (например, self.USD_RATE).
    # В-третьих, по заданию метод принимает только один аргумент - currency
    # В-четвёртых, нецелесообразно каждый раз передать вручную курс валют.
    # Куда логичнее было бы их запрашивать через API (например, сайт
    # free.currencyconverterapi.com имеет API для курсов валют, которые
    # можно запрашивать с помощью библиотеки requests).
    # Пример исправлений:
    # def get_today_cash_remained(self, currency):
    #     ...
    #     url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    #     if currency == 'usd':
    #         usd_rate = requests.get(url).json()['Valute']['USD']['Value']
    #         cash_remained /= usd_rate
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # Во-первых, в строке ошибка. Вместо операции присваивания ("=")
            # используется операция сравнения ("=="). Во-вторых, если
            # использовать операцию присваивания, то при передаче currency='rub'
            # остаток денег всегда будет равняться 1.00. Поэтому эта строка
            # не нужна.
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        # Избыточная проверка. Исходя из условий выше можно заменить на
        # else:
        elif cash_remained < 0:
            # Нет единообразия с остальной частью кода. Выше применяются
            # f-строки (например, строка 148), поэтому логичнее сохранить
            # единый стиль кода и продолжать использовать f-строки. Так же
            # в требованиях к коду указано, что: "Бэкслеши для переносов
            # не применяются.", поэтому лучше заменить на выражение в
            # круглых скобках
            # Пример исправлений:
            # return (
            #     'Денег нет, держись:'
            #     f' твой долг - {-cash_remained:.2f} {currency_type}'
            # )
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    # Избыточная запись. Так как класс CaloriesCalculator наследуется от
    # класса Calculator, в котором уже объявлен метод get_week_stats,
    # то при попытке вызвать этот метод у экземпляра текущего класса
    # вызовется метод класса Calculator.
    def get_week_stats(self):
        super().get_week_stats()
