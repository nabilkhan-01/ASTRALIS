from unittest.mock import Mock

from astralis.brain.request import Request
from astralis.brain.response import Response
from astralis.brain.source import RequestSource
from astralis.memory.retriever import MemoryRetriever
from astralis.monitoring.monitor import Monitor
from astralis.pipeline.request_pipeline import RequestPipeline


class TestRequestPipeline:
    """Tests for the RequestPipeline."""

    @staticmethod
    def _request() -> Request:
        """Create a test request."""

        return Request(
            text="Hello",
            source=RequestSource.CLI,
        )

    def test_process_with_monitoring_enabled(
        self,
    ) -> None:
        """Process a request with monitoring enabled."""

        brain = Mock()
        brain.process.return_value = Response(
            text="Hello!",
            success=True,
        )

        retriever = Mock(
            spec=MemoryRetriever,
        )

        retriever.retrieve.return_value =[]

        pipeline = RequestPipeline(
            brain=brain,
            retriever=retriever,
            monitor=Monitor(
                enabled=True,
            ),
        )

        request = self._request()

        response = pipeline.process(
            request,
        )

        assert response.success is True
        assert response.text == "Hello!"
        brain.process.assert_called_once()

        retriever.retrieve.assert_called_once_with(
            request,
        )

    def test_process_with_monitoring_disabled(
        self,
    ) -> None:
        """Process a request with monitoring disabled."""

        brain = Mock()
        brain.process.return_value = Response(
            text="Hello!",
            success=True,
        )

        retriever = Mock(
            spec=MemoryRetriever,
        )

        retriever.retrieve.return_value =[]

        pipeline = RequestPipeline(
            brain=brain,
            retriever=retriever,
            monitor=Monitor(
                enabled=False,
            ),
        )

        request = self._request()

        response = pipeline.process(
            request,
        )

        assert response.success is True
        assert response.text == "Hello!"
        retriever.retrieve.assert_called_once_with(
            request,
        )
        brain.process.assert_called_once()