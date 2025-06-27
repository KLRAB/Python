# ----------------- MODUŁY I PAKIETY -------------------
import json                    # <- obsługa plików json
import datetime                # <- operacje na datach
from functools import reduce   # <- programowanie funkcyjne

# ----------------- ZMIENNE GLOBALNE -------------------
PLIK_TXT = "plan.txt"      # <- zmienna globalna (nazwa pliku TXT)
PLIK_JSON = "plan.json"    # <- zmienna globalna (nazwa pliku JSON)

# ----------------- FUNKCJE POMOCNICZE -----------------
def str_to_date(s):
    # Funkcja zamieniająca string na datę (operacja na stringach)
    try:                                # <- obsługa wyjątków try/except
        return datetime.datetime.strptime(s, "%Y-%m-%d").date()
    except Exception:
        raise ValueError("Zły format daty! Poprawny: YYYY-MM-DD")

def input_date(msg):
    # Funkcja pomocnicza do pobierania daty od użytkownika
    while True:
        try:
            data = input(msg)
            return str_to_date(data)
        except Exception as e:
            print(e)

def pretty_print(data):
    # Funkcja wyświetlająca zawartość listy/krotki/słownika/zestawu (kontenery)
    if isinstance(data, (list, tuple, set)):
        for i, item in enumerate(data, 1):  # <- użycie krotki (i, item)
            print(f"{i}. {item}")
    elif isinstance(data, dict):
        for k, v in data.items():
            print(f"{k}: {v}")
    else:
        print(data)

def log_action(func):
    # Dekorator do logowania operacji (dekoratory, programowanie funkcyjne)
    def wrapper(*args, **kwargs):
        print(f"-> Wykonuję: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

# ----------------- KLASY I OOP ------------------------
class Task:
    """Zadanie do nauki – klasa OOP"""
    def __init__(self, name, subject, exam_date, done=False):
        # Konstruktory, zakres klasy, zmienne instancyjne (self.)
        self.name = name
        self.subject = subject
        self.exam_date = exam_date
        self.done = done

    def __str__(self):
        # Formatowanie stringów (operacje na stringach)
        status = "✔" if self.done else "✘"
        return f"{self.name} | {self.subject} | {self.exam_date} | {status}"

    def to_dict(self):
        # Metoda zwraca słownik (dictionary)
        return {
            "name": self.name,
            "subject": self.subject,
            "exam_date": self.exam_date.isoformat(),
            "done": self.done
        }

    @staticmethod
    def from_dict(d):
        # Funkcja przyjmująca inny słownik (funkcje z parametrem innej funkcji)
        return Task(d['name'], d['subject'], str_to_date(d['exam_date']), d['done'])

class RecurringTask(Task):  # <- dziedziczenie OOP
    """Zadanie cykliczne (dziedziczy po Task)"""
    def __init__(self, name, subject, exam_date, interval_days, done=False):
        super().__init__(name, subject, exam_date, done)
        self.interval_days = interval_days

    def next_date(self):
        # Funkcja rekurencyjna (przykład)
        return self.exam_date + datetime.timedelta(days=self.interval_days)

    def __str__(self):
        return super().__str__() + f" | co {self.interval_days} dni"

# ----------------- GŁÓWNY PLANNER ---------------------
class Planner:
    """Planer nauki – agreguje zadania w liście"""
    def __init__(self):
        self.tasks = []  # <- użycie listy (kontener)

    @log_action
    def add_task(self, task):
        self.tasks.append(task)

    @log_action
    def remove_task(self, idx):
        assert 0 <= idx < len(self.tasks), "Nieprawidłowy indeks!"  # <- użycie assert
        del self.tasks[idx]

    @log_action
    def mark_done(self, idx):
        assert 0 <= idx < len(self.tasks), "Nieprawidłowy indeks!"
        self.tasks[idx].done = True

    @log_action
    def change_task(self, idx, **kwargs):
        assert 0 <= idx < len(self.tasks), "Nieprawidłowy indeks!"
        task = self.tasks[idx]
        for k, v in kwargs.items():
            setattr(task, k, v)

    @log_action
    def show(self):
        if not self.tasks:
            print("Brak zadań.")
        else:
            pretty_print(self.tasks)  # <- użycie listy i pretty_print (z krotką)

    @log_action
    def show_names(self):
        # Przykład użycia map (programowanie funkcyjne)
        names = list(map(lambda t: t.name, self.tasks))  # <- użycie map i lambda
        print("Nazwy wszystkich zadań:")
        pretty_print(names)

    @log_action
    def find(self, query):
        # Wyszukiwanie po stringu (lambda, filter, operacje na stringach)
        res = list(filter(lambda t: query.lower() in t.name.lower() or query.lower() in t.subject.lower(), self.tasks))  # <- filter i lambda
        pretty_print(res)

    @log_action
    def upcoming(self, days=7):
        today = datetime.date.today()
        future = today + datetime.timedelta(days=days)
        soon = list(filter(lambda t: today <= t.exam_date <= future, self.tasks))  # <- filter i lambda
        pretty_print(soon)

    @log_action
    def stats(self):
        # Użycie zbioru (set), słownika (dict), krotki (tuple), reduce
        subjects = set(t.subject for t in self.tasks)         # <- set
        counts = {s: 0 for s in subjects}                    # <- dict
        for t in self.tasks:
            counts[t.subject] += 1
        print("Statystyki przedmiotów:")
        pretty_print(counts)
        # Reduce - suma ukończonych
        done_count = reduce(lambda acc, t: acc + int(t.done), self.tasks, 0)  # <- reduce, lambda
        print(f"Ukończonych zadań: {done_count} / {len(self.tasks)}")

    @log_action
    def save_txt(self, fname=PLIK_TXT):
        # Zapis do pliku .txt
        try:
            with open(fname, "w", encoding="utf-8") as f:
                for t in self.tasks:
                    f.write(f"{t.name}|{t.subject}|{t.exam_date}|{t.done}\n")
        except Exception as e:
            print("Błąd zapisu:", e)

    @log_action
    def load_txt(self, fname=PLIK_TXT):
        # Odczyt z pliku .txt
        try:
            with open(fname, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        name, subject, exam_date, done = line.strip().split('|')  # <- operacja na stringach (dzielenie)
                        self.tasks.append(Task(name, subject, str_to_date(exam_date), done == "True"))
                    except Exception:
                        print("Pominięto błędny wpis w pliku.")
        except FileNotFoundError:
            print("Brak pliku TXT, utworzony zostanie nowy planer.")

    @log_action
    def save_json(self, fname=PLIK_JSON):
        # Zapis do pliku .json
        try:
            with open(fname, "w", encoding="utf-8") as f:
                json.dump([t.to_dict() for t in self.tasks], f, ensure_ascii=False, indent=2)
        except Exception as e:
            print("Błąd zapisu:", e)

    @log_action
    def load_json(self, fname=PLIK_JSON):
        # Odczyt z pliku .json
        try:
            with open(fname, "r", encoding="utf-8") as f:
                self.tasks = [Task.from_dict(d) for d in json.load(f)]
        except FileNotFoundError:
            print("Brak pliku JSON, utworzony zostanie nowy planer.")
        except Exception as e:
            print("Błąd wczytywania JSON:", e)

# ----------------- UI: INTERAKTYWNE MENU ---------------
def menu():
    # Zmienna lokalna – menu jest tylko tutaj (zakres funkcji)
    print("""
    ==== PLANER NAUKI DO EGZAMINÓW ====
    1. Dodaj zadanie
    2. Dodaj zadanie cykliczne
    3. Wyświetl zadania
    4. Wyświetl nazwy wszystkich zadań (map)
    5. Zmień zadanie
    6. Usuń zadanie
    7. Oznacz jako wykonane
    8. Szukaj zadania
    9. Zadania na najbliższy tydzień
    10. Statystyki
    11. Zapisz do pliku TXT
    12. Wczytaj z pliku TXT
    13. Zapisz do pliku JSON
    14. Wczytaj z pliku JSON
    0. Wyjdź
    """)

# ----------------- FUNKCJA GŁÓWNA ----------------------
def main():
    # Zmienna lokalna planner (zakres funkcji)
    planner = Planner()

    # Przykładowe dane (przykład wejściowy/wyjściowy)
    planner.add_task(Task("Powtórka lambda", "Informatyka", datetime.date(2024, 7, 2)))
    planner.add_task(Task("Rozdział 3 - Chemia", "Chemia", datetime.date(2024, 7, 7)))
    planner.add_task(RecurringTask("Słownictwo", "Angielski", datetime.date(2024, 6, 28), interval_days=2))

    while True:
        menu()
        try:
            opcja = input("Wybierz opcję: ").strip()
            if opcja == "1":
                name = input("Nazwa zadania: ")
                subject = input("Przedmiot: ")
                date = input_date("Data egzaminu (YYYY-MM-DD): ")
                planner.add_task(Task(name, subject, date))
            elif opcja == "2":
                name = input("Nazwa zadania: ")
                subject = input("Przedmiot: ")
                date = input_date("Data pierwszego terminu: ")
                interval = int(input("Co ile dni powtarzać?: "))
                planner.add_task(RecurringTask(name, subject, date, interval))
            elif opcja == "3":
                planner.show()
            elif opcja == "4":
                planner.show_names()
            elif opcja == "5":
                idx = int(input("Podaj numer zadania do zmiany: ")) - 1
                field = input("Co chcesz zmienić? (name/subject/date): ")
                if field == "date":
                    val = input_date("Nowa data (YYYY-MM-DD): ")
                else:
                    val = input("Nowa wartość: ")
                planner.change_task(idx, **{field: val})
            elif opcja == "6":
                idx = int(input("Podaj numer zadania do usunięcia: ")) - 1
                planner.remove_task(idx)
            elif opcja == "7":
                idx = int(input("Podaj numer zadania do oznaczenia jako wykonane: ")) - 1
                planner.mark_done(idx)
            elif opcja == "8":
                query = input("Szukaj: ")
                planner.find(query)
            elif opcja == "9":
                planner.upcoming()
            elif opcja == "10":
                planner.stats()
            elif opcja == "11":
                planner.save_txt()
            elif opcja == "12":
                planner.load_txt()
            elif opcja == "13":
                planner.save_json()
            elif opcja == "14":
                planner.load_json()
            elif opcja == "0":
                print("Zapisuję do pliku TXT i kończę...")
                planner.save_txt()
                break
            else:
                print("Nieznana opcja!")
        except Exception as e:
            print("Błąd:", e)

# --------------- PUNKT STARTOWY ------------------------
if __name__ == "__main__":
    # Kod uruchamiany tylko przy bezpośrednim starcie pliku (zakres globalny)
    main()

