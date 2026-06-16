"""
Finger Slicer cleanup utility.

Removes generated and cached artifacts to get a clean slate:
  - assets/    segmented sprites
  - previews/  segmentation preview images
  - weights/   downloaded model weights (re-downloaded on next run)
  - every __pycache__/ directory in the project

Cross-platform replacement for cleaner.sh — works anywhere Python runs:
    python cleaner.py
"""
from   pathlib import Path
import sys
# Adjust the import path to include the project root
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

from   config import DEFAULT_OUTPUT_DIR, PREVIEW_DIR, WEIGHTS_DIR
import shutil

# Directories whose contents are wiped (the folder itself is kept).
CONTENT_DIRS = [DEFAULT_OUTPUT_DIR, PREVIEW_DIR, WEIGHTS_DIR]

def clear_dir(directory: Path) -> int:
    """
    Deletes everything inside `directory` (files and sub-folders) while keeping the directory itself.
    Hidden entries (names starting with ".", e.g. .gitkeep) are skipped.

    Args:
        directory: the folder to empty.

    Returns:
        The number of entries removed.
    """
    if not directory.is_dir():
        return 0

    entries = [entry for entry in directory.iterdir() if not entry.name.startswith(".")]
    for entry in entries:
        if entry.is_dir():
            shutil.rmtree(entry)
        else:
            entry.unlink()
    return len(entries)


def remove_pycaches() -> int:
    """
    Removes every `__pycache__` directory in the project,
    skipping hidden directories (e.g. a `.venv`).

    Returns:
        The number of `__pycache__` directories removed.
    """

    # Check parts relative to ROOT so a hidden ancestor above the project is ignored.
    caches = [p for p in ROOT_DIR.rglob("__pycache__")
              if not any(part.startswith(".") for part in p.relative_to(ROOT_DIR).parts)]

    for cache in caches:
        shutil.rmtree(cache, ignore_errors=True)
    return len(caches)


def main():
    for directory in CONTENT_DIRS:
        n = clear_dir(directory)
        print(f"Cleared {n} item(s) from {directory}" if n else f"Nothing to clear in {directory}")

    print(f"Removed {remove_pycaches()} __pycache__ folder(s)")

if __name__ == "__main__":
    main()