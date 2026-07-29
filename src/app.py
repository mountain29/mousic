from collections import deque
from typing import Any

from enums import ActionFocus, Actions
from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.events import Blur, Focus
from textual.screen import ModalScreen
from textual.widgets import DataTable, Footer, Header, Input, Label, Static
from youtube import yt
from tools import toolbox

class AppHeader(Horizontal):

    def compose(self):
        yield Label("[b]Mousic[/]", id="app-title")
        yield Label("[dim]Demo[/]", id="app-version")


class AppBody(Vertical):

    songs_data = {}

    def compose(self):
        with Horizontal(id="playback"):
            yield ThumbnailPane(id="thumbnail-pane", classes="pane")
            yield PlayerPane(id="player-pane", classes="pane")
            yield InfoPane(id="info-pane", classes="pane")

        with Horizontal(id="workspace"):
            with Vertical(id="details"):
                yield LyricsPane(id="lyrics-pane", classes="pane")
                yield QueuePane(id="queue-pane", classes="pane")

            yield BrowserPane(id="browser-pane", classes="pane")

    @on(DataTable.RowSelected, "#search-result")
    def on_search_result_selected(self, event: DataTable.RowSelected) -> None:

        queue: DataTable = self.query_one("#queue", DataTable)
        index = queue.row_count + 1

        row_key = event.row_key
        if row_key.value == "disabled": return

        print(self.songs_data)
        print(row_key.value)

        title = self.songs_data[row_key.value]["title"]
        isExplicit = self.songs_data[row_key.value]["isExplicit"]
        cropped_title = toolbox.truncate_text(title, 40, isExplicit, index)

        queue.add_row(
            cropped_title,
        )

        queue.move_cursor(row=queue.row_count - 1)

    @on(Input.Submitted, "#search")
    def handle_search(self, event: Input.Submitted):
        search_result: DataTable = self.query_one("#search-result", DataTable)
        search_result.clear()
        search_result.add_row("Please wait...", "", key="disabled")
        search_result.focus()

        self.fetch_songs(event.value)

    @work(exclusive=True, thread=True)
    def fetch_songs(self, query: str):

        songs = yt.search(query, 15)
        self.app.call_from_thread(self._update_search_result, songs)

    def _update_search_result(self, songs: list[dict]):
        search_result: DataTable = self.query_one("#search-result", DataTable)
        search_result.clear()

        if songs == []:
            search_result.add_row("No songs found .__.;;", key="disabled")
            return

        for s in songs:
            videoId = s["videoId"]
            title = s["title"]
            artists = ", ".join(artist["name"] for artist in s["artists"])
            duration = s["duration"]
            duration_seconds = s["duration_seconds"]
            isExplicit = s["isExplicit"]

            cropped_title = toolbox.truncate_text(title, 35, isExplicit)
            cropped_artists = toolbox.truncate_text(artists, 20)

            key = len(self.songs_data)
            search_result.add_row(
                f"[b]{cropped_title}[/]", f"[dim]{cropped_artists}[/]", key=key
            )

            self.songs_data[key] = {
                "videoId": videoId,
                "title": title,
                "artists": artists,
                "duration": duration,
                "duration_seconds": duration_seconds,
                "isExplicit": isExplicit,
            }


class ThumbnailPane(Vertical):

    def compose(self):
        yield Label("")


class PlayerPane(Vertical):

    def on_mount(self):
        self.border_title = "player"


class InfoPane(Vertical):

    def compose(self):
        yield Label("")


class LyricsPane(Horizontal):

    can_focus = True

    def compose(self):
        yield Label("")

    def on_mount(self):
        self.border_title = "lyrics"

class QueuePane(Horizontal):

    def compose(self):
        yield DataTable(id="queue")

    def on_mount(self):
        self.border_title = "queue"
        queue = self.query_one("#queue", DataTable)
        queue.show_header = False 
        queue.cursor_type = "row"
        queue.add_column("Title", key="title")
        queue.zebra_stripes = True


class BrowserPane(Vertical):

    def compose(self):
        yield SearchBar(id="search")
        yield SearchResult(id="search-result")

    def on_mount(self):
        self.border_title = "browser"


# Tools
class SearchBar(Input):

    def on_mount(self):
        self.placeholder = "Search song name, artist"


class SearchResult(DataTable):

    def on_mount(self):
        self.show_header = False
        self.cursor_type = "row"
        self.zebra_stripes = True

        self.add_column("Title", key="title")
        self.add_column("Artists", key="artists")
