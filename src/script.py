import tkinter as tk
import random
import json
import os
import hashlib

WORDS = [
    "kot", "pies", "dom", "las", "ser", "mysz", "król", "smok", "woda", "ogień",
    "ryba", "zamek", "góra", "ptak", "nos", "mleko", "deszcz", "liść", "wiatr", "noc",
    "jabłko", "zegarek", "książka", "kaktus", "cebula", "okulary", "apteka", "delfin",
    "skrzynia", "zegar", "harfa", "żaba", "latarka", "ogórek", "cukier", "motyl",
    "piernik", "ściana", "dywan", "wulkan", "wiewiórka", "żółw", "marchewka",
    "księżyc", "dynia", "pelikan", "jezioro", "śnieg", "podróż", "pociąg",
    "chmura", "rakieta", "lustro", "zameczek", "ścieżka"
]

def hash_password(p):
    """Hashuje hasło przy użyciu SHA-256.

    Args:
        p (str): Hasło użytkownika.

    Returns:
        str: Zahaszowane hasło.
    """
    return hashlib.sha256(p.encode()).hexdigest()

def load_users():
    """Wczytuje dane użytkowników z pliku JSON.

    Returns:
        dict: Słownik z danymi użytkowników.
    """
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            return json.load(f)
    return {}

def save_users(data):
    """Zapisuje dane użytkowników do pliku JSON.

    Args:
        data (dict): Słownik z danymi użytkowników.
    """
    with open("users.json", "w") as f:
        json.dump(data, f, indent=4)

def center_window(window, width=None, height=None):
    """Centruje okno aplikacji na ekranie.

    Args:
        window (tk.Tk): Referencja do głównego okna.
        width (int, optional): Szerokość okna. Domyślnie None.
        height (int, optional): Wysokość okna. Domyślnie None.
    """
    window.update_idletasks()
    if width is None or height is None:
        width = window.winfo_width()
        height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

class HangmanApp:
    """Główna klasa aplikacji gry Wisielec."""
    def __init__(self, root):
        """Inicjalizuje interfejs oraz ładuje dane użytkowników.

        Args:
            root (tk.Tk): Główne okno aplikacji.
        """
        self.root = root
        self.users = load_users()
        self.logged_in = {"A": None, "B": None}
        self.build_login()

    def build_login(self):
        """Buduje interfejs logowania dla dwóch graczy."""
        self.clear()
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack()
        tk.Label(self.login_frame, text="Zaloguj się", font=("Arial", 20)).pack(pady=20)
        self.status_labels = {}
        self.stats_buttons = {}

        for player in ["A", "B"]:
            f = tk.Frame(self.login_frame)
            f.pack(pady=10)
            tk.Label(f, text=f"Gracz {player}:", font=("Arial", 12)).grid(row=0, column=0, padx=5)
            tk.Button(f, text="Login", font=("Arial", 12), command=lambda p=player: self.login_popup(p)).grid(row=0, column=1, padx=5)
            tk.Button(f, text="Register", font=("Arial", 12), command=lambda p=player: self.register_popup(p)).grid(row=0, column=2, padx=5)
            self.status_labels[player] = tk.Label(f, text="Nie zalogowano", fg="red", font=("Arial", 12))
            self.status_labels[player].grid(row=0, column=3, padx=10)
            self.stats_buttons[player] = tk.Button(f, text="Statystyki", font=("Arial", 12),
                                                   command=lambda p=player: self.show_stats(p), state="disabled")
            self.stats_buttons[player].grid(row=0, column=4, padx=5)

        self.play_button = tk.Button(self.login_frame, text="PLAY", font=("Arial", 16), state="disabled", command=self.select_mode)
        self.play_button.pack(pady=20)

    def login_popup(self, player):
        """Tworzy okno popup do logowania gracza.

        Args:
            player (str): Symbol gracza ("A" lub "B").
        """
        w = tk.Toplevel()
        w.title(f"Logowanie Gracz {player}")
        center_window(w, 300, 200)
        tk.Label(w, text="Login").pack()
        login = tk.Entry(w, font=("Arial", 14), width=25)
        login.pack()
        tk.Label(w, text="Hasło").pack()
        password = tk.Entry(w, show="*", font=("Arial", 14), width=25)
        password.pack()

        def attempt():
            u = login.get()
            p = hash_password(password.get())
            if u in self.users and self.users[u]["password"] == p:
                self.logged_in[player] = u
                self.status_labels[player].config(text=f"{u} ✔", fg="green")
                self.stats_buttons[player].config(state="normal")
                w.destroy()
                if all(self.logged_in.values()):
                    self.play_button.config(state="normal")
            else:
                tk.Label(w, text="Błąd logowania", fg="red").pack()

        tk.Button(w, text="Zaloguj", command=attempt).pack()

    def register_popup(self, player):
        """Tworzy okno popup do rejestracji nowego gracza.

        Args:
            player (str): Symbol gracza ("A" lub "B").
        """
        w = tk.Toplevel()
        w.title(f"Rejestracja Gracz {player}")
        center_window(w, 300, 250)
        tk.Label(w, text="Login").pack()
        login = tk.Entry(w, font=("Arial", 14), width=25)
        login.pack()
        tk.Label(w, text="Hasło").pack()
        p1 = tk.Entry(w, show="*", font=("Arial", 14), width=25)
        p1.pack()
        tk.Label(w, text="Potwierdź Hasło").pack()
        p2 = tk.Entry(w, show="*", font=("Arial", 14), width=25)
        p2.pack()

        def register():
            u = login.get()
            if u in self.users:
                tk.Label(w, text="Użytkownik istnieje", fg="red").pack()
                return
            if p1.get() != p2.get():
                tk.Label(w, text="Hasła różne", fg="red").pack()
                return
            self.users[u] = {"password": hash_password(p1.get()), "wins": 0, "losses": 0}
            save_users(self.users)
            tk.Label(w, text="Zarejestrowano", fg="green").pack()

        tk.Button(w, text="Zarejestruj", command=register).pack()

    def show_stats(self, player):
        """Wyświetla statystyki dla zalogowanego gracza.

        Args:
            player (str): Symbol gracza ("A" lub "B").
        """
        user = self.logged_in[player]
        stats = self.users.get(user, {"wins": 0, "losses": 0})

        w = tk.Toplevel()
        w.title(f"Statystyki Gracza {player}")
        center_window(w, 300, 200)

        tk.Label(w, text=f"Gracz {player}: {user}", font=("Arial", 14)).pack(pady=10)
        tk.Label(w, text=f"Wygrane: {stats['wins']}", font=("Arial", 12)).pack(pady=5)
        tk.Label(w, text=f"Przegrane: {stats['losses']}", font=("Arial", 12)).pack(pady=5)

        tk.Button(w, text="Zamknij", command=w.destroy).pack(pady=10)

    def select_mode(self):
        """Pozwala wybrać tryb gry: łatwy lub trudny."""
        self.clear()
        self.mode_frame = tk.Frame(self.root)
        self.mode_frame.pack()
        tk.Label(self.mode_frame, text="Wybierz tryb gry", font=("Arial", 18)).pack(pady=15)
        tk.Button(self.mode_frame, text="Łatwy (11 prób)", font=("Arial", 14), command=lambda: self.start_game(11)).pack(pady=10)
        tk.Button(self.mode_frame, text="Trudny (6 prób)", font=("Arial", 14), command=lambda: self.start_game(6)).pack(pady=10)

    def start_game(self, max_tries):
        """Rozpoczyna rozgrywkę w wybranym trybie.

        Args:
            max_tries (int): Maksymalna liczba prób (6 lub 11).
        """
        self.max_tries = max_tries
        self.clear()
        self.word = {"A": random.choice(WORDS), "B": random.choice(WORDS)}
        self.guessed = {"A": set(), "B": set()}
        self.tries = {"A": max_tries, "B": max_tries}
        self.turn = "A"

        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack()

        tk.Label(self.game_frame, text=f"Tryb gry: {'Easy' if max_tries == 11 else 'Hard'}", font=("Arial", 16)).pack(pady=10)

        top = tk.Frame(self.game_frame)
        top.pack()

        self.canvas = {"A": tk.Canvas(top, width=150, height=150, bg="white"),
                       "B": tk.Canvas(top, width=150, height=150, bg="white")}
        tk.Label(top, text="Gracz A", font=("Arial", 14)).grid(row=0, column=0)
        self.canvas["A"].grid(row=1, column=0, padx=10, pady=5)
        tk.Label(top, text="Gracz B", font=("Arial", 14)).grid(row=0, column=1)
        self.canvas["B"].grid(row=1, column=1, padx=10, pady=5)

        self.word_display = {"A": tk.StringVar(), "B": tk.StringVar()}
        self.word_labels = {
            "A": tk.Label(top, textvariable=self.word_display["A"], font=("Courier", 24)),
            "B": tk.Label(top, textvariable=self.word_display["B"], font=("Courier", 24))
        }
        self.word_labels["A"].grid(row=2, column=0, pady=10)
        self.word_labels["B"].grid(row=2, column=1, pady=10)

        self.status = tk.StringVar()
        self.status.set("Tura gracza A")
        tk.Label(self.game_frame, textvariable=self.status, font=("Arial", 14)).pack(pady=10)

        self.entry = tk.Entry(self.game_frame, font=("Arial", 14), width=10)
        self.entry.pack(pady=5)
        tk.Button(self.game_frame, text="Zgadnij", font=("Arial", 14), command=self.make_guess).pack(pady=10)

        self.info = tk.StringVar()
        tk.Label(self.game_frame, textvariable=self.info, font=("Arial", 12)).pack(pady=5)

        self.update_display()

    def draw_hangman(self, canvas, stage, max_stage):
        """Rysuje wisielca w zależności od etapu gry.

        Args:
            canvas (tk.Canvas): Płótno do rysowania.
            stage (int): Aktualny etap (ilość błędów).
            max_stage (int): Maksymalna liczba etapów.
        """
        canvas.delete("all")
        canvas.create_line(10, 140, 140, 140, width=2)
        canvas.create_line(30, 140, 30, 10, width=2)
        canvas.create_line(30, 10, 100, 10, width=2)
        canvas.create_line(100, 10, 100, 30, width=2)

        elements = [
            lambda: canvas.create_oval(85, 30, 115, 60),
            lambda: canvas.create_line(100, 60, 100, 100),
            lambda: canvas.create_line(100, 70, 80, 90),
            lambda: canvas.create_line(100, 70, 120, 90),
            lambda: canvas.create_line(100, 100, 85, 125),
            lambda: canvas.create_line(100, 100, 115, 125),
            lambda: canvas.create_oval(92, 38, 94, 40),
            lambda: canvas.create_oval(106, 38, 108, 40),
            lambda: canvas.create_line(93, 50, 107, 50),
            lambda: canvas.create_line(95, 45, 97, 42),
            lambda: canvas.create_line(105, 45, 103, 42),
        ]

        draw_count = min(len(elements), round((stage / max_stage) * len(elements)))
        for i in range(draw_count):
            elements[i]()

    def update_display(self):
        """Aktualizuje wyświetlane słowa i rysunki wisielców."""
        for p in ["A", "B"]:
            if p == self.turn:
                self.word_display[p].set(' '.join([c if c in self.guessed[p] else '_' for c in self.word[p]]))
            else:
                self.word_display[p].set(' ' * len(self.word[p]))
            self.draw_hangman(self.canvas[p], self.max_tries - self.tries[p], self.max_tries)

    def make_guess(self):
        """Obsługuje zgadywanie liter lub słowa przez gracza."""
        guess = self.entry.get().strip().lower()
        self.entry.delete(0, tk.END)
        if not guess:
            return

        p = self.turn
        if guess == self.word[p]:
            self.guessed[p].update(self.word[p])
            self.info.set("Zgadłeś całe słowo!")
        elif len(guess) == 1:
            if guess in self.guessed[p]:
                self.info.set("Już była ta litera.")
            elif guess in self.word[p]:
                self.guessed[p].add(guess)
                self.info.set("Dobrze!")
            else:
                self.tries[p] -= 1
                self.info.set("Źle!")
        else:
            self.tries[p] -= 1
            self.info.set("Nieprawidłowe słowo.")

        self.check_end()
        self.update_display()

    def check_end(self):
        """Sprawdza czy gra się zakończyła i ogłasza wynik."""
        results = {}
        for p in ["A", "B"]:
            if set(self.word[p]) == self.guessed[p]:
                results[p] = "win"
            elif self.tries[p] <= 0:
                results[p] = "loss"
            else:
                results[p] = "ongoing"

        if all(r in ["win", "loss"] for r in results.values()):
            self.entry.config(state="disabled")
            self.info.set("Koniec gry!")

            winner = None
            if results["A"] == "win" and results["B"] != "win":
                winner = "A"
            elif results["B"] == "win" and results["A"] != "win":
                winner = "B"

            if winner:
                loser = "A" if winner == "B" else "B"
                self.users[self.logged_in[winner]]["wins"] += 1
                self.users[self.logged_in[loser]]["losses"] += 1
                save_users(self.users)
                self.status.set(f"Gracz {winner} wygrał! Słowo: {self.word[winner]}")
            else:
                self.status.set("Remis – obaj przegrali lub odgadli.")

            self.root.after(5000, self.build_login)
        else:
            self.turn = "B" if self.turn == "A" else "A"
            while results[self.turn] != "ongoing":
                self.turn = "B" if self.turn == "A" else "A"
            self.status.set(f"Tura gracza {self.turn}")

    def clear(self):
        """Czyści wszystkie widgety z głównego okna."""
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    """Uruchamia grę - 'Wisielec dla dwóch graczy'."""
    root = tk.Tk()
    root.title("Wisielec – Gra dla 2 graczy")
    app = HangmanApp(root)
    root.update_idletasks()
    center_window(root, 700, 600)
    root.mainloop()
