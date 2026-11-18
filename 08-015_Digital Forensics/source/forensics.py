"""Extract and display file metadata for the digital forensics task."""

import argparse
import os
from datetime import datetime


def extract_metadata(file_path, error_handler=print):
    """Return a metadata dictionary, or an empty dictionary on failure.

    Accept a path string or pathlib.Path. Timestamps use local time.
    Send errors to error_handler (print by default) for CLI or GUI use.
    The creation-time label uses st_ctime; on Unix it actually
    records the last metadata change. An extension only suggests file type.
    """
    try:
        # os.fspath allows both strings and Path objects.
        file_path = os.fspath(file_path)
        file_stat = os.stat(file_path)
        if not os.path.isfile(file_path):
            error_handler(f"Error: expected a regular file: {file_path}")
            return {}
    except FileNotFoundError:
        error_handler(f"Error: file not found: {file_path}")
        return {}
    except PermissionError:
        error_handler(f"Error: permission denied: {file_path}")
        return {}
    except (OSError, ValueError, TypeError) as error:
        error_handler(f"Error: cannot inspect the file: {error}")
        return {}

    # Divide by 1024 at each step to produce binary size units.
    readable_size = float(file_stat.st_size)
    for unit in ("bytes", "KiB", "MiB", "GiB", "TiB"):
        if readable_size < 1024 or unit == "TiB":
            break
        readable_size /= 1024

    date_format = "%Y-%m-%d %H:%M:%S"
    metadata = {
        "File Name": os.path.basename(file_path),
        "Absolute Path": os.path.abspath(file_path),
        "File Extension / Inferred Type": (
            os.path.splitext(file_path)[1] or "No extension"
        ),
        "File Size (bytes)": file_stat.st_size,
        "File Size (readable)": f"{readable_size:.2f} {unit}",
        "Creation Time (st_ctime)": datetime.fromtimestamp(
            file_stat.st_ctime
        ).strftime(date_format),
        "Last Modification Time": datetime.fromtimestamp(
            file_stat.st_mtime
        ).strftime(date_format),
        "Last Access Time": datetime.fromtimestamp(
            file_stat.st_atime
        ).strftime(date_format),
        "File Permissions (octal)": oct(file_stat.st_mode)[-3:],
    }
    return metadata


def display_metadata(metadata):
    """Print each dictionary entry with aligned labels."""
    if not metadata:
        return

    print("\nFILE METADATA")
    print("=" * 72)
    label_width = max(len(label) for label in metadata)
    for label, value in metadata.items():
        print(f"{label:<{label_width}} : {value}")
    print("=" * 72)
    print("Times are local. On Unix, st_ctime means metadata change time.")
    print("File type is inferred from the extension, not verified content.")


def main():
    """Run the interactive CLI, inspect several paths, or open the GUI."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*", help="file paths to inspect")
    parser.add_argument(
        "--gui", action="store_true", help="open the Tkinter GUI"
    )
    args = parser.parse_args()
    if args.gui:
        from forensics_gui import launch_gui
        return launch_gui(args.files)

    selected_paths = args.files
    if not selected_paths:
        # Resolve the default sample independently of the working directory.
        test_file = os.path.join(os.path.dirname(__file__), "test_file.txt")
        try:
            entered_path = input(
                "Enter a file path (Enter uses test_file.txt): "
            )
            selected_paths = [entered_path.strip() or test_file]
        except (EOFError, KeyboardInterrupt):
            print("\nMetadata extraction cancelled.")
            return 0

    failed = False
    for path in selected_paths:
        metadata = extract_metadata(path)
        display_metadata(metadata)
        failed = failed or not metadata
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
