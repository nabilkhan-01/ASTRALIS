from astralis.capability.file_system import FileSystemCapability
from astralis.tools.file_system import FileSystemTool
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

    @staticmethod
    def _create_capability() -> FileSystemCapability:
        """Create a file system capability."""

        return FileSystemCapability(
            FileSystemTool(),
        )

    def test_pwd(
        self,
    ) -> None:
        """Return the current working directory."""

        capability = self._create_capability()

        response = capability.execute(
            create_request(
                "pwd",
            ),
            create_conversation(),
            create_interpretation(),
        )

        assert response.success is True
        assert response.text

    def test_list_files(
        self,
    ) -> None:
        """List files."""

        capability = self._create_capability()

        response = capability.execute(
            create_request(
                "list files",
            ),
            create_conversation(),
            create_interpretation(),
        )

        assert response.success is True

    def test_list_folders(
        self,
    ) -> None:
        """List folders."""

        capability = self._create_capability()

        response = capability.execute(
            create_request(
                "list folders",
            ),
            create_conversation(),
            create_interpretation(),
        )

        assert response.success is True

    def test_read_existing_file(
        self,
    ) -> None:
        """Read an existing file."""

        capability = self._create_capability()

        response = capability.execute(
            create_request(
                "read README.md",
            ),
            create_conversation(),
            create_interpretation(),
        )

        assert response.success is True
        assert "ASTRALIS" in response.text

    def test_read_missing_file(
        self,
    ) -> None:
        """Handle a missing file."""

        capability = self._create_capability()

        response = capability.execute(
            create_request(
                "read missing.txt",
            ),
            create_conversation(),
            create_interpretation(),
        )

        assert response.success is False
        assert "does not exist" in response.text

    def test_missing_filename(
        self,
    ) -> None:
        """Handle a missing filename."""

        capability = self._create_capability()

        response = capability.execute(
            create_request(
                "read",
            ),
            create_conversation(),
            create_interpretation(),
        )

        assert response.success is False
        assert response.text == "Usage: read <file>"

    def test_unknown_command(
        self,
    ) -> None:
        """Handle an unknown command."""

        capability = self._create_capability()

        response = capability.execute(
            create_request(
                "hello",
            ),
            create_conversation(),
            create_interpretation(),
        )

        assert response.success is False
        assert response.text == "Unknown file system command."
