import requests

from astralis.api.search import SearchApi
from astralis.brain.conversation import Conversation
from astralis.brain.interpretation import Interpretation
from astralis.brain.request import Request
from astralis.brain.response import Response
from astralis.capability.capability import Capability


class SearchCapability(Capability):
    """Searches the web."""

    def __init__(
        self,
        api: SearchApi,
    ) -> None:
        self.api = api

    def execute(
        self,
        request: Request,
        conversation: Conversation,
        interpretation: Interpretation,
    ) -> Response:
        """Search the web."""

        _ = conversation, interpretation

        try:
            query = self._extract_query(
                request.text,
            )

            results = self.api.search(
                query,
            )

            if not results:
                return Response(
                    text="No results found.",
                )

            return Response(
                text=self._format_results(
                    query,
                    results,
                ),
            )

        except (
            ValueError,
            requests.RequestException,
        ) as error:
            return Response(
                text=str(error),
                success=False,
            )

    def _extract_query(
        self,
        text: str,
    ) -> str:
        """Extract the search query."""

        text = text.strip()

        if text.lower().startswith(
            "search ",
        ):
            query = text[len("search ") :].strip()

            if query:
                return query

        raise ValueError(
            "Please specify a search query.",
        )

    def _format_results(
        self,
        query: str,
        results,
    ) -> str:
        """Format search results for display."""

        lines = [
            f'Top {len(results)} results for "{query}":',
            "",
        ]

        for index, result in enumerate(
            results,
            start=1,
        ):
            content = result.content.strip()

            if len(content) > 200:
                content = content[:200] + "..."

            lines.extend(
                [
                    f"{index}. {result.title}",
                    result.url,
                    content,
                    "",
                ],
            )

        return "\n".join(
            lines,
        )
