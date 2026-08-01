class toolbox:

    def truncate_text(text: str, max_length: int = 35, isExplicit: bool = False, index: int = None, isPlaying: bool = False) -> str:
        if isExplicit:
            text = "[bold orange1]E [/]" + text
            max_length += 17

        if index is not None:
            text = f"{index}. " + text
            max_length += 2 + len(str(index))

        if isPlaying:
            text = "[bold green]▶ " + text + "[/]"
            max_length += 15

        if len(text) > max_length:
            return text[: max_length - 3].strip() + "..."
        return text