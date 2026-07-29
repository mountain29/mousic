from textual.app import App, ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Header, Footer, Static, Label, Input
from textual.containers import Horizontal, Vertical, Container
from textual.events import Focus, Blur

from collections import deque

from enums import Actions, ActionFocus

class AppHeader(Horizontal):
    def compose(self):
        yield Label("[b]Mousic[/]", id="app-title")
        yield Label("[dim]Demo[/]", id="app-version")

class AppBody(Vertical):

    def compose(self):
        with Horizontal():
            yield Thumbnail(classes="border1")
            yield Player(classes="border1")

        with Horizontal():

            with Vertical():
                yield Lyrics(classes="border1")
                yield Queue(classes="border1")

            yield Browser(classes="border1")

class Thumbnail(Vertical):

    def compose(self):
        yield Label("img")


class Player(Vertical):

    def compose(self):
        yield Label("player")


class Lyrics(Horizontal):

    def compose(self):
        yield Label("lyrics")


class Queue(Horizontal):

    def compose(self):
        yield Label("queue")


class Browser(Vertical):

    def compose(self):
        yield Label("browser")