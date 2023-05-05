import tkinter as tk
from tkinter import filedialog
import os
import json
import magic

with open('mime_to_ext.json','r') as f:
    mime_to_ext=json.load(f)

# functions
def get_folder_path():
    folder_path_var=filedialog.askdirectory()
    folder_path.set(folder_path_var)

def run():
    # clearing the output box
    output_box.delete("1.0",tk.END)
    folder_path_value=folder_path.get()
    if folder_path_value!='':
        folder_path_value=os.path.abspath(folder_path_value)
        files=os.listdir(folder_path_value)
        output_box.insert(tk.END,"Affected files are: \n")
        count=0
        for filename in files:
            file_path = os.path.join(folder_path_value, filename)
            mime_type=magic.from_file(file_path,mime=True)
            # Get extension based on mime type
            ext=mime_to_ext.get(mime_type)
            if os.path.splitext(filename)[1].lower()==ext or ext==None:
                continue
            
            # construct the new filename with the original extension
            new_filename = os.path.splitext(filename)[0] + ext
            final_path=os.path.join(folder_path_value,new_filename)
            src_path=os.path.join(folder_path_value,filename)
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

# creating entry
folder_path=tk.StringVar()
tk.Entry(root,textvariable=folder_path).grid(row=1,column=1)

# creating browse folder button
tk.Button(root,text="Browse",font=("serif",10,"bold"),command=get_folder_path).grid(row=1,column=2)

# creating run button
tk.Button(root,text="Run",font=("serif",15,"bold"),background="orange",fg="white",command=run).grid(row=4,column=1)

# for ouput window
output_box=tk.Text(root,width=40,height=7)
output_box.grid(row=5,column=1)

root.mainloop()
