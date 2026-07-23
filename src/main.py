from textual.app import App
from textual.app import ThemeProvider
from textual.widgets import Header, Footer, Static, Label
from textual.containers import Horizontal, Vertical, Container

from app import AppHeader, AppBody

class MusicApp(App):
    CSS_PATH = "styles.tcss"
    
    COMMANDS = {ThemeProvider}   

    BINDINGS = [
        ("z", "back", "Back")
    ]

    def compose(self):
        with Container(id="app-container"):
            yield AppHeader(id="top-section")
            yield AppBody()
        
        yield Footer()

if __name__ == "__main__":
    MusicApp().run()
