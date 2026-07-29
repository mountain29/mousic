from textual.app import App, ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Header, Footer, Static, Label, Input, OptionList
from textual.widgets.option_list import Option
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
        with Horizontal(id="playback"):
            yield ThumbnailPane(id="thumbnail-pane",classes="pane")
            yield PlayerPane(id="player-pane",classes="pane")
            yield InfoPane(id="info-pane",classes="pane")

        with Horizontal(id="workspace"):

            with Vertical(id="details"):
                yield LyricsPane(id="lyrics-pane",classes="pane")
                yield QueuePane(id="queue-pane",classes="pane")

            yield BrowserPane(id="browser-pane", classes="pane")

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        if event.option_list.id == "search-result":
            queue = self.query_one("#queue")
            index = len(queue.options)+1
            label = f"{index}. {event.option.prompt[:30]}"
            queue.add_option(Option(label))
            queue.highlighted = index-1
            queue.scroll_to_highlight()

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
        yield OptionList(id="queue")
    def on_mount(self):
        self.border_title = "queue"


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

class SearchResult(OptionList):
    def on_mount(self):
        tracks = [
            {"title": "Fuwa Fuwa Time", "artist": "Sakurakou K-ON Bu", "url": "https://youtu.be/k1"},
            {"title": "Cagayake! GIRLS", "artist": "HTT (K-ON!)", "url": "https://youtu.be/k2"},
            {"title": "Gunjou", "artist": "YOASOBI", "url": "https://youtu.be/y1"},
            {"title": "KICK BACK", "artist": "Kenshi Yonezu", "url": "https://youtu.be/ky1"},
            {"title": "Nàng Thơ", "artist": "Hoàng Dũng", "url": "https://youtu.be/v1"},
            {"title": "Chờ Anh Nhé", "artist": "Hoàng Dũng ft. Hà Anh Tuấn", "url": "https://youtu.be/v2"},
        ]

        self.clear_options()

        options = []
        for t in tracks:
            title = t['title'][:30].ljust(32)
            artist = t['artist']
            
            label = f"[b]{title}[/] [dim]{artist}[/]"
            options.append(Option(label, id=t['url']))

        self.add_options(options)
