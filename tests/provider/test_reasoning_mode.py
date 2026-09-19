import pytest

from astralis.providers.reasoning import ReasoningMode


class TestReasoningMode:
    """Tests for the provider-independent ReasoningMode abstraction."""

    def test_members_exist(
        self,
    ) -> None:
        """Verify FAST, DEEP, and AUTO reasoning modes exist."""

        assert hasattr(ReasoningMode, "FAST")
        assert hasattr(ReasoningMode, "DEEP")
        assert hasattr(ReasoningMode, "AUTO")

    def test_values_serialize_predictably(
        self,
    ) -> None:
        """Values serialize to expected lower-case string representations."""

        assert ReasoningMode.FAST.value == "fast"
        assert ReasoningMode.DEEP.value == "deep"
        assert ReasoningMode.AUTO.value == "auto"

    @pytest.mark.parametrize(
        ("input_str", "expected_mode"),
        [
            ("fast", ReasoningMode.FAST),
            ("FAST", ReasoningMode.FAST),
            ("Fast", ReasoningMode.FAST),
            ("  fast  ", ReasoningMode.FAST),
            ("deep", ReasoningMode.DEEP),
            ("DEEP", ReasoningMode.DEEP),
            ("Deep", ReasoningMode.DEEP),
            ("  deep  ", ReasoningMode.DEEP),
            ("auto", ReasoningMode.AUTO),
            ("AUTO", ReasoningMode.AUTO),
            ("Auto", ReasoningMode.AUTO),
            ("  auto  ", ReasoningMode.AUTO),
        ],
    )
    def test_from_string_case_insensitive(
        self,
        input_str: str,
        expected_mode: ReasoningMode,
    ) -> None:
        """ReasoningMode.from_string parses values case-insensitively with whitespace stripping."""

        assert ReasoningMode.from_string(input_str) is expected_mode

    def test_from_string_identity_for_existing_instance(
        self,
    ) -> None:
        """ReasoningMode.from_string returns the instance if already a ReasoningMode."""

        assert ReasoningMode.from_string(ReasoningMode.FAST) is ReasoningMode.FAST
        assert ReasoningMode.from_string(ReasoningMode.DEEP) is ReasoningMode.DEEP
        assert ReasoningMode.from_string(ReasoningMode.AUTO) is ReasoningMode.AUTO

    @pytest.mark.parametrize(
        "invalid_input",
        [
            "turbo",
            "medium",
            "slow",
            "true",
            "false",
            "1",
            "",
            "   ",
        ],
    )
    def test_from_string_invalid_string_raises_value_error(
        self,
        invalid_input: str,
    ) -> None:
        """Invalid reasoning mode strings raise ValueError with descriptive guidance."""

        with pytest.raises(
            ValueError,
            match="Invalid reasoning mode",
        ):
            ReasoningMode.from_string(invalid_input)

    @pytest.mark.parametrize(
        "invalid_type_input",
        [
            123,
            None,
            12.34,
            [],
            {},
        ],
    )
    def test_from_string_invalid_type_raises_type_error(
        self,
        invalid_type_input: object,
    ) -> None:
        """Non-string/non-ReasoningMode inputs raise TypeError."""

        with pytest.raises(
            TypeError,
            match="Invalid reasoning mode type",
        ):
            ReasoningMode.from_string(invalid_type_input)  # type: ignore[arg-type]

