import json
from datetime import datetime

bank_file = 'operations.json'


def load_json(bank_file, encoding='utf-8'):
    """
    Чтение JSON файла и возврат его содержимого в виде списка словарей.
    :param bank_file: Путь к JSON файлу.
    :param encoding: Кодировка файла (по умолчанию utf-8).
    :return: Список словарей, содержащих данные из файла.
    """
    try:
        with open(bank_file, 'r', encoding=encoding) as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON file {bank_file}")
        return []
    return data


def get_executed(bank_file):
    """
    Функция для вывода 5 последних операций по статусу EXECUTED

    """

    data = load_json(bank_file)
    executed = [item for item in data[::-1] if item.get("state") == "EXECUTED"][:5]
    return executed


def print_execute(bank_file):
    """
    Функция для вывода операции на экран
    :param bank_file:
    :return:
    """
    recent_operations = get_executed(bank_file)
    recent_operations.sort(key=lambda x: x["date"], reverse=True)
    for operation in recent_operations:
        transfer_date = operation["date"].split("T")[0]
        date = datetime.strptime(transfer_date, "%Y-%m-%d").strftime("%d.%m.%Y")
        description = operation["description"]
        where_from = hide_digit(operation.get("from"))
        destination = hide_digit(operation["to"])
        amount = operation["operationAmount"]["amount"]
        currency = operation["operationAmount"]["currency"]["name"]
        print(f"{date} {description}\n{where_from} -> {destination}\n{amount} {currency}\n")


def hide_digit(account: str) -> str:
    if not account:
        # Если переданный аргумент пустой, возвращаем пустую строку
        return f"{account}"
    account_parts = account.split(' ')
    if "Счет" in account_parts:
        return f"Счет **{account_parts[1][-4:]}"
    else:
        return f"{account_parts[0]} {account_parts[1][:4]} {account_parts[1][4:6]}** **** {account_parts[1][-4:]}"


print_execute(bank_file)
