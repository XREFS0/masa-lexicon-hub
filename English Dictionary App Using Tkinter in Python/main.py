"""
MASA 11_English Dictionary App Using Tkinter in Python with Source Code
Developer: MASA
"""

import customtkinter as ctk
import tkinter as tk
import requests
import json
import os

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

CACHE_FILE = "dictionary_cache.json"

if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r") as f:
        cache = json.load(f)
else:
    cache = {}


def save_cache():
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=4)


def search_word(word=None):
    output.config(state="normal")
    output.delete("1.0", "end")
    w = word if word else entry.get().strip().lower()
    if not w:
        return

    if w in cache:
        display_data(cache[w])
        history.insert("end", w)
        output.config(state="disabled")
        return

    try:
        res = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{w}")
        if res.status_code != 200:
            output.insert("end", "Word not found.")
            output.config(state="disabled")
            return

        data = res.json()[0]
        cache[w] = data
        save_cache()
        display_data(data)
        history.insert("end", w)
        output.config(state="disabled")

    except:
        output.insert("end", "Network error.")
        output.config(state="disabled")


def display_data(data):
    output.config(state="normal")
    word = data["word"]
    phonetic = data.get("phonetic", "N/A")

    output.insert("end", f"{word.upper()}\n", "title")
    output.insert("end", f"Pronunciation: {phonetic}\n\n", "subtitle")

    for meaning in data.get("meanings", []):
        output.insert("end", f"{meaning.get('partOfSpeech','')}\n", "subtitle")
        for idx, d in enumerate(meaning.get("definitions", []), 1):
            output.insert("end", f"{idx}. {d.get('definition','')}\n")

            synonyms = d.get("synonyms", [])
            if synonyms:
                output.insert("end", "   Synonyms: ")
                for s in synonyms[:10]:
                    start = output.index("end")
                    output.insert("end", s + " ")
                    end = output.index("end")
                    output.tag_add(s, start, end)
                    output.tag_config(s, foreground="#1e90ff", underline=True)
                    output.tag_bind(s, "<Button-1>", lambda e, w=s: search_word(w))
                output.insert("end", "\n")

            antonyms = d.get("antonyms", [])
            if antonyms:
                output.insert("end", "   Antonyms: ")
                for a in antonyms[:10]:
                    start = output.index("end")
                    output.insert("end", a + " ")
                    end = output.index("end")
                    output.tag_add(a, start, end)
                    output.tag_config(a, foreground="#ff4500", underline=True)
                    output.tag_bind(a, "<Button-1>", lambda e, w=a: search_word(w))
                output.insert("end", "\n")
        output.insert("end", "\n")
    output.config(state="disabled")


def auto_suggest(event):
    typed = entry.get().lower()
    suggestions.delete(0, "end")
    if not typed:
        return
    for word in cache.keys():
        if word.startswith(typed):
            suggestions.insert("end", word)


def select_suggestion(event):
    if not suggestions.curselection():
        return
    selected = suggestions.get(suggestions.curselection())
    entry.delete(0, "end")
    entry.insert(0, selected)
    search_word(selected)


app = ctk.CTk()
app.title("MASA Lexicon Dictionary")
app.geometry("850x600")

top_frame = ctk.CTkFrame(app)
top_frame.pack(fill="x", padx=10, pady=10)

entry = ctk.CTkEntry(top_frame, width=400, font=("Arial", 16))
entry.pack(side="left", padx=(0, 10))
entry.bind("<KeyRelease>", auto_suggest)

ctk.CTkButton(top_frame, text="Search", command=search_word, width=100).pack(side="left")
ctk.CTkButton(
    top_frame,
    text="🌙 Toggle Theme",
    command=lambda: ctk.set_appearance_mode("Dark" if ctk.get_appearance_mode() == "Light" else "Light"),
).pack(side="right")

main_frame = ctk.CTkFrame(app)
main_frame.pack(fill="both", expand=True, padx=10, pady=5)

suggestions = tk.Listbox(
    main_frame, height=15, font=("Arial", 12), bg="#1e1e1e", fg="white", selectbackground="#3b82f6", width=25
)
suggestions.pack(side="left", fill="y", padx=(0, 5))
suggestions.bind("<<ListboxSelect>>", select_suggestion)

output_frame = ctk.CTkFrame(main_frame)
output_frame.pack(side="left", fill="both", expand=True)

output_scroll = ctk.CTkScrollbar(output_frame, orientation="vertical")
output_scroll.pack(side="right", fill="y")

output = tk.Text(output_frame, wrap="word", font=("Arial", 14), yscrollcommand=output_scroll.set)
output.pack(fill="both", expand=True)
output_scroll.configure(command=output.yview)
output.config(state="disabled")

output.tag_config("title", font=("Arial", 20, "bold"), foreground="#3b82f6")
output.tag_config("subtitle", font=("Arial", 14, "bold"), foreground="#555555")

history = tk.Listbox(main_frame, height=15, font=("Arial", 12))
history.pack(side="right", fill="y", padx=(5, 0))

app.mainloop()
