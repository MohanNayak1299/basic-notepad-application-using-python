import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import os

class Notepad:
    def __init__(self, **kwargs):
        self.root_window = tk.Tk()  # main window
        self.root_window.title("Untitled - Notepad")
        
        # Set the window size (default 700x500)
        self.window_width = kwargs.get('width', 700)
        self.window_height = kwargs.get('height', 500)
        self.root_window.geometry(f'{self.window_width}x{self.window_height}')
        
        screen_width = self.root_window.winfo_screenwidth()
        screen_height = self.root_window.winfo_screenheight()
        position_top = (screen_height // 2) - (self.window_height // 2)
        position_left = (screen_width // 2) - (self.window_width // 2)
        self.root_window.geometry(f'{self.window_width}x{self.window_height}+{position_left}+{position_top}')
        
        self.text_area = scrolledtext.ScrolledText(self.root_window, wrap=tk.WORD, font=("Arial", 12))
        self.text_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        self.current_file = None  # To track the current file being edited
        
        self.create_menus()
        
    def create_menus(self):
        style = ttk.Style()
        style.configure("TMenu", background="white", foreground="black", font=("Arial", 10))  # Reduced font size
        style.configure("TMenuItem", background="white", foreground="black", font=("Arial", 10))  # Reduced font size

        self.menu_bar = tk.Menu(self.root_window, bg="white", fg="black", font=("Arial", 10))  # Reduced font size
        
        # File Menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0, bg="white", fg="black", font=("Arial", 10))  # Reduced font size
        self.file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        self.file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        self.file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        self.file_menu.add_command(label="Save As", command=self.save_as_file, accelerator="Ctrl+Shift+S")  # New Save As option
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.quit_application)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        
        # Edit Menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0, bg="white", fg="black", font=("Arial", 10))  # Reduced font size
        self.edit_menu.add_command(label="Cut", command=self.cut, accelerator="Ctrl+X")
        self.edit_menu.add_command(label="Copy", command=self.copy, accelerator="Ctrl+C")
        self.edit_menu.add_command(label="Paste", command=self.paste, accelerator="Ctrl+V")
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        
        # Help Menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0, bg="white", fg="black", font=("Arial", 10))  # Reduced font size
        self.help_menu.add_command(label="About", command=self.show_about)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        
        # Set the menu
        self.root_window.config(menu=self.menu_bar)

        # Keyboard shortcuts
        self.root_window.bind("<Control-n>", lambda event: self.new_file())
        self.root_window.bind("<Control-o>", lambda event: self.open_file())
        self.root_window.bind("<Control-s>", lambda event: self.save_file())
        self.root_window.bind("<Control-Shift-S>", lambda event: self.save_as_file())  # Bind Save As to Ctrl+Shift+S
        self.root_window.bind("<Control-x>", lambda event: self.cut())
        self.root_window.bind("<Control-c>", lambda event: self.copy())
        self.root_window.bind("<Control-v>", lambda event: self.paste())

    def quit_application(self):
        self.root_window.quit()

    def show_about(self):
        messagebox.showinfo("Notepad", "Developed by Mrinal Verma", icon='info')

    def open_file(self):
        self.current_file = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")],
            title="Open File"
        )
        if self.current_file:
            with open(self.current_file, 'r') as file:
                content = file.read()
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, content)
            self.root_window.title(f"{os.path.basename(self.current_file)} - Notepad")

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.root_window.title("Untitled - Notepad")
        self.current_file = None

    def save_file(self):
        if self.current_file is None:
            self.current_file = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")],
                title="Save File"
            )
        if self.current_file:
            with open(self.current_file, 'w') as file:
                file.write(self.text_area.get(1.0, tk.END))
            self.root_window.title(f"{os.path.basename(self.current_file)} - Notepad")

    def save_as_file(self):
        """Handles the 'Save As' functionality"""
        self.current_file = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")],
            title="Save As"
        )
        if self.current_file:
            with open(self.current_file, 'w') as file:
                file.write(self.text_area.get(1.0, tk.END))
            self.root_window.title(f"{os.path.basename(self.current_file)} - Notepad")

    def cut(self):
        self.text_area.event_generate("<<Cut>>")

    def copy(self):
        self.text_area.event_generate("<<Copy>>")

    def paste(self):
        self.text_area.event_generate("<<Paste>>")

    def run(self):
        self.root_window.mainloop()

# Running the Notepad application
notepad = Notepad(width=700, height=500)
notepad.run()