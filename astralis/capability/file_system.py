from astralis.brain.conversation import Conversation
from astralis.brain.interpretation import Interpretation
from astralis.brain.request import Request
from astralis.brain.response import Response
from astralis.capability.capability import Capability
from astralis.tools.file_system import FileSystemTool


class FileSystemCapability(Capability):
    """Provides read-only access to the file system."""

    PWD_COMMAND = "pwd"
    LIST_FILES_COMMAND = "list files"
    LIST_FOLDERS_COMMAND = "list folders"
    READ_COMMAND = "read"

    def __init__(
        self,
        file_system: FileSystemTool,
    ) -> None:
        self.file_system = file_system

    def execute(
        self,
        request: Request,
        conversation: Conversation,
        interpretation: Interpretation,
    ) -> Response:
        """Execute a file system request."""

        _ = conversation, interpretation

        text = request.text.strip()
        lower = text.lower()

        try:
            if lower == self.PWD_COMMAND:
                return self._handle_pwd()

            if lower == self.LIST_FILES_COMMAND:
                return self._handle_list_files()

            if lower == self.LIST_FOLDERS_COMMAND:
                return self._handle_list_folders()

            if lower.startswith(
                self.READ_COMMAND,
            ):
                return self._handle_read_file(
                    text,
                )

            return Response(
                text="Unknown file system command.",
                success=False,
            )

        except (
            OSError,
            UnicodeDecodeError,
        ) as error:
            return Response(
                text=str(error),
                success=False,
            )

    def _handle_pwd(
        self,
    ) -> Response:
        """Return the current working directory."""

        return Response(
            text=self.file_system.current_directory(),
        )

    def _handle_list_files(
        self,
    ) -> Response:
        """Return all files."""

        files = self.file_system.list_files()

        return self._create_list_response(
            files,
            "No files found.",
        )

    def _handle_list_folders(
        self,
    ) -> Response:
        """Return all folders."""

        folders = self.file_system.list_folders()

        return self._create_list_response(
            folders,
            "No folders found.",
        )

    def _handle_read_file(
        self,
        text: str,
    ) -> Response:
        """Read a text file."""

        path = text[len(self.READ_COMMAND) :].strip()

        if not path:
            return Response(
                text="Usage: read <file>",
                success=False,
            )

        if not self.file_system.exists(
            path,
        ):
            return Response(
                text=f"'{path}' does not exist.",
                success=False,
            )

        return Response(
            text=self.file_system.read_file(
                path,
            ),
        )

    def _create_list_response(
        self,
        items: list[str],
        empty_message: str,
    ) -> Response:
        """Create a response for a list of items."""

        if not items:
            return Response(
                text=empty_message,
            )

        return Response(
            text="\n".join(
                items,
            ),
        )
