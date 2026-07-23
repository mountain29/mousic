from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, ListView, ListItem, Label

class SearchApp(App):
    CSS = """
    Input { margin-bottom: 1; }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder="🔍 Type song name & press Enter...", id="search-input")
        yield ListView(id="results-list")
        yield Footer()

    # Triggered when user presses ENTER inside the Input box
    @on(Input.Submitted, "#search-input")
    def handle_search(self, event: Input.Submitted) -> None:
        query = event.value
        results_list = self.query_one("#results-list", ListView)
        results_list.clear()

        # Simulate adding search results
        if query:
            results_list.append(ListItem(Label(f"▶ {query} - Original Track")))
            results_list.append(ListItem(Label(f"▶ {query} - Acoustic Cover")))
            results_list.append(ListItem(Label(f"▶ {query} - Remix")))
            self.notify(f"Search results updated for: {query}")

    # Triggered when user selects an item from the ListView
    @on(ListView.Selected, "#results-list")
    def handle_song_select(self, event: ListView.Selected) -> None:
        # Get label text from selected ListItem
        label = event.item.query_one(Label).renderable
        self.notify(f"Selected: {label}", title="Now Playing")

if __name__ == "__main__":
    SearchApp().run()