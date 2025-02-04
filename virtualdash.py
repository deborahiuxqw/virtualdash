import tkinter as tk
from tkinter import simpledialog, colorchooser, messagebox
import os

class VirtualDash:
    def __init__(self, root):
        self.root = root
        self.root.title("VirtualDash")
        self.root.geometry("300x200")
        
        self.notes = []
        
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New Note", command=self.create_note)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Save Notes", command=self.save_notes)
        self.file_menu.add_command(label="Load Notes", command=self.load_notes)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        
    def create_note_window(self, content="", color="yellow"):
        note_window = tk.Toplevel(self.root)
        note_window.title("Sticky Note")
        note_window.geometry("200x150")
        
        text = tk.Text(note_window, wrap='word', bg=color)
        text.insert('1.0', content)
        text.pack(expand=True, fill='both')
        
        note_window.protocol("WM_DELETE_WINDOW", lambda: self.close_note(note_window, text))
        self.notes.append((note_window, text))
        
    def create_note(self):
        color = colorchooser.askcolor(title="Choose Note Color")[1] or "yellow"
        self.create_note_window(color=color)
    
    def close_note(self, note_window, text):
        note_content = text.get("1.0", tk.END).strip()
        if note_content:
            response = messagebox.askyesnocancel("Save Note", "Do you want to save this note?")
            if response:  # Save
                self.save_single_note(note_content, note_window.cget("bg"))
        self.notes.remove((note_window, text))
        note_window.destroy()
    
    def save_single_note(self, content, color):
        with open("notes.txt", "a") as file:
            file.write(f"{color}|{content}\n")
    
    def save_notes(self):
        with open("notes.txt", "w") as file:
            for note_window, text in self.notes:
                content = text.get("1.0", tk.END).strip()
                if content:
                    color = note_window.cget("bg")
                    file.write(f"{color}|{content}\n")
        messagebox.showinfo("Save Notes", "Notes saved successfully!")
    
    def load_notes(self):
        if os.path.exists("notes.txt"):
            with open("notes.txt", "r") as file:
                for line in file:
                    color, content = line.strip().split("|", 1)
                    self.create_note_window(content=content, color=color)
        else:
            messagebox.showwarning("Load Notes", "No saved notes found.")
    
if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualDash(root)
    root.mainloop()