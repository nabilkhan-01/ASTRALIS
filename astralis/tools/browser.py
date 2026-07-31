import webbrowser


class BrowserTool:
    """Provides browser-related functionality."""

    def open(
        self,
        url: str,
    ) -> bool:
        """Open a URL in the user's default web browser."""

        if not url.strip():
            return False

        return webbrowser.open(
            url,
        )
