import re, os, click
from .constants import *

superscript_map = {
    "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶",
    "7": "⁷", "8": "⁸", "9": "⁹", "a": "ᵃ", "b": "ᵇ", "c": "ᶜ", "d": "ᵈ",
    "e": "ᵉ", "f": "ᶠ", "g": "ᵍ", "h": "ʰ", "i": "ᶦ", "j": "ʲ", "k": "ᵏ",
    "l": "ˡ", "m": "ᵐ", "n": "ⁿ", "o": "ᵒ", "p": "ᵖ", "q": "۹", "r": "ʳ",
    "s": "ˢ", "t": "ᵗ", "u": "ᵘ", "v": "ᵛ", "w": "ʷ", "x": "ˣ", "y": "ʸ",
    "z": "ᶻ", "A": "ᴬ", "B": "ᴮ", "C": "ᶜ", "D": "ᴰ", "E": "ᴱ", "F": "ᶠ",
    "G": "ᴳ", "H": "ᴴ", "I": "ᴵ", "J": "ᴶ", "K": "ᴷ", "L": "ᴸ", "M": "ᴹ",
    "N": "ᴺ", "O": "ᴼ", "P": "ᴾ", "Q": "Q", "R": "ᴿ", "S": "ˢ", "T": "ᵀ",
    "U": "ᵁ", "V": "ⱽ", "W": "ᵂ", "X": "ˣ", "Y": "ʸ", "Z": "ᶻ", "+": "⁺",
    "-": "⁻", "=": "⁼", "(": "⁽", ")": "⁾"}

current_dir = os.path.dirname(os.path.abspath(__file__))

superscript_pattern = re.compile(r"\^[A-Za-zÀ-ÖØ-öø-ÿ -]+\^")
correction_pattern = re.compile(r"\[\[(([A-Za-zÀ-ÖØ-öø-ÿ -]+\|[A-Za-zÀ-ÖØ-öø-ÿ -]+)|[A-Za-zÀ-ÖØ-öø-ÿ -]+)]]")
unreadable_pattern = re.compile(r"-\[[A-z -]+]-")

@click.command()
def clean_model():
    clean = os.path.join(current_dir, ALTO_BRUT)
    for file in os.listdir(os.path.join(current_dir, ALTO_BRUT)):
        with open(file, 'r') as f:
            xml = f.read()
        with open(f"{clean}/{file}", 'w') as write_file:
            for lines in xml.split('\n'):
                re.sub(correction_pattern, lines)


#use .group for regex si il y a plusieurs resultats dans une meme ligne