import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime
from zxcvbn import zxcvbn

# Leetspeak substitutions
LEET_MAP = {
    'a': ['4', '@'],
    'e': ['3'],
    'i': ['1', '!'],
    'o': ['0'],
    's': ['$', '5'],
    't': ['7'],
}

def leetspeak_variants(word):
    def helper(w, index):
        if index >= len(w):
            return ['']
        c = w[index]
        subs = LEET_MAP.get(c.lower(), [c])
        tail_variants = helper(w, index + 1)
        results = []
        for sub in subs:
            for tail in tail_variants:
                results.append(sub + tail)
        return results
    return helper(word, 0)

def generate_custom_wordlist(inputs, years_range=(2000, datetime.now().year + 1)):
    base_words = set()
    for item in inputs:
        item = item.lower()
        base_words.add(item)
        base_words.update(leetspeak_variants(item))
    base_words = list(base_words)

    wordlist = set(base_words)
    for word in base_words:
        for year in range(*years_range):
            wordlist.add(f"{word}{year}")
            wordlist.add(f"{year}{word}")
    return sorted(wordlist)

def analyze_password(password):
    return zxcvbn(password)

def save_wordlist(wordlist):
    filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if filepath:
        with open(filepath, 'w') as f:
            for word in wordlist:
                f.write(word + "\n")
        messagebox.showinfo("Success", f"Wordlist saved to:\n{filepath}")

# GUI setup
def create_gui():
    root = tk.Tk()
    root.title("🔐 Password Analyzer & Wordlist Generator")
    root.geometry("550x600")
    root.configure(bg="#1e1e2f")

    # Fonts & colors
    font_title = ("Helvetica", 18, "bold")
    font_label = ("Helvetica", 12)
    font_result = ("Courier", 10)
    color_fg = "#f0f0f0"
    entry_bg = "#2e2e3e"
    button_bg = "#007acc"
    button_fg = "#ffffff"

    # Title
    tk.Label(root, text="Password Strength Analyzer", font=font_title, bg="#1e1e2f", fg="#70db70").pack(pady=15)

    # Password Input
    tk.Label(root, text="Enter Password:", font=font_label, bg="#1e1e2f", fg=color_fg).pack()
    password_entry = tk.Entry(root, show='*', font=font_label, bg=entry_bg, fg=color_fg, insertbackground=color_fg)
    password_entry.pack(pady=5, ipadx=5)

    result_label = tk.Label(root, text="", wraplength=520, bg="#1e1e2f", fg="#f5c542", font=font_result)
    result_label.pack(pady=10)

    def analyze():
        pwd = password_entry.get()
        if not pwd:
            messagebox.showwarning("Missing", "Please enter a password.")
            return
        result = analyze_password(pwd)
        score = result['score']
        time = result['crack_times_display']['offline_fast_hashing_1e10_per_second']
        feedback = result['feedback']
        result_label.config(
            text=f"Score: {score} / 4\nCrack Time: {time}\nFeedback: {feedback.get('warning', '')} {' '.join(feedback.get('suggestions', []))}"
        )

    tk.Button(root, text="Analyze Password", font=font_label, bg=button_bg, fg=button_fg, command=analyze).pack(pady=8)

    # Inputs for wordlist
    for label_text, var_name in [
        ("Name:", "name_entry"),
        ("Birth Year or Important Date:", "date_entry"),
        ("Pet Name:", "pet_entry")
    ]:
        tk.Label(root, text=label_text, font=font_label, bg="#1e1e2f", fg=color_fg).pack()
        globals()[var_name] = tk.Entry(root, font=font_label, bg=entry_bg, fg=color_fg, insertbackground=color_fg)
        globals()[var_name].pack(pady=5, ipadx=5)

    def generate_wordlist():
        name = name_entry.get()
        date = date_entry.get()
        pet = pet_entry.get()

        if not any([name, date, pet]):
            messagebox.showwarning("Missing", "Enter at least one input.")
            return

        custom_inputs = list(filter(None, [name, date, pet]))
        wordlist = generate_custom_wordlist(custom_inputs)
        save_wordlist(wordlist)

    tk.Button(root, text="Generate & Save Wordlist", font=font_label, bg="#ff5733", fg=button_fg, command=generate_wordlist).pack(pady=20)

    root.mainloop()

# Start GUI
if __name__ == "__main__":
    create_gui()
