System Backup Tool

A desktop backup app built in Python with Tkinter. You pick a source folder and a destination folder, hit one button, and the app copies everything across into a fresh timestamped version folder while showing you a live log and a progress bar.

Built as an Operating Systems course project. The goal was to get hands on with file system traversal, metadata preserving copies and versioned storage instead of just reading about them.

What it does
Pick folders through a file dialog. No typing paths by hand.
Full backup with structure preserved. Nested folders inside the source come out the same way inside the backup.
Versioned snapshots. Every run creates a new folder named Backup_YYYY-MM-DD_HH-MM-SS, so old backups are never overwritten. You keep a history you can roll back to by hand.
Metadata preserving copies. Uses shutil.copy2 so timestamps and file mode survive the copy.
Live progress. A determinate progress bar plus a scrolling log of every file that moved, so you can see exactly what happened and where it went.
Basic guard rails. The app warns you if either folder is missing before it starts, and it handles an empty source folder without crashing.
Running it

Needs Python 3.8 or newer. Tkinter ships with most Python installs, no pip packages required.

bash
git clone https://github.com/<your-username>/System_Backup_tool.git
cd System_Backup_tool
python app.py

Then choose a source folder, choose a destination, and click Start Backup.

How it is put together

I split the app into three layers so the backup logic can be tested or reused without the GUI attached to it.

app.py                    entry point, boots the Tk window
ui/
  main_window.py          all widgets, folder pickers, log panel, progress bar
logic/
  backup.py               the backup routine
  versioning.py           timestamped version folder naming
  restore.py              planned
  compare.py              planned
utilis/
  file_utilis.py          directory walk, safe copy, parent folder creation
  logger.py               planned

The UI never touches the file system directly and the logic layer never imports Tkinter. run_backup() takes three callbacks for logging, status text and progress percentage, so the same function could be driven from a CLI or a test harness with no changes. That was the design decision I cared most about on this project.

Roughly what happens on a run:

create_backup_folder() stamps a new version directory inside the destination.
get_all_files() walks the source tree with os.walk and collects every file path.
Each file gets its path rebuilt relative to the source root, parent folders are created on demand, then copy2 moves it over.
After every file the progress callback fires and the UI redraws.
What I would do next

Being straight about the current state: full backup works end to end. These are the pieces I scoped out and have not finished yet.

Incremental backup. Compare modified time and size against the previous version folder and only copy what changed. The compare.py module is stubbed for this.
Restore. Pick a version folder and push it back to the original location.
Threading. The copy currently runs on the main thread, so the window locks up on very large folders. Moving run_backup onto a worker thread and pushing UI updates through a queue is the fix.
File logging. Write the session log to disk instead of only into the text panel.
Compression. Optional zip output for old versions to save space.
What I picked up from it
How os.walk actually behaves on nested trees and why relative paths matter when you rebuild a structure somewhere else.
The difference between copy and copy2 and why metadata matters for a backup tool.
Why timestamped versioning is safer than overwriting, and what that costs you in disk space.
Keeping the GUI and the file logic apart through callbacks so neither one depends on the other.

Python, Tkinter, os, shutil, pathlib style file handling. No external dependencies.
