import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import sys

# class
import tkinter as tk
from tkinter import ttk

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        x, y,cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + cy + self.widget.winfo_rooty() + 25
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tooltip, text=self.text, justify='left', background="#ffffe0", relief='solid', borderwidth=1, font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()


# functions
def get_folder_path():
    folder_path_var=filedialog.askdirectory()
    folder_path.set(folder_path_var)

def run():
    # clearing the output box
    output_box.delete("1.0",tk.END)

    folder_path_value=folder_path.get()
    new_extension_value=new_extension.get()
    excluded_extensions_value=excluded_extensions.get()
    excluded_extensions_list=excluded_extensions_value.split(",")

    if folder_path_value=='' or new_extension=='':
        pass
    else:
        folder_path_value=os.path.abspath(folder_path_value)
        files=os.listdir(folder_path_value)
        output_box.insert(tk.END,"Affected files are: \n")
        count=0
        for i in files:
            a=i.split(".")
            if  a[-1].lower() not in excluded_extensions_list:
                del a[-1]
                if "." in new_extension_value:
                    a.append(new_extension_value)
                else:
                    a.append("."+ new_extension_value)
                final_path=os.path.join(folder_path_value,"".join(a))
                src_path=os.path.join(folder_path_value,i)
                os.rename(src_path,final_path)
                output_box.insert(tk.END,src_path+"\n")
                count=count+1
        output_box.insert(tk.END,str(count)+" files are affected")


# creating root window
root = tk.Tk()
root.geometry("700x400")
root.minsize(700,400)
root.maxsize(700,400)
root.title("ERT")



title_icon=tk.PhotoImage(file=r"images\title.png")
root.iconphoto(False,title_icon)


# creating fonts,bg
text_box_font=("serif",12,"bold")
title_font=("Futura",15,"bold")

# creating label
tk.Label(root,text="Extension Recovery Tool- ERT",font=title_font,bg="blue",fg="white").grid(row=0,column=1)
tk.Label(root,text="Folder Path:",font=text_box_font).grid(row=1,column=0)
tk.Label(root,text="New Extension:",font=text_box_font).grid(row=2,column=0)
tk.Label(root,text="Excluded Extensions:",font=text_box_font).grid(row=3,column=0)

# creating entry
folder_path=tk.StringVar()
new_extension=tk.StringVar()
excluded_extensions=tk.StringVar()
tk.Entry(root,textvariable=folder_path).grid(row=1,column=1)
tk.Entry(root,textvariable=new_extension).grid(row=2,column=1)
excluded_extensions_box=tk.Entry(root,textvariable=excluded_extensions)
excluded_extensions_box.grid(row=3,column=1)

# Create a dropdown menu
new_extension_options = ["pdf", "jpg", "png","txt","gif","mp3","mp4"]
ttk.OptionMenu(root, new_extension, new_extension_options[0], *new_extension_options).grid(row=2,column=2)


# creating browse folder button
tk.Button(root,text="Browse",font=("serif",10,"bold"),command=get_folder_path).grid(row=1,column=2)

# creating run button
tk.Button(root,text="Run",font=("serif",15,"bold"),background="orange",fg="white",command=run).grid(row=4,column=1)

# for ouput window
output_box=tk.Text(root,width=40,height=7)
output_box.grid(row=5,column=1)

# Create a tooltip for the excluded_extensions
Tooltip(excluded_extensions_box, "You can supply multple \nextension separated by comma(,)")


root.mainloop()
