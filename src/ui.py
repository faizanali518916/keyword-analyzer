import os

import questionary
from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings
from rich.panel import Panel
from rich.text import Text
from rich import box

from .styles import console


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def banner():
    clear()
    console.print(
        Panel(
            Text("⌨  KEYWORD HELPER", justify="center", style="bold white"),
            subtitle="[dim]Interactive keyword management tool[/dim]",
            border_style="bright_magenta",
            box=box.DOUBLE_EDGE,
            padding=(1, 4),
        )
    )
    console.print()


def page_navigation(page_num, total_pages):
    """Wait for page navigation keys and return next, previous, or back."""
    if total_pages <= 1:
        questionary.press_any_key_to_continue().ask()
        return "back"

    bindings = KeyBindings()

    @bindings.add("left")
    def previous_page(event):
        event.app.exit(result="previous")

    @bindings.add("right")
    def next_page(event):
        event.app.exit(result="next")

    @bindings.add("enter")
    @bindings.add("escape")
    def return_to_menu(event):
        event.app.exit(result="back")

    console.print(
        f"[dim]  Page {page_num + 1}/{total_pages}  |  "
        "Left/Right: change page  |  Enter/Esc: back[/dim]"
    )
    try:
        return prompt("  ", key_bindings=bindings)
    except (EOFError, KeyboardInterrupt):
        return "back"
