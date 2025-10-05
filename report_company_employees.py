import urllib.request
import csv
from collections import defaultdict

CORP_SUMMARY = []


def load_csv_to_global():
    """
    Функция загружает CSV-файл по URL и сохраняет его в глобальную переменную CORP_SUMMARY.
    """
    global CORP_SUMMARY
    url = "https://raw.githubusercontent.com/masaevke/report_company_employees/main/Corp_Summary.csv"
    response = urllib.request.urlopen(url)
    CORP_SUMMARY = [line.decode("utf-8") for line in response.readlines()]


def show_hierarchy():
    """
    Выводит иерархию.
    1. парсит CORP_SUMMARY с учетом utf-8.
    2. циклом собирает Департаменты и Команды в словарь где Ключ - Департамент, Значение - Команда.
    3. использует только встроенные модули Python.
    4. из сортированного словаря печатает по строчно в цикле иерархию
    """
    reader = csv.DictReader(CORP_SUMMARY, delimiter=";")

    hierarchy = defaultdict(set)
    for row in reader:
        dept = row["Департамент"]
        team = row["Отдел"]
        hierarchy[dept].add(team)

    print("Иерархия:")
    print("-" * 40)
    for dept in sorted(hierarchy.keys()):
        print(f"Департамент: {dept}")
        for team in sorted(hierarchy[dept]):
            print(f"  - Команда: {team}")
        print()


def report():
    """
    Выводит сводный отчёт по департаментам:
     - название
     - численность
     - вилка зарплат (мин – макс)
     - средняя зарплата
    """
    reader = csv.DictReader(CORP_SUMMARY, delimiter=";")

    dept_salaries = defaultdict(list)

    for row in reader:
        dept = row["Департамент"]
        salary = int(row["Оклад"])
        dept_salaries[dept].append(salary)

    print("Сводный отчёт по департаментам:")
    print("-" * 60)
    for dept in sorted(dept_salaries.keys()):
        salaries = dept_salaries[dept]
        count = len(salaries)
        min_sal = min(salaries)
        max_sal = max(salaries)
        avg_sal = sum(salaries) / len(salaries)

        print(f"Департамент: {dept}")
        print(f"  Численность: {count}")
        print(f"  Вилка зарплат: {min_sal} – {max_sal}")
        print(f"  Средняя зарплата: {avg_sal:.2f}")
        print()


def download(filename: str = "report_company_employees.csv"):
    """
    Функция создаёт сводный отчёт по департаментам и сохраняет его в CSV-файл.
    Использует данные из глобальной переменной CORP_SUMMARY.
    """
    reader = csv.DictReader(CORP_SUMMARY, delimiter=";")

    dept_salaries = defaultdict(list)

    for row in reader:
        dept = row["Департамент"]
        salary = int(row["Оклад"])
        dept_salaries[dept].append(salary)

    rows = []
    for dept in sorted(dept_salaries.keys()):
        salaries = dept_salaries[dept]
        count = len(salaries)
        min_sal = min(salaries)
        max_sal = max(salaries)
        avg_sal = round(sum(salaries) / len(salaries), 2)

        rows.append(
            {
                "Департамент": dept,
                "Численность": count,
                "Мин. зарплата": min_sal,
                "Макс. зарплата": max_sal,
                "Средняя зарплата": avg_sal,
            }
        )

    with open(filename, mode="w", encoding="utf-8", newline="") as f:
        fieldnames = [
            "Департамент",
            "Численность",
            "Мин. зарплата",
            "Макс. зарплата",
            "Средняя зарплата",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Сводный отчёт сохранён в файл: {filename}")

if __name__ == "__main__":
    load_csv_to_global()

while True:
    print("Выберите, какое действие произвести (укажите одну цифру):")
    print("1 - Показать иерархию")
    print("2 - Показать сводный отчет")
    print("3 - Скачать сводный отчет")
    print("0 - Выйти")
    choice = input(">>> ")

    if choice == "1":
        show_hierarchy()
    elif choice == "2":
        report()
    elif choice == "3":
        download()
    elif choice == "0":
        print("Выход.")
        break
    else:
        print("Неверный ввод. Попробуйте снова.")
    print()
