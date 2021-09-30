# Description
This project provides a minimal GUI in Python in order to generate animated GIF pictures from a list of pictures.
Technically, this application is implemented using the [Tkinter](https://docs.python.org/3/library/tkinter.html) library 
for the GUI part, and relies on the [Pillow](https://pillow.readthedocs.io/en/stable/) library for the picture 
manipulation.

#Installation
## Requirements
The application requires [Python3](https://www.python.org/download/releases/3.0/) to be installed et and setup.

## Installing
```pip3 install -r requirements.txt```

#Usage
```python3 main.py```
The GUI is split in 4 parts:
1. the *input* part: this is where you can select a set of files to add them latter to the sequence. Once a folder is 
selected, all the files it contains will be listed in order. It is possible to change of directory anytime, the content
of the list will be updated.
2. Select the files to be added to the sequence by using the *Add* button. Adding the file is done in order. Be careful
as the input list is a multi-select, and clicking *Add* does not unselect the selected input files (it may be improved 
in the future?).
3. The sequence control: after adding all the required pictures in the sequence, it is still possible to reorder them or
 remove some of them.
4. The output: select an output folder, a file name, and a period for frame animation (in milliseconds), then click 
*generate*. **IF THE FILE ALREADY EXISTS, IT WILL BE OVERRIDDEN, WITHOUT ASKING ANY CONFIRMATION**

# Why this project
I needed this small tool as I couldn't an offline one which makes it easy to select files from a folder and re-order 
them. [GIMP](https://www.gimp.org/) is a great tool, but I couldn't find a way- to create animated GIF in a few clicks...
I may have missed something here.
I hope that the GUI may be useful to other peoples and is self-explanatory enough...if not, please do not hesitate to 
contribute to the code.