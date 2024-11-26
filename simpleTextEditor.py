# Simple Text Editor using Tkinter

from tkinter import *  # Import all necessary modules from tkinter
from tkinter import messagebox
import tkinter.filedialog  # For file dialog operations
import os # for file size calculation

# Initialize the root window with the title "Simple Text Editor"
root = Tk("Text Editor")
root.title("Simple Text Editor")

# Set the icon
root.iconbitmap('simpleTextEditor.ico')

# Configure the grid to allow resizing
root.rowconfigure(0, weight=1) # make row 0 expandable
root.columnconfigure(0, weight=1) # make column 0 expandable

# Create a Frame to hold the text widget and scrollbars
frame = Frame(root)
frame.grid(sticky="nsew")  # allow text widget to stretch in all directions with the window

# Configure the frame's grid to allow resizing
frame.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)

# Create a text widget in the frame
text = Text(frame, wrap=NONE)
text.grid(row=0, column=0, sticky="nsew")

#Create a vertical and horizontal scroll bars
v_scrollbar = Scrollbar(frame, orient=VERTICAL, command=text.yview)
h_scrollbar = Scrollbar(frame, orient=HORIZONTAL, command=text.xview)
v_scrollbar.grid(row=0, column=1, sticky="ns")
h_scrollbar.grid(row=1, column=0, sticky="ew")
text.config(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

# Set variable to track wrap state to True
wrap_var = BooleanVar(value=False)

# Status bar at the bottom
status_bar = Label(root, text="Insert Mode | Line: 1 Col: 1 | Size: 0 bytes", anchor=W, bd=1, relief=SUNKEN)
status_bar.grid(row=2, column=0, columnspan=2, sticky="ew")

# Track keyboard lock status and insert mode
caps_lock = False
insert_mode = True

def update_status_bar(event=None):
    """Update the status bar with file information and cursor position."""
    global insert_mode

    # Determine insert/overwrite mode
    if text["state"] == "normal":
        insert_mode = True
    else:
        insert_mode = False

    # Cursor position
    row, col = text.index(INSERT).split('.')
    row, col = int(row), int(col) + 1

    # File size
    content = text.get("1.0", "end-1c")
    file_size = len(content.encode('utf-8'))

    # Update status bar text
    status_text = f"{'Insert' if insert_mode else 'Overwrite'} Mode | Line: {row} Col: {col} | Size: {file_size} bytes"
    status_bar.config(text=status_text)


def check_caps_lock(event=None):
    """Check Caps Lock status."""
    global caps_lock
    caps_lock = not caps_lock
    status_bar.config(text=f"{'CAPS ON' if caps_lock else 'CAPS OFF'}")


# Bind cursor movement and content changes to update the status bar
text.bind("<KeyRelease>", update_status_bar)
text.bind("<ButtonRelease>", update_status_bar)

# Bind Caps Lock key
root.bind("<Caps_Lock>", check_caps_lock)

# Function to define creating a new file
def newFile():
    if check_unsaved_changes():
        text.delete('1.0', "end-1c")
        updateTitle()
        text.edit_modified(False)

def check_unsaved_changes():
    if text.edit_modified():
        result = messagebox.askyesnocancel(
            "Unsaved Changes",
            "You have unsaved changes. Do you want to save before proceeding?"
        )
        if result: # User chooses Yes
            saveFile()
        return result != None # Returns false if the user cancels
    return True

# Function to save the current text to a file
def saveFile():
    t = text.get("1.0", "end-1c")  # Get all text from the Text widget
    saveLocation = tkinter.filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )  
    # Prompt user to select file save location
    if saveLocation:
        try:
            with open (saveLocation, "w") as file1:
                file1.write(t)
            updateTitle(saveLocation)
            text.edit_modified(False) # Reset the Modified Flag
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {e}")

# Function to open a text file.
def openFile():
    if check_unsaved_changes():
        filePath = tkinter.filedialog.askopenfilename(
            title="Select a File",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )
    if filePath:
        try:
            with open(filePath, 'r') as file:
                fileContents = file.read()
                text.delete('1.0', "end-1c")
                text.insert('1.0', fileContents)
                updateTitle(filePath)
                text.edit_modified(False)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {e}")

# Quit the application
def exitApp():
    if check_unsaved_changes():
        root.quit()

#Toggle Word Wrap
def toggleWrap():
    current_wrap = text.cget("wrap") # get current wrap state
    if current_wrap == "none":
        text.config(wrap=WORD) # Enable word wrap
        h_scrollbar.grid_remove() # Hide the horizontal scrollbar
        wrap_var.set(True)
    else:
        text.config(wrap="none") #Disable word wrap
        h_scrollbar.grid() # Show the horizontal scrollbar
        wrap_var.set(False)

# Bind keyboard shortcuts
def bind_shortcuts():
    root.bind("<Control-o>", lambda event: openFile())  # Ctrl+O for Open
    root.bind("<Control-s>", lambda event: saveFile())  # Ctrl+S for Save
    root.bind("<Control-w>", lambda event: toggleWrap())  # Ctrl+W for Toggle Word Wrap
    root.bind("<Control-q>", lambda event: exitApp())  # Ctrl+Q for Exit
    root.bind("<Control-n>", lambda event: newFile()) # Ctrl+N for New

# Update the title bar
def updateTitle(filePath=None):
    if filePath:
        root.title(f"{filePath} - Simple Text Editor")
    else:
        root.title("Simple Text Editor")

# Create the Menu Bar
menuBar = Menu(root)

#create the 'File' Menu
fileMenu = Menu(menuBar, tearoff=0)
fileMenu.add_command(label="Open ...", command=openFile, accelerator="Ctrl+O") # Open file dialog
fileMenu.add_command(label="Save ...", command=saveFile,accelerator="Ctrl+S") # Save As file dialog
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=exitApp, accelerator="Ctrl+Q") # Exit the appliction
fileMenu.add_command(label="New", command=newFile, accelerator="Ctrl+N") # Create a new file
menuBar.add_cascade(label="File", menu=fileMenu)

#Create the 'Format' Menu
formatMenu = Menu(menuBar, tearoff=0)
formatMenu.add_checkbutton(label="Word Wrap",  variable=wrap_var, command=toggleWrap, accelerator="Ctrl+W")
menuBar.add_cascade(label="Format", menu=formatMenu)

# Attach menu bar to the root window
root.config(menu=menuBar)

# Start the Tkinter main event loop
root.mainloop()