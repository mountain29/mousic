from textual.app import App
from textual.app import ThemeProvider
from textual.widgets import Header, Footer, Static, Label
from textual.containers import Horizontal, Vertical, Container

from app import AppHeader, AppBody

class MusicApp(App):
    CSS_PATH = "styles.tcss"
    
    COMMANDS = {ThemeProvider}   

    BINDINGS = [
        ("z", "back", "Back"),
        ("q", "quit", "Quit")
    ]

    def compose(self):
        with Container():
            yield AppHeader(id="title-bar")
            yield AppBody()
        
        yield Footer()

if __name__ == "__main__":
    MusicApp().run()
