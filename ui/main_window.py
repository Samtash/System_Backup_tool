import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from logic.versioning import create_backup_folder
from logic.backup import run_backup


class MainWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.source_path = tk.StringVar()
        self.dest_path = tk.StringVar()

        self._build_layout()

    def _build_layout(self):
        left = tk.Frame(self, padx=10, pady=10)
        left.pack(side="left", fill="y")

        tk.Label(left, text="Source folder:").pack(anchor="w")
        tk.Label(left, textvariable=self.source_path, fg="blue").pack(anchor="w")

        tk.Button(left, text="Choose Source Folder",
                  command=self.choose_source).pack(pady=(5, 15), fill="x")

        tk.Label(left, text="Destination folder:").pack(anchor="w")
        tk.Label(left, textvariable=self.dest_path, fg="blue").pack(anchor="w")

        tk.Button(left, text="Choose Destination Folder",
                  command=self.choose_dest).pack(pady=(5, 15), fill="x")

        tk.Button(left, text="Start Backup",
                  command=self.start_backup).pack(pady=(10, 5), fill="x")

        right = tk.Frame(self, padx=10, pady=10)
        right.pack(side="right", fill="both", expand=True)

        tk.Label(right, text="Backup Log").pack(anchor="w")

        self.log_text = tk.Text(right, height=25, state="disabled")
        self.log_text.pack(fill="both", expand=True, pady=(5, 10))

        self.progress = ttk.Progressbar(right, mode="determinate")
        self.progress.pack(fill="x")

        self.status_label = tk.Label(right, text="Ready.")
        self.status_label.pack(anchor="w", pady=(5, 0))

    # =======================
    # FOLDER SELECTION
    # =======================

    def choose_source(self):
        folder = filedialog.askdirectory(title="Select source folder")
        if folder:
            self.source_path.set(folder)
            self._log(f"Selected source: {folder}")

    def choose_dest(self):
        folder = filedialog.askdirectory(title="Select backup destination")
        if folder:
            self.dest_path.set(folder)
            self._log(f"Selected destination: {folder}")

    # =======================
    # START BACKUP
    # =======================

    def start_backup(self):
        if not self.source_path.get() or not self.dest_path.get():
            messagebox.showwarning(
                "Missing folders",
                "Please choose both source and destination folders."
            )
            return

        self._log("=== Backup started ===")
        self.status_label.config(text="Starting backup...")
        self.progress["value"] = 0
        self.update_idletasks()

        # callbacks for UI updates
        def log_cb(msg):
            self._log(msg)

        def status_cb(text):
            self.status_label.config(text=text)
            self.status_label.update_idletasks()

        def progress_cb(value):
            self.progress["value"] = value
            self.progress.update_idletasks()

        # run full backup
        run_backup(
            self.source_path.get(),
            self.dest_path.get(),
            log_cb,
            status_cb,
            progress_cb
        )

    # =======================
    # LOGGING
    # =======================

    def _log(self, text: str):
        self.log_text.config(state="normal")
        self.log_text.insert("end", text + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")
