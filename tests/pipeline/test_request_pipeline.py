from unittest.mock import Mock

from astralis.brain.request import Request
from astralis.brain.response import Response
from astralis.brain.source import RequestSource
from astralis.monitoring.monitor import Monitor
from astralis.pipeline.request_pipeline import RequestPipeline


class TestRequestPipeline:
    """Tests for the RequestPipeline."""

    @staticmethod
    def _request() -> Request:
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

        pipeline = RequestPipeline(
            brain=brain,
            monitor=Monitor(
                enabled=True,
            ),
        )

        response = pipeline.process(
            self._request(),
        )

        assert response.success is True
        assert response.text == "Hello!"
        brain.process.assert_called_once()

    def test_process_with_monitoring_disabled(
        self,
    ) -> None:
        """Process a request with monitoring disabled."""

        brain = Mock()
        brain.process.return_value = Response(
            text="Hello!",
            success=True,
        )

        pipeline = RequestPipeline(
            brain=brain,
            monitor=Monitor(
                enabled=False,
            ),
        )

        response = pipeline.process(
            self._request(),
        )

        assert response.success is True
        assert response.text == "Hello!"
        brain.process.assert_called_once()