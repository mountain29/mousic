from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Label
from textual.containers import Horizontal, Vertical, Container
from textual.events import Focus, Blur

from enums import Actions

class AppHeader(Horizontal):
    def compose(self):
        yield Label("[b]Mousic[/]", id="app-title")
        yield Label("[dim]Demo[/]", id="app-version")

class AppBody(Horizontal):

    def compose(self):
        with Vertical(id="left-section"):
            yield ActionPane(id="action-pane", classes="pane")

        with Vertical(id="right-section"):
            yield QueuePane(id="queue-pane", classes="pane")
            yield StatusPane(id="status-pane", classes="pane")

class ActionPane(Vertical):

    can_focus = True


    # ACTIONS = ["Play", "Add", "Playlists", "Favorited", "Edit Queue"]
    ACTIONS = Actions.get_actions()
    selected_action_index = 0

    def compose(self) -> ComposeResult:
        with Horizontal(id="action-navigation"):

            with Vertical(id="actions"):
                for action in self.ACTIONS:
                    if action == self.ACTIONS[self.selected_action_index]:
                        yield Label(f"♪ [b]{action.display_name}[/]", classes="action-label")
                    else:
                        yield Label(f"[dim]{action.display_name}[/]", classes="action-label")

            with Vertical(id="sub-actions"):
                for sub_action in self.ACTIONS[self.selected_action_index].sub_actions:
                    yield Label(f"[dim]{sub_action.display_name}[/]", classes="subaction-label")

        with Vertical(id="action-content"):
            yield Label("content")
    
    def on_key(self, event) -> None:
        if event.key == "up":
            self.selected_action_index = (self.selected_action_index - 1) % len(self.ACTIONS)
        elif event.key == "down":
            self.selected_action_index = (self.selected_action_index + 1) % len(self.ACTIONS)

        self._update_action_labels()
        self._update_subaction_labels()

    def _update_action_labels(self) -> None:
        for i, label in enumerate(self.query(".action-label")):
            if i == self.selected_action_index:
                label.update(f"♪ [b]{self.ACTIONS[i].display_name}[/]")
            else:
                label.update(f"[dim]{self.ACTIONS[i].display_name}[/]")

    def _update_subaction_labels(self) -> None:
        container = self.query_one("#sub-actions")
        container.remove_children()

        labels = [
            Label(f"[dim]{sub_action.display_name}[/]", classes="subaction-label") 
            for sub_action in self.ACTIONS[self.selected_action_index].sub_actions
        ]

        container.mount(*labels)

    def on_focus(self, event: Focus) -> None:
        self.border_title = "Actions"
        self.add_class("focused")
        self.remove_class("blurred")
    
    def on_blur(self, event: Blur) -> None:
        self.border_title = ""
        self.add_class("blurred")
        self.remove_class("focused")

    

class QueuePane(Horizontal):

    can_focus = True

    def compose(self) -> ComposeResult:
        self.add_class("blurred")
        yield Label("🦗   Empty Queue   🦗", id="content-label")

    def on_focus(self, event: Focus) -> None:
        self.border_title = "Queue"
        self.add_class("focused")
        self.remove_class("blurred")
    
    def on_blur(self, event: Blur) -> None:
        self.border_title = ""
        self.add_class("blurred")
        self.remove_class("focused")

class StatusPane(Horizontal):
    can_focus = True

    def compose(self) -> ComposeResult:
        self.add_class("blurred")
        yield Label("", id="content-label")

    def on_focus(self, event: Focus) -> None:
        self.border_title = "Status"
        self.add_class("focused")
        self.remove_class("blurred")
    
    def on_blur(self, event: Blur) -> None:
        self.border_title = ""
        self.add_class("blurred")
        self.remove_class("focused")

