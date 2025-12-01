from tkinter import Tk
from ui.main_window import MainWindow


def main():
    root = Tk()
    root.title("System Backup Tool")
    root.geometry("900x600")  # width x height

    # Create and attach our main UI frame
    app = MainWindow(root)
    app.pack(fill="both", expand=True)

    root.mainloop()


if __name__ == "__main__":
    main()
