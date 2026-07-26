from astralis.capability.file_system import FileSystemCapability
from tests.helpers.conversation_factory import (
    create_conversation,
)
from tests.helpers.interpretation_factory import (
    create_interpretation,
)
from tests.helpers.request_factory import (
    create_request,
)


class TestFileSystemCapability:
    """Tests for the FileSystemCapability."""

    def setup_method(
        self,
    ) -> None:
        self.capability = FileSystemCapability()

    def test_pwd(
        self,
    ) -> None:
        """Return the current working directory."""

        response = self.capability.execute(
            create_request("pwd"),
            create_conversation(),
            create_interpretation(),
        )

        assert response.success
        assert response.text

    def test_list_files(
        self,
    ) -> None:
        """List files."""

        response = self.capability.execute(
            create_request("list files"),
            create_conversation(),
            create_interpretation(),
        )

        assert response.success

    def test_list_folders(
        self,
    ) -> None:
        """List folders."""

        response = self.capability.execute(
            create_request("list folders"),
            create_conversation(),
            create_interpretation(),
        )

        assert response.success

    def test_read_existing_file(
        self,
    ) -> None:
        """Read an existing file."""

        response = self.capability.execute(
            create_request("read README.md"),
            create_conversation(),
            create_interpretation(),
        )

        assert response.success
        assert "ASTRALIS" in response.text

    def test_read_missing_file(
        self,
    ) -> None:
        """Handle a missing file."""

        response = self.capability.execute(
            create_request("read missing.txt"),
            create_conversation(),
            create_interpretation(),
        )

        assert not response.success
        assert "does not exist" in response.text

    def test_missing_filename(
        self,
    ) -> None:
        """Handle a missing filename."""

        response = self.capability.execute(
            create_request("read"),
            create_conversation(),
            create_interpretation(),
        )

        assert not response.success
        assert response.text == "Please specify a file."

    def test_unknown_command(
        self,
    ) -> None:
        """Handle an unknown command."""

        response = self.capability.execute(
            create_request("hello"),
            create_conversation(),
            create_interpretation(),
        )

        assert not response.success
        assert response.text == "Unknown file system command."
