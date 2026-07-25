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
            yield ActionPane(id="action-pane", classes="pane")

        with Vertical(id="right-section"):
            yield QueuePane(id="queue-pane", classes="pane")
            yield StatusPane(id="status-pane", classes="pane")

class ActionPane(Vertical):

    can_focus = True

    ACTIONS = Actions.get_actions()
    selected_action_index = 0
    selected_subaction_index = -1

    FOCUS_CYCLE = deque([ActionFocus.ACTION, ActionFocus.SUB_ACTION, ActionFocus.CONTENT])

    def compose(self) -> ComposeResult:
        with Horizontal(id="action-navigation"):

            with Vertical(id="actions"):
                for action in self.ACTIONS:
                    if action == self.ACTIONS[self.selected_action_index]:
                        yield Label(f"♪ [b]{action.display_name}[/]", classes="action-label")
                    else:
                        yield Label(f"[dim]{action.display_name}[/]", classes="action-label")

            with Vertical(id="sub-actions"):
                for sub_action in self._get_subactions():
                    yield Label(f"[dim]{sub_action.display_name}[/]", classes="subaction-label")

        with Vertical(id="action-content"):
            yield Label("content")
    
    def on_key(self, event) -> None:

        if event.key in ["up", "down"]:
            match self.FOCUS_CYCLE[0]:
                case ActionFocus.ACTION:

                    if event.key == "up":
                        self.selected_action_index = (self.selected_action_index - 1) % len(self.ACTIONS)
                    elif event.key == "down":
                        self.selected_action_index = (self.selected_action_index + 1) % len(self.ACTIONS)

                case ActionFocus.SUB_ACTION:

                    sub_actions = self._get_subactions()
                    if event.key == "up":
                        self.selected_subaction_index = (self.selected_subaction_index - 1) % len(sub_actions)
                    elif event.key == "down":
                        self.selected_subaction_index = (self.selected_subaction_index + 1) % len(sub_actions)
        else:
            if event.key == "z":
                if self.FOCUS_CYCLE[0] == ActionFocus.CONTENT:
                    pass
                else:
                    if self.FOCUS_CYCLE[0] == ActionFocus.ACTION:
                        self.selected_subaction_index = 0

                    self.FOCUS_CYCLE.rotate(-1)

            elif event.key == "x" and self.FOCUS_CYCLE[0] != ActionFocus.ACTION:
                if self.FOCUS_CYCLE[0] == ActionFocus.SUB_ACTION:
                    self.selected_subaction_index = -1

                self.FOCUS_CYCLE.rotate(1)

        self._update_action_labels()
        self._update_subaction_labels()

    def _update_action_labels(self) -> None:
        for i, label in enumerate(self.query(".action-label")):
            if i == self.selected_action_index:
                prefix = "♪ " if self.FOCUS_CYCLE[0] == ActionFocus.ACTION else ""
                label.update(f"{prefix}[b]{self.ACTIONS[i].display_name}[/]")
            else:
                label.update(f"[dim]{self.ACTIONS[i].display_name}[/]")

    def _update_subaction_labels(self) -> None:
        container = self.query_one("#sub-actions")
        container.remove_children()

        labels = []
        for i,sub_action in enumerate(self._get_subactions()):
            if i == self.selected_subaction_index:
                prefix = "♪ " if self.FOCUS_CYCLE[0] == ActionFocus.SUB_ACTION else ""
                labels.append(Label(f"{prefix}[b]{sub_action.display_name}[/]", classes="subaction-label"))
            else:
                labels.append(Label(f"[dim]{sub_action.display_name}[/]", classes="subaction-label"))

        container.mount(*labels)

    def on_focus(self, event: Focus) -> None:
        self.border_title = "Actions"
        self.add_class("focused")
        self.remove_class("blurred")
    
    def on_blur(self, event: Blur) -> None:
        self.border_title = ""
        self.add_class("blurred")
        self.remove_class("focused")

    def _get_subactions(self) -> tuple:
        return self.ACTIONS[self.selected_action_index].sub_actions

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

