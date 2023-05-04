import json
from datetime import datetime

bank_file = 'operations.json'


def load_json(bank_file: str, encoding: str = 'utf-8') -> list:
    """Чтение JSON файла и возврат его содержимого в виде списка словарей.

    """
    try:
        with open(bank_file, 'r', encoding=encoding) as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON file {bank_file}")
        return []
    return data


def get_executed(bank_file: str) -> list:
    """Функция для вывода 5 последних операций по статусу EXECUTED
    """
    data = load_json(bank_file)
    executed = [item for item in data[::-1] if item.get("state") == "EXECUTED"][:5]
    return executed


def get_result(bank_file: str) -> str:
    """Функция для вывода операции на экран
    """
    recent_operations = get_executed(bank_file)
    recent_operations.sort(key=lambda x: x["date"], reverse=True)
    result = []
    for operation in recent_operations:
        transfer_date = operation["date"].split("T")[0]
        date = datetime.strptime(transfer_date, "%Y-%m-%d").strftime("%d.%m.%Y")
        description = operation["description"]
        where_from = hide_digit(operation.get("from"))
        destination = hide_digit(operation["to"])
        amount = operation["operationAmount"]["amount"]
        currency = operation["operationAmount"]["currency"]["name"]
        result.append(f"{date} {description}\n{where_from} -> {destination}\n{amount} {currency}\n")
    return "\n".join(result)


def hide_digit(account: str) -> str:
    """Функция для вывода счета и карты в скрытом формате
    """
    if not account:
        # Если переданный аргумент пустой, возвращаем пустую строку
        return f"{account}"
    account_parts = account.split(' ')
    if "Счет" in account_parts:
        return f"Счет **{account_parts[1][-4:]}"
    else:
        return f"{account_parts[0]} {account_parts[1][:4]} {account_parts[1][4:6]}** **** {account_parts[1][-4:]}"


if __name__ == '__main__':
    print(get_result(bank_file))
