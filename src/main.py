from textual.app import App
from textual.app import ThemeProvider
from textual.widgets import Header, Footer, Static, Label
from textual.containers import Horizontal, Vertical, Container

from app import AppHeader, AppBody

class MusicApp(App):
    CSS_PATH = "styles.tcss"
    
    COMMANDS = {ThemeProvider}   

    BINDINGS = [
        ("/", "search", "search"),
        ("q", "quit", "quit")
    ]

    def compose(self):
        with Container():
            yield AppHeader(id="title-bar")
            yield AppBody(id="app")
        
        yield Footer()

    def on_mount(self):
        # self.theme = "catppuccin-macchiato"
        self.theme = "nord"

    def action_search(self):
        search = self.query_one("#search")
        search.focus()

if __name__ == "__main__":
    MusicApp().run()
