from pathlib import Path

from astralis.tools.file_system import FileSystemTool


class TestFileSystemTool:
    """Tests for the FileSystemTool."""

    @staticmethod
    def _create_tool() -> FileSystemTool:
        """Create a file system tool."""

        return FileSystemTool()

    def test_current_directory(
        self,
    ) -> None:
        """Return the current working directory."""

        tool = self._create_tool()

        current = tool.current_directory()

        assert Path(
            current,
        ).exists()

    def test_exists(
        self,
        tmp_path: Path,
    ) -> None:
        """Check whether a file exists."""

        tool = self._create_tool()

        file = tmp_path / "test.txt"

        file.write_text(
            "Hello",
            encoding="utf-8",
        )

        assert (
            tool.exists(
                str(file),
            )
            is True
        )

    def test_list_files(
        self,
        tmp_path: Path,
    ) -> None:
        """List files in a directory."""

        tool = self._create_tool()

        (tmp_path / "a.txt").write_text(
            "A",
        )

        (tmp_path / "b.txt").write_text(
            "B",
        )

        files = tool.list_files(
            str(tmp_path),
        )

        assert files == [
            "a.txt",
            "b.txt",
        ]

    def test_list_folders(
        self,
        tmp_path: Path,
    ) -> None:
        """List folders in a directory."""

        tool = self._create_tool()

        (tmp_path / "docs").mkdir()

        (tmp_path / "tests").mkdir()

        folders = tool.list_folders(
            str(tmp_path),
        )

        assert folders == [
            "docs",
            "tests",
        ]

    def test_read_file(
        self,
        tmp_path: Path,
    ) -> None:
        """Read a text file."""

        tool = self._create_tool()

        file = tmp_path / "notes.txt"

        file.write_text(
            "Hello ASTRALIS",
            encoding="utf-8",
        )

        content = tool.read_file(
            str(file),
        )

        assert content == "Hello ASTRALIS"

    def test_missing_file(
        self,
        tmp_path: Path,
    ) -> None:
        """Missing files should not exist."""

        tool = self._create_tool()

        file = tmp_path / "missing.txt"

        assert (
            tool.exists(
                str(file),
            )
            is False
        )
