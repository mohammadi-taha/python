#!/usr/bin/env python3
"""
100 Films to See Before You Die -- a desktop ticket ledger.

A tkinter GUI: search, sort, filter by decade, and "punch" tickets
to mark films watched. Pure standard library, no dependencies.

Run:
    python3 best_100_films_gui.py
"""

import json
import os
import tkinter as tk
from tkinter import ttk

# Watched-state is saved next to this script so it survives closing/reopening
# the app.
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "watched_films.json")

# ---------------------------------------------------------------- data --

FILMS = [
    {"r": 1, "title": "Seven Samurai", "orig": "", "year": 1954, "director": "Akira Kurosawa"},
    {"r": 2, "title": "Citizen Kane", "orig": "", "year": 1941, "director": "Orson Welles"},
    {"r": 3, "title": "2001: A Space Odyssey", "orig": "", "year": 1968, "director": "Stanley Kubrick"},
    {"r": 4, "title": "Rashomon", "orig": "", "year": 1950, "director": "Akira Kurosawa"},
    {"r": 5, "title": "Mulholland Dr.", "orig": "", "year": 2001, "director": "David Lynch"},
    {"r": 6, "title": "Amélie", "orig": "Le fabuleux destin d'Amélie Poulain", "year": 2001, "director": "Jean-Pierre Jeunet"},
    {"r": 7, "title": "Barry Lyndon", "orig": "", "year": 1975, "director": "Stanley Kubrick"},
    {"r": 8, "title": "The Godfather: Part II", "orig": "", "year": 1974, "director": "Francis Ford Coppola"},
    {"r": 9, "title": "City Lights", "orig": "", "year": 1931, "director": "Charles Chaplin"},
    {"r": 10, "title": "M", "orig": "M – Eine Stadt sucht einen Mörder", "year": 1931, "director": "Fritz Lang"},
    {"r": 11, "title": "The Grand Budapest Hotel", "orig": "", "year": 2014, "director": "Wes Anderson"},
    {"r": 12, "title": "Raging Bull", "orig": "", "year": 1980, "director": "Martin Scorsese"},
    {"r": 13, "title": "The Matrix", "orig": "", "year": 1999, "director": "Lilly and Lana Wachowski"},
    {"r": 14, "title": "The Godfather", "orig": "", "year": 1972, "director": "Francis Ford Coppola"},
    {"r": 15, "title": "In the Mood for Love", "orig": "Fa yeung nin wah", "year": 2000, "director": "Kar-Wai Wong"},
    {"r": 16, "title": "City of God", "orig": "Cidade de Deus", "year": 2002, "director": "Fernando Meirelles, Kátia Lund"},
    {"r": 17, "title": "Psycho", "orig": "", "year": 1960, "director": "Alfred Hitchcock"},
    {"r": 18, "title": "Network", "orig": "", "year": 1976, "director": "Sidney Lumet"},
    {"r": 19, "title": "Se7en", "orig": "", "year": 1995, "director": "David Fincher"},
    {"r": 20, "title": "The Grapes of Wrath", "orig": "", "year": 1940, "director": "John Ford"},
    {"r": 21, "title": "12 Angry Men", "orig": "", "year": 1957, "director": "Sidney Lumet"},
    {"r": 22, "title": "Forrest Gump", "orig": "", "year": 1994, "director": "Robert Zemeckis"},
    {"r": 23, "title": "Lost in Translation", "orig": "", "year": 2003, "director": "Sofia Coppola"},
    {"r": 24, "title": "Life Is Beautiful", "orig": "La vita è bella", "year": 1997, "director": "Roberto Benigni"},
    {"r": 25, "title": "Pather Panchali", "orig": "", "year": 1955, "director": "Satyajit Ray"},
    {"r": 26, "title": "Blade Runner", "orig": "", "year": 1982, "director": "Ridley Scott"},
    {"r": 27, "title": "There Will Be Blood", "orig": "", "year": 2007, "director": "Paul Thomas Anderson"},
    {"r": 28, "title": "Goodfellas", "orig": "", "year": 1990, "director": "Martin Scorsese"},
    {"r": 29, "title": "Once Upon a Time in the West", "orig": "", "year": 1968, "director": "Sergio Leone"},
    {"r": 30, "title": "Underground", "orig": "", "year": 1995, "director": "Emir Kusturica"},
    {"r": 31, "title": "Birdman or (The Unexpected Virtue of Ignorance)", "orig": "", "year": 2014, "director": "Alejandro G. Iñárritu"},
    {"r": 32, "title": "Metropolis", "orig": "", "year": 1927, "director": "Fritz Lang"},
    {"r": 33, "title": "The Rules of the Game", "orig": "La règle du jeu", "year": 1939, "director": "Jean Renoir"},
    {"r": 34, "title": "Pulp Fiction", "orig": "", "year": 1994, "director": "Quentin Tarantino"},
    {"r": 35, "title": "The Passion of Joan of Arc", "orig": "La passion de Jeanne d'Arc", "year": 1928, "director": "Carl Theodor Dreyer"},
    {"r": 36, "title": "Chinatown", "orig": "", "year": 1974, "director": "Roman Polanski"},
    {"r": 37, "title": "Man with a Movie Camera", "orig": "Chelovek s kino-apparatom", "year": 1929, "director": "Dziga Vertov"},
    {"r": 38, "title": "Kagemusha", "orig": "", "year": 1980, "director": "Akira Kurosawa"},
    {"r": 39, "title": "Apocalypse Now", "orig": "", "year": 1979, "director": "Francis Ford Coppola"},
    {"r": 40, "title": "The General", "orig": "", "year": 1926, "director": "Clyde Bruckman, Buster Keaton"},
    {"r": 41, "title": "Sunrise: A Song of Two Humans", "orig": "", "year": 1927, "director": "F.W. Murnau"},
    {"r": 42, "title": "The Birth of a Nation", "orig": "", "year": 1915, "director": "D.W. Griffith"},
    {"r": 43, "title": "Touch of Evil", "orig": "", "year": 1958, "director": "Orson Welles"},
    {"r": 44, "title": "Before Sunrise", "orig": "", "year": 1995, "director": "Richard Linklater"},
    {"r": 45, "title": "Breathless", "orig": "À bout de souffle", "year": 1960, "director": "Jean-Luc Godard"},
    {"r": 46, "title": "The Bridge", "orig": "", "year": None, "director": "—"},
    {"r": 47, "title": "Annie Hall", "orig": "", "year": 1977, "director": "Woody Allen"},
    {"r": 48, "title": "Tokyo Story", "orig": "Tōkyō monogatari", "year": 1953, "director": "Yasujirō Ozu"},
    {"r": 49, "title": "Battleship Potemkin", "orig": "Bronenosets Potemkin", "year": 1925, "director": "Sergei M. Eisenstein"},
    {"r": 50, "title": "Chungking Express", "orig": "Chung Hing sam lam", "year": 1994, "director": "Kar-Wai Wong"},
    {"r": 51, "title": "8½", "orig": "", "year": 1963, "director": "Federico Fellini"},
    {"r": 52, "title": "Inception", "orig": "", "year": 2010, "director": "Christopher Nolan"},
    {"r": 53, "title": "Alien", "orig": "", "year": 1979, "director": "Ridley Scott"},
    {"r": 54, "title": "Stagecoach", "orig": "", "year": 1939, "director": "John Ford"},
    {"r": 55, "title": "Gone with the Wind", "orig": "", "year": 1939, "director": "Victor Fleming, George Cukor and Sam Wood"},
    {"r": 56, "title": "The Cabinet of Dr. Caligari", "orig": "Das Cabinet des Dr. Caligari", "year": 1920, "director": "Robert Wiene"},
    {"r": 57, "title": "Schindler's List", "orig": "", "year": 1993, "director": "Steven Spielberg"},
    {"r": 58, "title": "Amadeus", "orig": "", "year": 1984, "director": "Milos Forman"},
    {"r": 59, "title": "Jurassic Park", "orig": "", "year": 1993, "director": "Steven Spielberg"},
    {"r": 60, "title": "Requiem for a Dream", "orig": "", "year": 2000, "director": "Darren Aronofsky"},
    {"r": 61, "title": "La Dolce Vita", "orig": "", "year": 1960, "director": "Federico Fellini"},
    {"r": 62, "title": "The Big Lebowski", "orig": "", "year": 1998, "director": "Joel and Ethan Coen"},
    {"r": 63, "title": "Modern Times", "orig": "", "year": 1936, "director": "Charles Chaplin"},
    {"r": 64, "title": "Aguirre, Wrath of God", "orig": "Aguirre, der Zorn Gottes", "year": 1972, "director": "Werner Herzog"},
    {"r": 65, "title": "Eternal Sunshine of the Spotless Mind", "orig": "", "year": 2004, "director": "Michel Gondry"},
    {"r": 66, "title": "Bicycle Thieves", "orig": "", "year": 1948, "director": "Vittorio De Sica"},
    {"r": 67, "title": "Paris, Texas", "orig": "", "year": 1984, "director": "Wim Wenders"},
    {"r": 68, "title": "The Good, the Bad and the Ugly", "orig": "", "year": 1966, "director": "Sergio Leone"},
    {"r": 69, "title": "Rocky", "orig": "", "year": 1976, "director": "John G. Avildsen"},
    {"r": 70, "title": "Contempt", "orig": "Le Mépris", "year": 1960, "director": "Jean-Luc Godard"},
    {"r": 71, "title": "Fanny and Alexander", "orig": "", "year": 1982, "director": "Ingmar Bergman"},
    {"r": 72, "title": "Groundhog Day", "orig": "", "year": 1993, "director": "Harold Ramis"},
    {"r": 73, "title": "Munich", "orig": "", "year": 2005, "director": "Steven Spielberg"},
    {"r": 74, "title": "Stalker", "orig": "", "year": 1979, "director": "Andrei Tarkovsky"},
    {"r": 75, "title": "It Happened One Night", "orig": "", "year": 1934, "director": "Frank Capra"},
    {"r": 76, "title": "The Double Life of Véronique", "orig": "", "year": 1991, "director": "Krzysztof Kieślowski"},
    {"r": 77, "title": "The 400 Blows", "orig": "Les quatre cents coups", "year": 1959, "director": "François Truffaut"},
    {"r": 78, "title": "Persona", "orig": "", "year": 1966, "director": "Ingmar Bergman"},
    {"r": 79, "title": "The Thin Red Line", "orig": "", "year": 1998, "director": "Terrence Malick"},
    {"r": 80, "title": "The Night of the Hunter", "orig": "", "year": 1955, "director": "Charles Laughton"},
    {"r": 81, "title": "All About My Mother", "orig": "Todo sobre mi madre", "year": 1999, "director": "Pedro Almodóvar"},
    {"r": 82, "title": "Fight Club", "orig": "", "year": 1999, "director": "David Fincher"},
    {"r": 83, "title": "Dog Day Afternoon", "orig": "", "year": 1975, "director": "Sidney Lumet"},
    {"r": 84, "title": "The Color of Pomegranates", "orig": "", "year": 1969, "director": "Sergei Parajanov"},
    {"r": 85, "title": "Rear Window", "orig": "", "year": 1954, "director": "Alfred Hitchcock"},
    {"r": 86, "title": "Halloween", "orig": "", "year": 1978, "director": "John Carpenter"},
    {"r": 87, "title": "Nosferatu", "orig": "", "year": 1922, "director": "F.W. Murnau"},
    {"r": 88, "title": "Three Colors: Blue", "orig": "", "year": 1993, "director": "Krzysztof Kieślowski"},
    {"r": 89, "title": "Les Diaboliques", "orig": "", "year": 1955, "director": "Henri-Georges Clouzot"},
    {"r": 90, "title": "El Topo", "orig": "", "year": 1970, "director": "Alejandro Jodorowsky"},
    {"r": 91, "title": "Fargo", "orig": "", "year": 1996, "director": "Joel and Ethan Coen"},
    {"r": 92, "title": "Sunset Boulevard", "orig": "", "year": 1950, "director": "Billy Wilder"},
    {"r": 93, "title": "Memories of Murder", "orig": "Salinui chueok", "year": 2003, "director": "Bong Joon Ho"},
    {"r": 94, "title": "L'Avventura", "orig": "", "year": 1960, "director": "Michelangelo Antonioni"},
    {"r": 95, "title": "Iruvar", "orig": "", "year": 1997, "director": "Mani Ratnam"},
    {"r": 96, "title": "Scream", "orig": "", "year": 1996, "director": "Wes Craven"},
    {"r": 97, "title": "Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb", "orig": "", "year": 1964, "director": "Stanley Kubrick"},
    {"r": 98, "title": "Black Christmas", "orig": "", "year": 1974, "director": "Bob Clark"},
    {"r": 99, "title": "Blow-Up", "orig": "", "year": 1966, "director": "Michelangelo Antonioni"},
    {"r": 100, "title": "It's a Wonderful Life", "orig": "", "year": 1946, "director": "Frank Capra"},
]

# ------------------------------------------------------------- palette --

BG = "#14110F"
BG_ALT = "#1B1613"
CARD = "#201A16"
GOLD = "#C89B4A"
GOLD_BRIGHT = "#E4B963"
RED = "#8C2F2F"
CREAM = "#EDE6D6"
MUTED = "#948A7C"
LINE = "#3A322A"

FONT_DISPLAY = ("Georgia", 22, "bold")
FONT_SUB = ("Georgia", 10)
FONT_LABEL = ("Segoe UI", 9)
FONT_MONO = ("Consolas", 10)
FONT_TREE = ("Consolas", 11)
FONT_TREE_HEAD = ("Segoe UI Semibold", 10)


class TicketLedger(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("100 Films to See Before You Die")
        self.geometry("980x720")
        self.configure(bg=BG)
        self.minsize(760, 520)

        self.watched = self._load_watched()
        self.decade_filter = tk.StringVar(value="All decades")
        self.watch_filter = tk.StringVar(value="All films")
        self.sort_mode = tk.StringVar(value="Rank")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self.render())

        self._build_style()
        self._build_header()
        self._build_controls()
        self._build_table()
        self._build_footer()

        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.render()

    # ------------------------------------------------------ persistence --
    @staticmethod
    def _load_watched():
        """Read the set of watched ranks from disk. Returns empty set if
        the file doesn't exist yet or can't be read."""
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            return set(int(r) for r in data.get("watched", []))
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            return set()

    def _save_watched(self):
        """Write the current watched set to disk so it survives restarts."""
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as fh:
                json.dump({"watched": sorted(self.watched)}, fh, ensure_ascii=False, indent=2)
        except OSError:
            pass  # non-fatal: worst case, progress just won't persist

    def _on_close(self):
        self._save_watched()
        self.destroy()

    # ---------------------------------------------------------- style --
    def _build_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("TFrame", background=BG)
        style.configure("Alt.TFrame", background=BG_ALT)

        style.configure(
            "TCombobox",
            fieldbackground=BG_ALT,
            background=BG_ALT,
            foreground=CREAM,
            arrowcolor=GOLD,
            bordercolor=LINE,
            lightcolor=BG_ALT,
            darkcolor=BG_ALT,
        )
        self.option_add("*TCombobox*Listbox.background", BG_ALT)
        self.option_add("*TCombobox*Listbox.foreground", CREAM)
        self.option_add("*TCombobox*Listbox.selectBackground", GOLD)
        self.option_add("*TCombobox*Listbox.selectForeground", BG)

        style.configure(
            "Treeview",
            background=CARD,
            fieldbackground=CARD,
            foreground=CREAM,
            rowheight=30,
            bordercolor=LINE,
            borderwidth=0,
            font=FONT_TREE,
        )
        style.map(
            "Treeview",
            background=[("selected", "#2E2620")],
            foreground=[("selected", GOLD_BRIGHT)],
        )
        style.configure(
            "Treeview.Heading",
            background=BG_ALT,
            foreground=GOLD,
            relief="flat",
            font=FONT_TREE_HEAD,
        )
        style.map("Treeview.Heading", background=[("active", BG_ALT)])

        style.configure(
            "Ledger.Vertical.TScrollbar",
            background=BG_ALT,
            troughcolor=BG,
            bordercolor=BG,
            arrowcolor=GOLD,
        )

    # --------------------------------------------------------- header --
    def _build_header(self):
        # sprocket strip
        sprockets = tk.Canvas(self, height=16, bg="#0F0C0A", highlightthickness=0)
        sprockets.pack(fill="x")
        self._draw_sprockets(sprockets)
        sprockets.bind("<Configure>", lambda e: self._draw_sprockets(sprockets))

        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", pady=(20, 10))

        eyebrow = tk.Label(
            header, text="A CINÉMATHÈQUE INDEX  ·  NO. 1–100",
            fg=GOLD, bg=BG, font=("Segoe UI", 9, "bold"),
        )
        eyebrow.pack()

        title = tk.Label(
            header, text="100 Films to See Before You Die",
            fg=CREAM, bg=BG, font=FONT_DISPLAY,
        )
        title.pack(pady=(6, 4))

        sub = tk.Label(
            header,
            text="A ranked admission ledger. Double-click a row to punch the ticket.",
            fg=MUTED, bg=BG, font=FONT_SUB,
        )
        sub.pack()

        # progress
        prog_wrap = tk.Frame(header, bg=BG)
        prog_wrap.pack(fill="x", padx=260, pady=(16, 0))

        prog_label_row = tk.Frame(prog_wrap, bg=BG)
        prog_label_row.pack(fill="x")
        tk.Label(prog_label_row, text="TICKETS PUNCHED", fg=MUTED, bg=BG,
                 font=("Segoe UI", 8, "bold")).pack(side="left")
        self.progress_text = tk.Label(
            prog_label_row, text="0 / 100", fg=GOLD_BRIGHT, bg=BG,
            font=("Segoe UI", 8, "bold"),
        )
        self.progress_text.pack(side="right")

        self.progress_canvas = tk.Canvas(prog_wrap, height=8, bg=BG_ALT, highlightthickness=1,
                                          highlightbackground=LINE)
        self.progress_canvas.pack(fill="x", pady=(4, 0))
        self.progress_canvas.bind("<Configure>", lambda e: self._draw_progress())

    def _draw_sprockets(self, canvas):
        canvas.delete("all")
        w = canvas.winfo_width() or 980
        x = 7
        while x < w:
            canvas.create_oval(x - 4, 3, x + 4, 11, fill=BG, outline="")
            x += 28

    def _draw_progress(self):
        self.progress_canvas.delete("bar")
        w = self.progress_canvas.winfo_width()
        h = self.progress_canvas.winfo_height()
        frac = len(self.watched) / 100
        if frac > 0:
            self.progress_canvas.create_rectangle(
                0, 0, w * frac, h, fill=GOLD, outline="", tags="bar"
            )

    # -------------------------------------------------------- controls --
    def _build_controls(self):
        bar = tk.Frame(self, bg=BG)
        bar.pack(fill="x", padx=24, pady=(6, 8))

        search_frame = tk.Frame(bar, bg=BG_ALT, highlightbackground=LINE, highlightthickness=1)
        search_frame.pack(side="left", fill="x", expand=True, ipady=4)
        tk.Label(search_frame, text="🔎", bg=BG_ALT, fg=MUTED).pack(side="left", padx=(8, 2))
        entry = tk.Entry(
            search_frame, textvariable=self.search_var, bg=BG_ALT, fg=CREAM,
            insertbackground=CREAM, relief="flat", font=FONT_MONO,
        )
        entry.pack(side="left", fill="x", expand=True, padx=(0, 8))

        decades = ["All decades"] + [f"{d}s" for d in sorted({(f['year'] // 10) * 10 for f in FILMS if f["year"]})]
        decade_box = ttk.Combobox(
            bar, textvariable=self.decade_filter, values=decades, state="readonly", width=12
        )
        decade_box.pack(side="left", padx=8)
        decade_box.bind("<<ComboboxSelected>>", lambda e: self.render())

        watch_box = ttk.Combobox(
            bar, textvariable=self.watch_filter,
            values=["All films", "Watched only", "Unwatched only"],
            state="readonly", width=14,
        )
        watch_box.pack(side="left", padx=8)
        watch_box.bind("<<ComboboxSelected>>", lambda e: self.render())

        sort_box = ttk.Combobox(
            bar, textvariable=self.sort_mode,
            values=["Rank", "Title A–Z", "Year (oldest)", "Year (newest)"],
            state="readonly", width=14,
        )
        sort_box.pack(side="left", padx=8)
        sort_box.bind("<<ComboboxSelected>>", lambda e: self.render())

        self.count_label = tk.Label(self, text="", fg=MUTED, bg=BG, font=("Segoe UI", 9, "bold"))
        self.count_label.pack(anchor="w", padx=26, pady=(0, 4))

    # ----------------------------------------------------------- table --
    def _build_table(self):
        wrap = tk.Frame(self, bg=BG)
        wrap.pack(fill="both", expand=True, padx=24, pady=(0, 10))

        columns = ("watched", "rank", "title", "year", "director")
        self.tree = ttk.Treeview(
            wrap, columns=columns, show="headings", selectmode="browse"
        )
        self.tree.heading("watched", text="✓")
        self.tree.heading("rank", text="No.")
        self.tree.heading("title", text="Title")
        self.tree.heading("year", text="Year")
        self.tree.heading("director", text="Director")

        self.tree.column("watched", width=36, anchor="center", stretch=False)
        self.tree.column("rank", width=54, anchor="center", stretch=False)
        self.tree.column("title", width=440, anchor="w")
        self.tree.column("year", width=70, anchor="center", stretch=False)
        self.tree.column("director", width=260, anchor="w")

        vsb = ttk.Scrollbar(wrap, orient="vertical", command=self.tree.yview,
                             style="Ledger.Vertical.TScrollbar")
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        self.tree.tag_configure("watched", foreground=GOLD_BRIGHT)
        self.tree.tag_configure("unwatched", foreground=CREAM)

        self.tree.bind("<Double-1>", self._on_toggle)
        self.tree.bind("<Return>", self._on_toggle)

    def _build_footer(self):
        tk.Label(
            self, text="COMPILED FROM A 100-FILMS CANON  ·  DOUBLE-CLICK TO PUNCH A TICKET",
            fg=MUTED, bg=BG, font=("Segoe UI", 8),
        ).pack(pady=(0, 14))

    # ----------------------------------------------------------- logic --
    def _on_toggle(self, event):
        item = self.tree.identify_row(event.y) if hasattr(event, "y") else self.tree.focus()
        if not item:
            return
        rank = int(self.tree.set(item, "rank"))
        if rank in self.watched:
            self.watched.remove(rank)
        else:
            self.watched.add(rank)
        self._save_watched()
        self.render(keep_selection=item)

    def _filtered_sorted(self):
        q = self.search_var.get().strip().lower()
        decade = self.decade_filter.get()
        watch_mode = self.watch_filter.get()

        rows = []
        for f in FILMS:
            if q:
                hay = f"{f['title']} {f['orig']} {f['director']}".lower()
                if q not in hay:
                    continue
            if decade != "All decades":
                d = int(decade[:-1])
                if not f["year"] or (f["year"] // 10) * 10 != d:
                    continue
            if watch_mode == "Watched only" and f["r"] not in self.watched:
                continue
            if watch_mode == "Unwatched only" and f["r"] in self.watched:
                continue
            rows.append(f)

        mode = self.sort_mode.get()
        if mode == "Title A–Z":
            rows.sort(key=lambda f: f["title"].lower())
        elif mode == "Year (oldest)":
            rows.sort(key=lambda f: f["year"] or 9999)
        elif mode == "Year (newest)":
            rows.sort(key=lambda f: -(f["year"] or 0))
        else:
            rows.sort(key=lambda f: f["r"])
        return rows

    def render(self, keep_selection=None):
        self.tree.delete(*self.tree.get_children())
        rows = self._filtered_sorted()
        for f in rows:
            title = f["title"] + (f"  [{f['orig']}]" if f["orig"] else "")
            mark = "✓" if f["r"] in self.watched else ""
            tag = "watched" if f["r"] in self.watched else "unwatched"
            self.tree.insert(
                "", "end",
                values=(mark, f["r"], title, f["year"] or "—", f["director"]),
                tags=(tag,),
            )

        self.count_label.config(text=f"{len(rows)} OF 100 FILMS")
        self.progress_text.config(text=f"{len(self.watched)} / 100")
        self._draw_progress()


if __name__ == "__main__":
    app = TicketLedger()
    app.mainloop()
