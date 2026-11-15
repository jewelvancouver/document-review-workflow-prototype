from pathlib import Path

SUPPORTED_EXTENSIONS = {".txt", ".md"}
MAX_FILE_BYTES = 100_000  # 100 KB for this beginner prototype.


def read_document(path: Path) -> str:
    """Read one supported UTF-8 text document with a simple size limit."""
    path = Path(path)

    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {path.suffix or '[no extension]'}")
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"Document not found: {path}")
    if path.stat().st_size > MAX_FILE_BYTES:
        raise ValueError(f"File exceeds the {MAX_FILE_BYTES // 1000} KB size limit")

    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Document is not valid UTF-8 text") from exc


def collect_input_files(inputs: list[str]) -> list[Path]:
    """Expand folders into their immediate files; keep explicit file paths."""
    collected: list[Path] = []
    for raw in inputs:
        path = Path(raw)
        if path.is_dir():
            collected.extend(sorted(item for item in path.iterdir() if item.is_file()))
        else:
            collected.append(path)
    return collected
