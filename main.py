import os
import random
import tkinter as tk
import argostranslate.package
import argostranslate.translate
import unicodedata
import logging

# Setup logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Tkinter window
root = tk.Tk()
root.geometry('700x700')
root.title('Перекладач')
root.resizable(False, False)

# Set the language codes for translation
from_code = "uk"
to_code = "en"

# Update and install the translation package
logging.info("Updating package index and installing translation package...")
argostranslate.package.update_package_index()
available_packages = argostranslate.package.get_available_packages()

# Select the correct translation package
package_to_install = next(
    filter(
        lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
    )
)
argostranslate.package.install_from_path(package_to_install.download())

# Function to load words from a file
def load_words_from_file(file_path):
    """
    This function loads words from a file and returns them as a list.
    If the file is not found, it logs a warning and returns an empty list.
    """
    try:
        with open(file_path, 'r') as file:
            words = file.readlines()
        logging.info(f"Loaded {len(words)} words from file {file_path}")
        return [word.strip() for word in words]
    except FileNotFoundError:
        logging.warning(f"File {file_path} not found.")
        return []

# Function to get random words from the loaded list
def get_random_words(words, count=10):
    """
    This function returns a random sample of words from the provided list.
    The sample size is capped to the number of words available.
    """
    if len(words) < 10:
        count = len(words)
    return random.sample(words, count)

# Function to write translation history to a file
def write_history(item):
    """
    This function appends a translation to the history file if it doesn't already exist.
    """
    try:
        with open("translate_history.txt", "r") as translate_history_file:
            translate_history = translate_history_file.read().splitlines()
        if item not in translate_history:
            translate_history.append(item)
            with open("translate_history.txt", "w") as translate_history_file:
                translate_history_file.write('\n'.join(translate_history))
            logging.info(f"Added '{item}' to translation history.")
    except FileNotFoundError:
        with open("translate_history.txt", "w") as translate_history_file:
            translate_history_file.write(item)
        logging.info(f"Created new history file and added '{item}'.")

# Function to perform translation
def translate(event=None, word=None):
    """
    This function performs translation from Ukrainian to English. It splits the input into words and translates each one.
    """
    if word is None:
        word = prompt_obj.get()
    words = word.split()  # Split the input into words (separated by spaces)
    logging.info(f"Translating words: {words}")

    try:
        # Translate each word individually
        translated_words = []
        for w in words:
            translated_word = argostranslate.translate.translate(w, from_code, to_code)
            translated_words.append(translated_word)
            logging.info(f"Translated '{w}' to '{translated_word}'")

        # Join the translated words into a single string
        result = " ".join(translated_words)
        logging.info(f"Translation result: {result}")
        translate_sign.config(text=f"Переклад: {result}")
        write_history(word)
    except Exception as e:
        logging.error(f"Error during translation: {e}")
        translate_sign.config(text="Переклад: ERR_UNKNOWN_WORLD")

# Function for quick translation from history
def quick_translate(i):
    """
    This function handles quick translation by populating the input field with the selected word.
    """
    prompt_obj.delete(0, tk.END)
    prompt_obj.insert(0, i)
    logging.info(f"Quick translate selected: {i}")

# Function to clear the prompt field
def clear_prompt(event=None):
    """
    This function clears the translation result display.
    """
    translate_sign.config(text="Переклад: ERR_UNKNOWN_WORLD")

# Function to clear the translation history
def clear_history():
    """
    This function clears the translation history and removes the history file.
    """
    for i in quick_translate_btns:
        i.destroy()
    quick_translate_title.config(text="Історія перекладів поки що відсутня або виникла помилка при зчитуванні :(")
    os.remove("translate_history.txt")

# UI elements for the Tkinter interface
prompt_help_sign = tk.Label(root, text="Уведіть будь-яке українське слово у це поле: ", font=('Arial', 14))
prompt_help_sign.pack()

tk.Label(root, font=("Arial", 1)).pack()  # Spacing

prompt_obj = tk.Entry(root, font=('Arial', 12))
prompt_obj.pack()
prompt_obj.bind("<Return>", translate)
prompt_obj.bind("<KeyPress>", clear_prompt)

tk.Label(root, font=("Arial", 10)).pack()  # Spacing

prompt_submit = tk.Button(root, font=('Arial', 14), text="Перекласти", command=translate)
prompt_submit.pack()

tk.Label(root, font=("Arial", 30)).pack()  # Spacing

translate_sign = tk.Label(root, text="Переклад: ERR_UNKNOWN_WORLD", font=("Arial", 15), fg="green")
translate_sign.pack()

tk.Label(root, font=("Arial", 30)).pack()  # Spacing

quick_translate_title = tk.Label(root, text="Історія перекладів:", font=("Arial", 15))
quick_translate_title.pack()

# Loading translation history
if "translate_history.txt" not in os.listdir("./"):
    quick_translate_title.config(text="Історія перекладів поки що відсутня або виникла помилка при зчитуванні :(")
else:
    # Read and get random words for quick translation buttons
    x = load_words_from_file('translate_history.txt')
    y = get_random_words(x)
    quick_translate_btns = []
    for i in y:
        logging.info(f"Creating quick translate button for: {i}")
        button = tk.Button(root, text=i, command=lambda i=i: quick_translate(i))
        quick_translate_btns.append(button)
        button.pack()

    tk.Label(root, font=("Arial", 30)).pack()  # Spacing

    clear_history_btn = tk.Button(root, text="ОЧИСТИТИ ІСТОРІЮ ПЕРЕКЛАДІВ", font=("Arial", 15), command=clear_history)
    clear_history_btn.pack()

# Start the Tkinter main loop
root.mainloop()
