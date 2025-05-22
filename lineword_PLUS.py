import itertools
from datetime import datetime
import os
import sys

def display_banner():
    print(r"""
  ___      __ _       _ _     _     _____          _        
 / __|___ / _(_)_ __ | (_)___| |_  |_   _|__  ___| |_ ___  
| (_ / -_)  _| | '  \| | / -_)  _|   | |/ _ \/ _ \  _/ -_) 
 \___\___|_| |_|_|_|_|_|_\___|\__|   |_|\___/\___/\__\___| 
    """)
    print("[ PLUS | telegram: @scriptshops_ir ]".center(50, "="))
    print("")

def get_base_words():
    print("\n[1] Input Method Selection")
    print("1. Manual entry (comma-separated)")
    print("2. Read from file")
    print("3. Use common defaults")
    
    while True:
        choice = input("> Select option (1-3): ")
        if choice in ["1", "2", "3"]:
            break
        print("Invalid choice")
    
    if choice == "1":
        words_input = input("> Enter words: ")
        return [word.strip() for word in words_input.split(",") if word.strip()]
    elif choice == "2":
        while True:
            filename = input("> Enter filename: ")
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    return [line.strip() for line in f if line.strip()]
            print("File not found")
    else:
        return ["admin", "user", "password", "root", "login"]

def get_save_path():
    default = os.path.join(os.getcwd(), "wordlist.txt")
    print(f"\n[2] Save Location (default: {default})")
    path = input("> Enter path: ")
    return path if path else default

def generate_combinations(base_words):
    numbers = ["", "123", "1234", "123456", "2023", "2024", "1", "12", "12345"]
    symbols = ["", "!", "$", "%", "&", "*", "_", "-"]
    current_year = datetime.now().year
    dates = [str(current_year), f"01{current_year}", "0101", "1010", "2020"]
    
    for word in base_words:
        for num in numbers:
            combo = f"{word}{num}"
            if len(combo) >= 4:
                yield combo
                yield combo.capitalize()
        
        for sym in symbols:
            if sym:
                for num in numbers:
                    combo = f"{word}{sym}{num}"
                    if len(combo) >= 4:
                        yield combo
                        yield combo.capitalize()
        
        for date in dates:
            combo = f"{word}{date}"
            if len(combo) >= 4:
                yield combo
                yield combo.capitalize()
            for sym in symbols:
                if sym:
                    combo = f"{word}{date}{sym}"
                    if len(combo) >= 4:
                        yield combo
                        yield combo.capitalize()

def generate_wordlist():
    display_banner()
    
    base_words = get_base_words()
    if not base_words:
        print("No words provided")
        return
    
    save_path = get_save_path()
    total = 0
    
    print("\n[3] Generation Options")
    print("1. Basic combinations")
    print("2. All combinations")
    choice = input("> Select mode: ")
    
    print("\nGenerating wordlist...")
    with open(save_path, "w") as f:
        for combo in generate_combinations(base_words):
            if "#" not in combo and "?" not in combo:
                f.write(f"{combo}\n")
                total += 1
                if total % 1000 == 0:
                    print(f"Generated {total}", end="\r")
    
    print(f"\n\nGenerated {total} combinations")
    print(f"Saved to: {os.path.abspath(save_path)}")

if __name__ == "__main__":
    try:
        generate_wordlist()
    except KeyboardInterrupt:
        print("\nCancelled")
        sys.exit(1)