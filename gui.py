import tkinter as tk
from tkinter import filedialog

import os
import subprocess


# close the gui once both selections are submitted
def submit():
    selected_stain = stain_var.get()
    
    if selected['dir'] and selected_stain != 'Select a stain':
        selected['stain'] = selected_stain
        root.destroy()
    else:
        print('Select a directory and stain.')


# open directory selecter
def select_dir():
    dir = filedialog.askdirectory(title = 'Select patient directory')
    if dir:
        selected['dir'] = dir
        dir_label.config(text = f'Selected directory: {dir}')


# dictionary to store user selections
selected = {'dir': None, 'stain': None}

# initialize gui window
root = tk.Tk()
root.title('Slice Extraction')
root.geometry('400x300')

# button to select patient directory
dir_button = tk.Button(root, text = 'Select patient directory', 
                       command = select_dir, bg = 'navy', fg = 'white')
dir_button.pack(pady = 5)

# display selected directory
dir_label = tk.Label(root, text = 'No directory selected')
dir_label.pack(pady = 0)

# add stain variable to the gui
stain_var = tk.StringVar(root)
stain_var.set('Select a stain')

# add stain option menu to the gui
stains = ['H&E', 'Melan', 'Sox10', 'ALL STAINS']
stain_menu = tk.OptionMenu(root, stain_var, *stains)
stain_menu.config(bg = 'navy', fg = 'white')
stain_menu.pack(pady = 30)

# add button to submit selections
submit_button = tk.Button(root, text = 'Submit', command = submit)
submit_button.pack(pady = 0)

# run the gui
root.mainloop()

if selected['dir'] and selected['stain']:

    if selected['stain'] == 'ALL STAINS':
        # select all available stains
        todo = list(map(lambda x: x.lower(), stains[:-1]))
    else:
        todo = [selected['stain'].lower()]

    # run the cropping script for each patient in the selected directory
    for patient in os.listdir(selected['dir']):
        
        for stain in todo:
            if stain in patient.lower():
                id = f'{patient.split()[0]}/{stain}'

                subprocess.run(['python3', 'separate.py', id, os.path.join(selected['dir'], patient)])

else:
    print('Selection canceled')