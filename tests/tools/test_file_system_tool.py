from pathlib import Path

from astralis.tools.file_system import FileSystemTool


class TestFileSystemTool:
    """Tests for the FileSystemTool."""

    def setup_method(
        self,
    ) -> None:
        self.tool = FileSystemTool()

    def test_current_directory(
        self,
    ) -> None:
        """Return the current working directory."""

        current = self.tool.current_directory()

        assert Path(
            current,
        ).exists()

    def test_exists(
        self,
        tmp_path: Path,
    ) -> None:
        """Check whether a file exists."""

        file = tmp_path / "test.txt"

        file.write_text(
            "Hello",
            encoding="utf-8",
        )

        assert self.tool.exists(
            str(file),
        )

    def test_list_files(
        self,
        tmp_path: Path,
    ) -> None:
        """List files in a directory."""

        (tmp_path / "a.txt").write_text(
            "A",
        )

        (tmp_path / "b.txt").write_text(
            "B",
        )

        files = self.tool.list_files(
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

        (tmp_path / "docs").mkdir()

        (tmp_path / "tests").mkdir()

        folders = self.tool.list_folders(
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

        file = tmp_path / "notes.txt"

        file.write_text(
            "Hello ASTRALIS",
            encoding="utf-8",
        )

        content = self.tool.read_file(
            str(file),
        )

        assert content == "Hello ASTRALIS"

    def test_missing_file(
        self,
        tmp_path: Path,
    ) -> None:
        """Missing files should not exist."""

        file = tmp_path / "missing.txt"

        assert not self.tool.exists(
            str(file),
        )