from dataclasses import dataclass
from enum import Enum, auto

class SubActionKey(Enum):
    ADD_FIND = auto()
    ADD_PLAYLIST = auto()
    ADD_RECOMMEND = auto()

    PLAYLISTS_NEW = auto()
    PLAYLISTS_MANAGE = auto()
    PLAYLISTS_IMPORT = auto()

    FAV_SONGS = auto()
    FAV_ARTISTS = auto()

@dataclass(frozen=True)
class SubActionMetadata:
    key: SubActionKey
    display_name: str
    description: str

class Actions(Enum):
    ADD = (
        "Add",
        (
            SubActionMetadata(
                SubActionKey.ADD_FIND,
                "Find",
                "Find songs by title or artist"
            ),
            SubActionMetadata(
                SubActionKey.ADD_PLAYLIST,
                "Playlist",
                "Add songs from a playlist"
            ),
            SubActionMetadata(
                SubActionKey.ADD_RECOMMEND,
                "Recommend",
                "Choose songs recommended by Last.fm API"
            )
        )
    )

    PLAYLISTS = (
        "Playlist",
        (
            SubActionMetadata(
                SubActionKey.PLAYLISTS_NEW,
                "New",
                "Create a new empty playlist"
            ),
            SubActionMetadata(
                SubActionKey.PLAYLISTS_MANAGE,
                "Manage",
                "Add songs from a playlist"
            ),
            SubActionMetadata(
                SubActionKey.PLAYLISTS_IMPORT,
                "Import",
                "Import an existing Youtube playlist"
            )
        )
    )

    FAVORITED = (
        "Favorited",
        (
            SubActionMetadata(
                SubActionKey.FAV_SONGS,
                "Songs",
                "Favorited songs"
            ),
            SubActionMetadata(
                SubActionKey.FAV_ARTISTS,
                "Artists",
                "Favorited artists"
            ),
        )
    )

    def __init__(self, display_name: str, sub_actions: tuple[SubActionMetadata, ...]):
        self.display_name = display_name
        self.sub_actions = sub_actions

    def get_actions() -> list[str]:
        return [action for action in Actions]

class ActionFocus(Enum):
    ACTION = auto()
    SUB_ACTION = auto()
    CONTENT = auto()
