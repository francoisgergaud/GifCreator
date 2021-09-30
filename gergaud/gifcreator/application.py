import glob
import re
from PIL import Image
from tkinter import Tk, Frame, Label, LabelFrame, Listbox, filedialog, Button, Scrollbar, LEFT, RIGHT, BOTH, BOTTOM, TOP, \
    HORIZONTAL, messagebox, Entry
from os.path import basename, sep


class GifCreator:
    current_directory_file_list = []
    sequence_file_list = []
    current_directory_name = None
    output_directory_name = None
    input_file_listbox = None
    sequence_listbox = None
    output_size = None

    def __init__(self):
        root = Tk()
        root.title("GIF creator")

        # the windows frames. fro, the main frame:
        # --input---add--sequence-sequence control-
        # --output---------------------------------
        main_frame = Frame(root)
        main_frame.pack(side=TOP, fill=BOTH)
        input_frame = LabelFrame(main_frame, text="input")
        input_frame.pack(padx=10, pady=10, side=LEFT, fill=BOTH)
        add_frame = Frame(main_frame)
        add_frame.pack(side=LEFT, fill=BOTH)
        sequence_frame = LabelFrame(main_frame, text="sequence")
        sequence_frame.pack(padx=10, pady=10, side=LEFT, fill=BOTH)
        sequence_control_frame = Frame(main_frame)
        sequence_control_frame.pack(side=LEFT, fill=BOTH)
        output_frame = LabelFrame(root, text="output")
        output_frame.pack(padx=10, pady=10,side=BOTTOM, fill=BOTH)

        # the input frame
        input_directory_frame = Frame(input_frame)
        input_directory_frame.pack(side=TOP)
        open_input_directory_chooser = Button(input_directory_frame, text="Choose directory",
                                              command=self.set_input_directory)
        open_input_directory_chooser.pack(padx=3, pady=3)
        directory_name_label = Label(input_directory_frame, text="No directory open")
        directory_name_label.pack()
        horizontal_scrollbar = Scrollbar(input_frame, orient=HORIZONTAL)
        horizontal_scrollbar.pack(side=BOTTOM, fill=BOTH)
        input_file_listbox = Listbox(input_frame)
        input_file_listbox.pack(side=LEFT, fill=BOTH)
        vertical_scrollbar = Scrollbar(input_frame)
        vertical_scrollbar.pack(side=LEFT, fill=BOTH)
        input_file_listbox.config(xscrollcommand=horizontal_scrollbar.set, yscrollcommand=vertical_scrollbar.set,
                                  selectmode="multiple")
        vertical_scrollbar.config(command=input_file_listbox.yview)
        horizontal_scrollbar.config(command=input_file_listbox.xview)
        self.directory_name_label = directory_name_label
        self.input_file_listbox = input_file_listbox

        # the add frame
        add_button = Button(add_frame, text="Add", command=self.add_input_to_sequence)
        add_button.pack(padx=3, pady=60)

        # the sequence frame
        horizontal_scrollbar = Scrollbar(sequence_frame, orient=HORIZONTAL)
        horizontal_scrollbar.pack(side=BOTTOM, fill=BOTH)
        sequence_listbox = Listbox(sequence_frame)
        sequence_listbox.pack(side=LEFT, fill=BOTH)
        vertical_scrollbar = Scrollbar(sequence_frame)
        vertical_scrollbar.pack(side=LEFT, fill=BOTH)
        sequence_listbox.config(xscrollcommand=horizontal_scrollbar.set, yscrollcommand=vertical_scrollbar.set)
        vertical_scrollbar.config(command=sequence_listbox.yview)
        horizontal_scrollbar.config(command=sequence_listbox.xview)

        remove_button = Button(sequence_control_frame, text="Remove", command=self.remove_selected_item_from_sequence)
        remove_button.pack(padx=3, pady=3)
        move_up_button = Button(sequence_control_frame, text="Up", command=self.move_selected_item_up)
        move_up_button.pack(padx=3, pady=3)
        move_down_button = Button(sequence_control_frame, text="Down", command=self.move_selected_item_down)
        move_down_button.pack(padx=3, pady=3)
        self.sequence_listbox = sequence_listbox

        # the output frame
        open_output_directory_chooser = Button(output_frame, text="Choose directory", command=self.set_output_directory)
        open_output_directory_chooser.pack(side=LEFT, padx=3, pady=3)
        output_directory_name_label = Label(output_frame, text="No directory open")
        output_directory_name_label.pack(side=LEFT)
        output_file_name_label = Label(output_frame, text="output filename")
        output_file_name_label.pack(side=LEFT)
        output_file_name_entry = Entry(output_frame)
        proc = output_file_name_entry.register(self.is_valid_filename)
        output_file_name_entry.config(validate="key", validatecommand=(proc, "%P", "%d"))
        output_file_name_entry.pack(side=LEFT)
        output_duration_label = Label(output_frame, text="frame duration (ms)")
        output_duration_label.pack(side=LEFT)
        output_duration_entry = Entry(output_frame)
        proc = output_duration_entry.register(self.is_valid_duration)
        output_duration_entry.config(validate="key", validatecommand=(proc, "%P", "%d"))
        output_duration_entry.pack(side=LEFT)
        generate_button = Button(output_frame, text="Generate", command=self.make_gif)
        generate_button.pack(side=LEFT, padx=3, pady=3)
        self.output_directory_name_label = output_directory_name_label
        self.output_file_name_entry = output_file_name_entry
        self.output_duration_entry = output_duration_entry

        root.mainloop()

    def add_input_to_sequence(self):
        for index in self.input_file_listbox.curselection():
            file_name = self.input_file_listbox.get(index)
            self.sequence_listbox.insert(self.input_file_listbox.size(), file_name)
            self.sequence_file_list.append(self.current_directory_name + sep + file_name)

    def remove_selected_item_from_sequence(self):
        item_to_remove_indexes = self.sequence_listbox.curselection()
        if len(item_to_remove_indexes) < 1:
            messagebox.showerror("Error", "No item selected")
            return
        item_to_remove_index = item_to_remove_indexes[0]
        del self.sequence_file_list[item_to_remove_index]

    def move_selected_item_up(self):
        item_to_move_indexes = self.sequence_listbox.curselection()
        if len(item_to_move_indexes) < 1:
            messagebox.showerror("Error", "No item selected")
            return
        item_to_move_index = item_to_move_indexes[0]
        if item_to_move_index > 0:
            file_name = self.sequence_listbox.get(item_to_move_index)
            file_path = self.sequence_file_list[item_to_move_index]
            self.sequence_listbox.delete(item_to_move_index)
            del self.sequence_file_list[item_to_move_index]
            self.sequence_listbox.insert(item_to_move_index - 1, file_name)
            self.sequence_listbox.selection_set(item_to_move_index - 1)
            self.sequence_file_list.insert(item_to_move_index - 1, file_path)

    def move_selected_item_down(self):
        item_to_move_indexes = self.sequence_listbox.curselection()
        if len(item_to_move_indexes) < 1:
            messagebox.showerror("Error", "No item selected")
            return
        item_to_move_index = item_to_move_indexes[0]
        if item_to_move_index < self.sequence_listbox.size():
            file_name = self.sequence_listbox.get(item_to_move_index)
            file_path = self.sequence_file_list[item_to_move_index]
            self.sequence_listbox.delete(item_to_move_index)
            del self.sequence_file_list[item_to_move_index]
            self.sequence_listbox.insert(item_to_move_index + 1, file_name)
            self.sequence_listbox.selection_set(item_to_move_index + 1)
            self.sequence_file_list.insert(item_to_move_index + 1, file_path)

    def set_input_directory(self):
        self.current_directory_name = filedialog.askdirectory()
        for _ in self.current_directory_file_list:
            self.input_file_listbox.delete(0)
        self.current_directory_file_list = glob.glob(f"{self.current_directory_name}/*.*")
        self.current_directory_file_list.sort()
        self.directory_name_label['text'] = self.current_directory_name
        for idx, filename in enumerate(self.current_directory_file_list):
            self.input_file_listbox.insert(idx, basename(filename))

    def set_output_directory(self):
        self.output_directory_name = filedialog.askdirectory()
        self.output_directory_name_label['text'] = self.output_directory_name

    def make_gif(self):
        output_directory_name = self.output_directory_name
        if not output_directory_name:
            messagebox.showerror("Error", "No output directory set")
            return
        output_filename = self.output_file_name_entry.get()
        if not output_filename:
            messagebox.showerror("Error", "No output filename set")
            return
        duration = self.output_duration_entry.get()
        if not duration:
            messagebox.showerror("Error", "No frame duration set")
            return
        picture_cache = {}
        frames = []
        for file in self.sequence_file_list:
            if file not in picture_cache:
                picture = Image.open(file)
                if self.output_size is None:
                    self.output_size = picture.size
                picture_cache[file] = picture.resize(self.output_size)
            frames.append(picture_cache[file])
        # pictures = [Image.open(image) for image in glob.glob(f"{frame_folder}/*.*")]
        output_path = output_directory_name + sep + output_filename
        if len(frames) > 0:
            frames[0].save(output_path, format="GIF", append_images=frames[1:], save_all=True, duration=int(duration),
                           loop=0)
            messagebox.showinfo("Info", "Gif generated")

    def is_valid_filename(self, input_string, action_type):
        if action_type == '1':  # insert
            match = re.search(r"[\w\-_]+$", input_string)
            if match is None:
                messagebox.showerror("Error", "invalid character for output file")
            return match is not None
        return True

    def is_valid_duration(self, input_string, action_type):
        if action_type == '1':  # insert
            if not input_string.isdigit():
                messagebox.showerror("Error", "invalid character for duration")
                return False
        return True
