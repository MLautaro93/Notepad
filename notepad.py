# Import library
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import os

# Create root widget
root = tk.Tk()
root.title('Notepad')

# Notepad window
notepad = tk.Text()

# Define functions for menu commands
def new():
    # Allow user to save changes
    mb = messagebox.askyesnocancel(root.title(), 'Do you want to save changes?')
    if mb != None:
        if mb == True:
            save()
        notepad.delete(0.0, tk.END)
        root.title('Notepad')

def open_file():
    # Allow user to save changes
    mb = messagebox.askyesnocancel(root.title(), 'Do you want to save changes?')
    if mb != None:
        if mb == True:
            save()
        
        global my_file
        my_file = filedialog.askopenfile(mode = 'r')
        if my_file != None:
            data = my_file.read()
            notepad.delete(0.0, tk.END)
            notepad.insert(0.0, data)
            # Change main window title
            name = os.path.basename(my_file.name)
            root.title(name)
            my_file.close()

def save():
    try:
        with open(my_file.name, mode = 'w') as file:
            data = notepad.get(1.0, tk.END)
            file.write(data)
            file.truncate()
            file.close()
    except:
        # If file has not been previously saved, we call "save as" function.
        save_as()   

def save_as():
    global my_file
    my_file = filedialog.asksaveasfile(mode = 'w', defaultextension = '.txt')
    if my_file != None:
        data = notepad.get(1.0, tk.END)
        my_file.write(data)
        # Change main window title
        name = os.path.basename(my_file.name)
        root.title(name)
        my_file.close()

def exit():
    if messagebox.askyesno(root.title(), 'Are you sure you want to exit?'):
        root.destroy()

def cut():
    notepad.event_generate('<<Cut>>')

def copy():
    notepad.event_generate('<<Copy>>')

def paste():
    notepad.event_generate('<<Paste>>')

def delete():
    notepad.event_generate('<<Clear>>')

def find():
    notepad.tag_remove('found', 1.0, tk.END)
    query = simpledialog.askstring('Find', 'Find:')
    if query:
        # Index
        idx = 1.0
        while True:
            idx = notepad.search(pattern = query, index = idx, nocase = 1, stopindex = tk.END)
            if not idx: break
            lastidx = '%s + %dc' % (idx, len(query))
            # Overwrite 'found' from idx to lastidx
            notepad.tag_add('found', idx, lastidx)
            idx = lastidx
        # Highlight text
        notepad.tag_configure('found', foreground = 'white', background = 'blue')
        # Function for disabling hightlight at a click
        notepad.bind('<1>', disable)

def disable(event):
    notepad.tag_configure('found', foreground = 'black', background = 'white')

def select_all():
    notepad.event_generate('<<SelectAll>>')

def about():
    messagebox.showinfo('About Notepad', '© Lautaro Mizrahi. All rights reserved.')

# Main menu
menu_bar = tk.Menu()
root.configure(menu = menu_bar)

# File menu
file_menu = tk.Menu(menu_bar, tearoff = False)
menu_bar.add_cascade(label = 'File', menu = file_menu)
file_menu.add_command(label = 'New', command = new)
file_menu.add_command(label = 'Open...', command = open_file)
file_menu.add_command(label = 'Save', command = save)
file_menu.add_command(label = 'Save As...', command = save_as)
file_menu.add_separator()
file_menu.add_command(label = 'Exit', command = exit)

# Edit menu
edit_menu = tk.Menu(menu_bar, tearoff = False)
menu_bar.add_cascade(label = 'Edit', menu = edit_menu)
edit_menu.add_command(label = 'Cut', command = cut)
edit_menu.add_command(label = 'Copy', command = copy)
edit_menu.add_command(label = 'Paste', command = paste)
edit_menu.add_command(label = 'Delete', command = delete)
edit_menu.add_separator()
edit_menu.add_command(label = 'Find...', command = find)
edit_menu.add_separator()
edit_menu.add_command(label = 'Select All', command = select_all)

# Help menu
help_menu = tk.Menu(menu_bar, tearoff = False)
menu_bar.add_cascade(label = 'Help', menu = help_menu)
help_menu.add_command(label = 'About Notepad', command = about)


notepad.pack(expand = True, fill = 'both')
root.mainloop()
