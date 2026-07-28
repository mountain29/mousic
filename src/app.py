from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Label
from textual.containers import Horizontal, Vertical, Container
from textual.events import Focus, Blur

from collections import deque

from enums import Actions, ActionFocus

class AppHeader(Horizontal):
    def compose(self):
        yield Label("[b]Mousic[/]", id="app-title")
        yield Label("[dim]Demo[/]", id="app-version")

class AppBody(Horizontal):

    def compose(self):
        with Vertical(id="left-section"):
            # yield ActionPane(id="action-pane", classes="pane")

        with Vertical(id="right-section"):
            # yield QueuePane(id="queue-pane", classes="pane")
            # yield StatusPane(id="status-pane", classes="pane")