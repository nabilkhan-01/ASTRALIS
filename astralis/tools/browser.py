import webbrowser


class BrowserTool:
    """Opens web pages."""

    def open(
        self,
        url: str,
    ) -> bool:
        """Open a URL."""

        return webbrowser.open(
            url,
        )