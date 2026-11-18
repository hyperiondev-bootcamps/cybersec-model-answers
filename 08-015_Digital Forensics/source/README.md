# Digital forensics

## Setup for both tasks

Run all commands below from the `source` directory containing this README.
Create and activate the virtual environment, then install dependencies.

On macOS / Linux:

```sh
python3 -m venv venv
source venv/bin/activate
```

On Windows (Command Prompt), use:

```sh
python -m venv venv
.\venv\Scripts\activate
```

## Run the practical task: command-line metadata extraction

After setup, run this command on macOS / Linux or Windows PowerShell:

```sh
python forensics.py
```

Press Enter to inspect the supplied `test_file.txt`, or enter a file path at the
prompt. Metadata is printed in the terminal. Relative paths are resolved from
the terminal's working directory; the default sample is resolved relative to
the script. `forensics.py` and `test_file.txt` both live in this directory.

You can also supply a single file directly:

```sh
python forensics.py "test_file.txt"
```

## Optional task: graphical interface and multiple files

After setup, start the Tkinter interface with this command on macOS / Linux
or Windows PowerShell:

```sh
python forensics.py --gui
```

Click **Add files…** and select several files using your operating system's
multi-selection controls. Select a row to see its metadata in the read-only,
copyable details panel. Each failed file has an **Error** row with an explanation;
other files are still inspected. **Clear** removes all results. Cancelling the
file picker leaves existing results in place. Close the window to exit.

To preload files in the GUI:

```sh
python forensics.py --gui "test_file.txt" "another file.txt"
```

To inspect multiple files in the terminal:

```sh
python forensics.py "test_file.txt" "another file.txt"
```

Replace the example paths with existing files. Quote paths containing spaces.
The CLI processes every path, even after an error, and returns exit status 1
if any file fails (otherwise 0). Both interfaces share `extract_metadata`.

See the [official Python Tkinter documentation](https://docs.python.org/3/library/tkinter.html)
for installation and distribution details. Tkinter is Python's standard
interface to Tcl/Tk, distributed as an optional CPython module. Official Python
binary releases bundle Tcl/Tk; other Python distributors may provide Tkinter
separately. If it is missing, follow your Python distributor's instructions to
install its Tk package or use a Python distribution with Tcl/Tk support.
Tkinter is not installed through pip or `requirements.txt`.

The GUI needs a desktop session. Run `python -m tkinter` to check that a
demonstration window opens and displays the installed Tcl/Tk version.
The command-line interface remains usable without Tkinter.

Run `deactivate` when finished.

## How metadata is interpreted

extract_metadata collects filesystem attributes into a dictionary.
display_metadata loops over its entries and aligns the labels. Errors produce
a clear message and an empty dictionary, so missing files do not cause a crash.
The script inspects metadata with os.stat without reading the file contents.

Times are displayed in the computer's local timezone. The st_ctime
field is labelled as creation time, but on Unix (including
macOS) it is the last metadata change time, not the birth time. Extensions
suggest file types but cannot establish the actual contents. Permissions show
the final three octal digits, excluding ACLs and special bits.
Readable sizes use KiB/MiB (1024-based units); raw bytes are also shown.
