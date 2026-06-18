import time

try:
    import keyboard
    import pyperclip
    import pyautogui
except Exception as e:
    print("Missing GUI/keyboard libraries:", e)
    print("Install requirements: pip install keyboard pyperclip pyautogui")
    raise

try:
    import ollama
except Exception:
    ollama = None


def ask_local():
    prompt = pyperclip.paste() or ""
    if not prompt.strip():
        print("Clipboard is empty — copy a prompt and try again.")
        return
    print("Triggered! Processing prompt...")

    if ollama is None:
        print("`ollama` library not available. Install or run ollama CLI instead.")
        return

    messages = [
        {
            "role": "system",
            "content": "You are a Python problem solver; always output complete mid‑level Python solutions using loops, conditionals, functions, lists, dictionaries, and string methods—no advanced libraries, no comments, only the code."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    try:
        res = ollama.chat(model="deepseek-coder-v2:16b", messages=messages)
    except Exception as e:
        print("Error calling ollama:", e)
        return

    # Support multiple response shapes
    answer = None
    if isinstance(res, dict):
        answer = res.get("message", {}).get("content") or res.get("content")
    # Some client objects return objects with attributes
    if answer is None and hasattr(res, "message"):
        msg = getattr(res, "message")
        answer = getattr(msg, "content", None)
    if answer is None:
        answer = str(res)

    # Type the answer character-by-character at the current cursor location
    time.sleep(0.2)
    try:
        pyautogui.write(answer, interval=0.01)
        # add a newline and a short completion message after the answer
        pyautogui.press("enter")
        pyautogui.write("done with it !!", interval=0.01)
    except Exception as e:
        print("Error typing response, falling back to clipboard paste:", e)
        pyperclip.copy(answer)
        time.sleep(0.2)
        pyautogui.hotkey("ctrl", "v")
        # After pasting, also add the completion message
        try:
            time.sleep(0.05)
            pyautogui.press("enter")
            pyautogui.write("done with it !!", interval=0.01)
        except Exception:
            pass
    print("Done!")


def main():
    keyboard.add_hotkey("ctrl+shift+x", ask_local)
    print("Ready — press Ctrl+Shift+X to trigger")
    keyboard.wait()


if __name__ == "__main__":
    main()