from pathlib import Path


class FileSystemTool:
    """Provides read-only access to the file system."""

    def current_directory(
        self,
    ) -> str:
        """Return the current working directory."""

        return str(
            Path.cwd(),
        )

    def list_files(
        self,
        path: str = ".",
    ) -> list[str]:
        """Return all files in a directory."""

        directory = Path(
            path,
        )

        if not directory.is_dir():
            return []

        return sorted(file.name for file in directory.iterdir() if file.is_file())

    def list_folders(
        self,
        path: str = ".",
    ) -> list[str]:
        """Return all folders in a directory."""

        directory = Path(
            path,
        )

        if not directory.is_dir():
            return []

        return sorted(folder.name for folder in directory.iterdir() if folder.is_dir())

    def exists(
        self,
        path: str,
    ) -> bool:
        """Return whether a file or folder exists."""

        return Path(
            path,
        ).exists()

    def read_file(
        self,
        path: str,
    ) -> str:
        """Read a UTF-8 text file."""

        file = Path(
            path,
        )

        if not file.is_file():
            raise FileNotFoundError(
                f"'{path}' is not a file.",
            )

        return file.read_text(
            encoding="utf-8",
        )
