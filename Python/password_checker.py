"""Password strength checker.

Usage:
    python Python/password_checker.py
    (it will prompt to enter a password; press Enter to run demo samples)

Functions:
 - `score_password(password)`: returns (score:int, suggestions:list[str])
 - CLI that hides input and prints a short strength report + suggestions
"""
from __future__ import annotations
import re
import getpass
from typing import List, Tuple

COMMON_PASSWORDS = {
    'password', '123456', '123456789', 'qwerty', 'abc123', 'password1', '111111',
}

SYMBOL_RE = re.compile(r"[!@#$%^&*()_+\-=[\]{};':\",.<>/?\\|`~]")


def score_password(pw: str) -> Tuple[int, List[str]]:
    """Score the password and return (score, suggestions).

    Score range roughly 0-100.
    """
    suggestions: List[str] = []
    if not pw:
        return 0, ["Password is empty"]

    score = 0

    length = len(pw)
    # length contribution
    if length >= 12:
        score += 30
    elif length >= 8:
        score += 20
    elif length >= 6:
        score += 10
    else:
        score += 0

    # character variety
    upper = any(c.isupper() for c in pw)
    lower = any(c.islower() for c in pw)
    digit = any(c.isdigit() for c in pw)
    symbol = bool(SYMBOL_RE.search(pw))

    variety = sum((upper, lower, digit, symbol))
    score += variety * 10

    # penalize simple repeats or sequential characters
    if re.search(r'(.)\1{2,}', pw):
        suggestions.append('Avoid repeated characters like "aaa" or "111"')
        score -= 10

    if re.search(r'(?:012|123|234|345|456|567|678|789|abc|bcd|cde|qwe)', pw.lower()):
        suggestions.append('Avoid obvious sequences like "123" or "abc"')
        score -= 10

    # common password check
    if pw.lower() in COMMON_PASSWORDS:
        suggestions.append('This password is commonly used — choose a less common one')
        score = max(score - 40, 0)

    # mixture bonus
    if upper and lower and digit and symbol and length >= 12:
        score += 20

    # clamp
    score = max(0, min(100, score))

    # constructive suggestions
    if length < 12:
        suggestions.append('Increase length to at least 12 characters')
    if not upper:
        suggestions.append('Add uppercase letters (A-Z)')
    if not lower:
        suggestions.append('Add lowercase letters (a-z)')
    if not digit:
        suggestions.append('Add digits (0-9)')
    if not symbol:
        suggestions.append('Add symbols (e.g. !@#$%)')

    if not suggestions:
        suggestions.append('No suggestions: strong password')

    return score, suggestions


def describe(score: int) -> str:
    if score < 20:
        return 'Very weak'
    if score < 40:
        return 'Weak'
    if score < 60:
        return 'Moderate'
    if score < 80:
        return 'Strong'
    return 'Very strong'


def run_interactive() -> None:
    print('Password Strength Checker')
    print('Enter a password (input hidden). Press Enter with no input to run demo samples.')
    try:
        pw = getpass.getpass('Password: ')
    except (KeyboardInterrupt, EOFError):
        print('\nAborted')
        return

    samples = [pw] if pw else [
        'password', 'Summer2023', 'S3cure!Passw0rd', 'abc123', 'qwerty!!', 'P@55w0rdLonger'
    ]

    for p in samples:
        score, suggestions = score_password(p)
        print('\nPassword:', p)
        print('Score:', score, f'({describe(score)})')
        print('Suggestions:')
        for s in suggestions[:5]:
            print('-', s)


if __name__ == '__main__':
    run_interactive()
