"""Tkinter interface for inspecting metadata from multiple selected files."""

import os

from forensics import extract_metadata


class ForensicsApp:
    """Keep each file's metadata or error available for selection."""

    def __init__(self, root, paths=()):
        from tkinter import filedialog, ttk
        from tkinter.scrolledtext import ScrolledText

        self.filedialog = filedialog
        self.root = root
        self.results = {}
        root.title("Digital Forensics — File Metadata")
        root.geometry("1000x650")
        root.minsize(650, 450)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        root.rowconfigure(2, weight=2)

        toolbar = ttk.Frame(root, padding=8)
        toolbar.grid(row=0, column=0, sticky="ew")
        ttk.Button(toolbar, text="Add files…", command=self.choose_files).pack(
            side="left"
        )
        ttk.Button(toolbar, text="Clear", command=self.clear).pack(side="left")
        ttk.Label(toolbar, text="Select a row to view its metadata.").pack(
            side="left", padx=12
        )

        listing = ttk.Frame(root, padding=(8, 0))
        listing.grid(row=1, column=0, sticky="nsew")
        listing.columnconfigure(0, weight=1)
        listing.rowconfigure(0, weight=1)
        self.table = ttk.Treeview(
            listing, columns=("path", "status"), show="headings",
            selectmode="browse"
        )
        self.table.heading("path", text="File path")
        self.table.heading("status", text="Result")
        self.table.column("path", width=740, minwidth=200)
        self.table.column("status", width=100, stretch=False)
        self.table.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(
            listing, orient="vertical", command=self.table.yview
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.table.configure(yscrollcommand=scrollbar.set)
        self.table.bind("<<TreeviewSelect>>", self.show_selected)

        self.details = ScrolledText(root, wrap="word", state="disabled")
        self.details.grid(row=2, column=0, sticky="nsew", padx=8, pady=8)
        ttk.Label(
            root, padding=8, wraplength=620,
            text="Times are local. On Unix, st_ctime is metadata change time. "
                 "File types are inferred from extensions, not file contents."
        ).grid(row=3, column=0, sticky="ew")
        self.add_files(paths)

    def choose_files(self):
        """A cancelled file dialog leaves the current results unchanged."""
        paths = self.filedialog.askopenfilenames(
            parent=self.root, title="Select files to inspect",
            filetypes=[("All files", "*")]
        )
        self.add_files(paths)

    def add_files(self, paths):
        """Inspect each selected file independently, retaining failures too."""
        first = None
        for path in paths:
            errors = []
            metadata = extract_metadata(path, error_handler=errors.append)
            item = self.table.insert(
                "", "end", values=(os.path.abspath(path),
                                   "OK" if metadata else "Error")
            )
            self.results[item] = (metadata, "\n".join(errors))
            if first is None:
                first = item
        if first is not None:
            self.table.selection_set(first)
            self.table.see(first)
            self.show_selected()

    def show_selected(self, event=None):
        """Display all metadata fields or the selected file's error."""
        selection = self.table.selection()
        if not selection:
            return
        metadata, error = self.results[selection[0]]
        text = "\n".join(f"{key}: {value}" for key, value in metadata.items())
        self.set_details(text or error)

    def set_details(self, text):
        """Keep results selectable and copyable, but prevent editing."""
        self.details.configure(state="normal")
        self.details.delete("1.0", "end")
        self.details.insert("1.0", text)
        self.details.configure(state="disabled")

    def clear(self):
        """Remove all results so another group of files can be inspected."""
        for item in self.table.get_children():
            self.table.delete(item)
        self.results.clear()
        self.set_details("")


def launch_gui(paths=()):
    """Start Tkinter, reporting unavailable Tk or display access cleanly."""
    try:
        import tkinter as tk
    except ImportError:
        print("Error: Tkinter missing. Install Python with Tcl/Tk support.")
        return 1
    try:
        root = tk.Tk()
    except tk.TclError as error:
        print(f"Error: cannot open the Tkinter window: {error}")
        return 1
    ForensicsApp(root, paths)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(launch_gui())
