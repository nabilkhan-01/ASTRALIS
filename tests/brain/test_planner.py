from astralis.brain.intent import Intent
from astralis.brain.interpretation import Interpretation
from astralis.brain.planner import Planner
from astralis.capability.capability_type import CapabilityType


class TestPlanner:
    """Tests for the Planner."""

    def test_language_capability(
        self,
    ) -> None:
        """Select the language capability."""

        planner = Planner()

        interpretation = Interpretation(
            intent=Intent.CONVERSATION,
            entities=[],
        )

        plan = planner.plan(
            interpretation,
        )

        assert plan.capability is CapabilityType.LANGUAGE

    def test_time_capability(
        self,
    ) -> None:
        """Select the time capability."""

        planner = Planner()

        interpretation = Interpretation(
            intent=Intent.QUESTION,
            entities=["time"],
        )

        plan = planner.plan(
            interpretation,
        )

        assert plan.capability is CapabilityType.TIME

    def test_memory_falls_back_to_language(
        self,
    ) -> None:
        """Memory requests currently use the language capability."""

        planner = Planner()

        interpretation = Interpretation(
            intent=Intent.MEMORY,
            entities=["memory"],
        )

        plan = planner.plan(
            interpretation,
        )

        assert plan.capability is CapabilityType.LANGUAGE

    def test_weather_capability(
        self,
    ) -> None:
        """Select the weather capability."""

        planner = Planner()

        interpretation = Interpretation(
            intent=Intent.QUESTION,
            entities=["weather"],
        )

        plan = planner.plan(
            interpretation,
        )

        assert plan.capability is CapabilityType.WEATHER

    def test_calculator_capability(
        self,
    ) -> None:
        """Select the calculator capability."""

        planner = Planner()

        interpretation = Interpretation(
            intent=Intent.CONVERSATION,
            entities=["calculator"],
        )

        plan = planner.plan(
            interpretation,
        )

        assert plan.capability is CapabilityType.CALCULATOR
