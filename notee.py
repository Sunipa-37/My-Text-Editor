import tkinter as tk
from tkinter import filedialog, messagebox
def new_file():
    content = text.get("1.0", "end-1c") 
    if (len(content)>0):
        if messagebox.askyesno("confirm delete"," Do you want to save the current file?"):
            save_as_file()
    text.delete(1.0,tk.END)

def open_file():
    file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files","*.txt")])
    if file_path:
        with open(file_path, 'r', encoding="utf-8", errors="ignore" ) as file:
            text.delete(1.0,tk.END)
            text.insert(tk.END , file.read())

def save_as_file():
    file_path = filedialog.asksaveasfilename(defaultextension= ".txt", filetypes=[("Text files","*.txt")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(text.get(1.0,tk.END))
            messagebox.showinfo("Info","FILE SAVED SUCCESSFULLY!.")

def update_status(event=None):
    content = text.get("1.0", "end-1c")  # all text except last newline
    words = len(content.split())
    chars = len(content)
    lines = len(content.split("\n"))
    status.config(text=f"Words: {words} | Chars: {chars} | Lines: {lines}")

current_font_size = 12
def zoom_in():
    global current_font_size
    current_font_size += 4
    text.config(font=("Helvetica", current_font_size))
def zoom_out():
    global current_font_size
    if current_font_size > 6:
        current_font_size -= 4
    text.config(font=("Helvetica", current_font_size))

def apply_theme():
    if theme_var.get() == "Light":
        # Light mode
        text.config(bg="white", fg="black", insertbackground="black")
        root.config(bg="SystemButtonFace")
        status.config(bg="SystemButtonFace", fg="black")
        menu.config(bg="SystemButtonFace", fg="black")
        for m in [file_menu, edit_menu, view_menu]:
            m.config(bg="SystemButtonFace", fg="black", activebackground="lightgray", activeforeground="black")
    else:
        # Dark mode
        text.config(bg="black", fg="white", insertbackground="white")
        root.config(bg="black")
        status.config(bg="black", fg="white")
        menu.config(bg="black", fg="white")
        for m in [file_menu, edit_menu, view_menu]:
            m.config(bg="black", fg="white", activebackground="gray20", activeforeground="white")



def on_exit():
    content = text.get("1.0", "end-1c") 
    if (len(content)>0):
        if messagebox.askyesno("confirm delete"," Do you want to save the current file?"):
            save_as_file()
    if messagebox.askyesno("Confirm Exit", "Are you sure you want to exit?"):
        root.destroy()

def Cut():
    text.event_generate("<<Cut>>")

def Copy():
    text.event_generate("<<Copy>>")

def Paste():
    text.event_generate("<<Paste>>")
def find_replace():
    fr = tk.Toplevel(root)
    fr.title("Find & Replace")
    fr.geometry("400x150")
    fr.transient(root)   # Always on top of editor
    fr.resizable(False, False)

    tk.Label(fr, text="Find:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    find_entry = tk.Entry(fr, width=30)
    find_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(fr, text="Replace:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    replace_entry = tk.Entry(fr, width=30)
    replace_entry.grid(row=1, column=1, padx=10, pady=10)

    def do_find():
        text.tag_remove("highlight", "1.0", tk.END)
        find_text = find_entry.get()
        if find_text:
            start_pos = "1.0"
            while True:
                start_pos = text.search(find_text, start_pos, stopindex=tk.END)
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(find_text)}c"
                text.tag_add("highlight", start_pos, end_pos)
                start_pos = end_pos
            text.tag_config("highlight", background="yellow", foreground="black")

    def do_replace():
        find_text = find_entry.get()
        replace_text = replace_entry.get()
        content = text.get("1.0", tk.END)
        new_content = content.replace(find_text, replace_text)
        text.delete("1.0", tk.END)
        text.insert("1.0", new_content)
        update_status()

    tk.Button(fr, text="Find", command=do_find).grid(row=2, column=0, padx=10, pady=10)
    tk.Button(fr, text="Replace All", command=do_replace).grid(row=2, column=1, padx=10, pady=10)



root = tk.Tk()
root.title("My Text Editor")

root.geometry("800x600")

theme_var = tk.StringVar(root, value="Light")


menu = tk.Menu(root)
root.config(menu=menu)
file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File",menu=file_menu)
file_menu.add_command(label="New",command=new_file, accelerator="ctrl+N")
file_menu.add_command(label="Open",command=open_file, accelerator="ctrl+O")
file_menu.add_command(label="Save",command=save_as_file, accelerator="ctrl+S")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=on_exit, accelerator="ctrl+Q")

edit_menu=tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Edit",menu=edit_menu)
edit_menu.add_command(label='Undo',command=lambda: text.edit_undo(), accelerator="ctrl+Z")
edit_menu.add_command(label='Redo', command=lambda: text.edit_redo(), accelerator="ctrl+Y")
edit_menu.add_separator()
edit_menu.add_command(label="Cut", command=Cut, accelerator="ctrl+X")
edit_menu.add_command(label="Copy", command=Copy, accelerator="ctrl+C")
edit_menu.add_command(label="Paste", command=Paste, accelerator="ctrl+V")
edit_menu.add_separator()
edit_menu.add_command(label="Find & Replace", command=find_replace, accelerator="Ctrl+F")


dark_mode_var = tk.BooleanVar(value=False) 
view_menu=tk.Menu(menu,tearoff=0)
menu.add_cascade(label="View", menu=view_menu)
view_menu.add_command(label="Zoom in", command=zoom_in, accelerator="ctrl+shift+")
view_menu.add_command(label="Zoom out", command=zoom_out, accelerator="ctrl+-")
#prev:::: view_menu.add_checkbutton(label="Dark Mode", variable= dark_mode_var, command=toggle_dark_mode, onvalue=True, offvalue=False, accelerator="Ctrl+D")
view_menu.add_radiobutton(label="Light Mode ☀", variable=theme_var, value="Light", command=apply_theme)
view_menu.add_radiobutton(label="Dark Mode 🌙", variable=theme_var, value="Dark", command=apply_theme)


# File menu shortcuts
root.bind("<Control-n>", lambda event: new_file())
root.bind("<Control-o>", lambda event: open_file())
root.bind("<Control-s>", lambda event: save_as_file())
root.bind("<Control-q>", lambda event: on_exit())

# Edit menu shortcuts
root.bind("<Control-z>", lambda event: text.edit_undo())
root.bind("<Control-y>", lambda event: text.edit_redo())
root.bind("<Control-x>", lambda event: Cut())
root.bind("<Control-c>", lambda event: Copy())
root.bind("<Control-v>", lambda event: Paste())

# View menu shortcuts
root.bind("<Control-plus>", lambda event: zoom_in())
root.bind("<Control-minus>", lambda event: zoom_out())
root.bind("<Control-f>", lambda event: find_replace())


text = tk.Text(root, wrap=tk.WORD, font=("Helvetica",12), fg="black", undo=True)
text.pack(expand=tk.YES, fill=tk.BOTH)

# Apply initial menu style (light mode by default)
menu.config(bg="SystemButtonFace", fg="black")
for m in [file_menu, edit_menu, view_menu]:
    m.config(bg="SystemButtonFace", fg="black", activebackground="lightgray", activeforeground="black")


status = tk.Label(root, text="Words: 0 | Characters: 0 | Lines: 0", anchor="w")
status.pack(side="bottom", fill="x")


text.bind("<KeyRelease>", update_status)
root.protocol("WM_DELETE_WINDOW", on_exit)

root.mainloop()