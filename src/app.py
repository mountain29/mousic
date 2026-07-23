from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Label
from textual.containers import Horizontal, Vertical, Container
from textual.events import Focus, Blur

class AppHeader(Horizontal):
    def compose(self):
        yield Label("[b]Mou's Music Player[/]", id="app-title")
        yield Label("[dim]Demo[/]", id="app-version")

class AppBody(Container):

    def compose(self):
        with Horizontal(id="main-section"):
            
            yield ActionPane(id="action-pane", classes="pane")
            
            yield ContentPane(id="content-pane", classes="pane")

        with Vertical(id="bottom-section"):
            yield StatusPane(id="status-pane", classes="pane")

class ActionPane(Vertical):

    can_focus = True

    ACTIONS = ["Play", "Add", "Playlists", "Favorited", "Edit Queue"]
    selected_action = 0

    def compose(self) -> ComposeResult:
        self.border_title = "Actions"

        for i in self.ACTIONS:
            if i == self.ACTIONS[self.selected_action]:
                yield Label(f"[b]{i}[/] 👈", classes="action-label")
            else:
                yield Label(f"[dim]{i}[/]", classes="action-label")
    
    def on_key(self, event) -> None:
        if event.key == "up":
            self.selected_action = (self.selected_action - 1) % len(self.ACTIONS)
        elif event.key == "down":
            self.selected_action = (self.selected_action + 1) % len(self.ACTIONS)
        self._update_action_labels()

    def _update_action_labels(self) -> None:
        for i, label in enumerate(self.query(".action-label")):
            if i == self.selected_action:
                label.update(f"[b]{self.ACTIONS[i]}[/] 👈")
            else:
                label.update(f"[dim]{self.ACTIONS[i]}[/]")

    def on_focus(self, event: Focus) -> None:
        self.border_title = "Actions"
        self.add_class("focused")
    
    def on_blur(self, event: Blur) -> None:
        self.border_title = ""
        self.remove_class("focused")


class ContentPane(Vertical):

    can_focus = True

    def compose(self) -> ComposeResult:
        self.border_title = "Content"
        yield Label("🦗 Empty Queue 🦗", id="content-label")

    def on_focus(self, event: Focus) -> None:
        self.border_title = "Content"
        self.add_class("focused")
    
    def on_blur(self, event: Blur) -> None:
        self.border_title = ""
        self.remove_class("focused")

class StatusPane(Horizontal):
    can_focus = True

    def compose(self) -> ComposeResult:
        self.border_title = "Status"
        yield Label("", id="content-label")

    def on_focus(self, event: Focus) -> None:
        self.border_title = "Content"
        self.add_class("focused")
    
    def on_blur(self, event: Blur) -> None:
        self.border_title = ""
        self.remove_class("focused")