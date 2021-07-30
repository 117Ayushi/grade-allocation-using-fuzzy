try: 
    import Tkinter as tk
except ImportError:
    import tkinter as tk

import pandas as pd
from fcmeans import FCM
from tkinter import filedialog

class EditorApp:

    def __init__(self, master, dataframe, edit_rows=[]):
        """ master    : tK parent widget
        dataframe : pandas.DataFrame object"""
        self.root = master
        self.root.minsize(width=1000, height=700)
        self.root.title('Grade Allocation System')

        self.main = tk.Frame(self.root)
        self.main.pack(fill=tk.BOTH, expand=True)

        self.lab_opt = {'background': 'darkgreen', 'foreground': 'white'}

# #       the dataframe
#         import_file_path = filedialog.askopenfilename()
#         self.df = pd.read_excel (import_file_path)
#         # self.df = dataframe
#         self.dat_cols = list(self.df)
#         if edit_rows:
#             self.dat_rows = edit_rows
#         else:
#             self.dat_rows = range(len(self.df))
#         self.rowmap = {i: row for i, row in enumerate(self.dat_rows)}

# #       subset the data and convert to giant list of strings (rows) for viewing
#         self.sub_data = self.df.loc[self.dat_rows, self.dat_cols]
#         self.sub_datstring = self.sub_data.to_string(
#             index=False, col_space=13).split('\n')
#         self.title_string = self.sub_datstring[0]

# # save the format of the lines, so we can update them without re-running
# # df.to_string()
#         self._get_line_format(self.title_string)

#       fill in the main frame
        self._fill()

#       updater for tracking changes to the database
        self.update_history = []

##################
# ADDING WIDGETS #
##################
    def _fill(self):
        self.canvas = tk.Canvas(self.main)
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)

        self._init_scroll()
        self._init_lb()
        self._pack_config_scroll()
        self._pack_bind_lb()
        # self._fill_listbox()
        # self._make_editor_frame()
        # self._sel_mode()
        self._get_excel()
##############
# SCROLLBARS #
##############
    def _init_scroll(self):
        self.scrollbar = tk.Scrollbar(self.canvas, orient="vertical")
        self.xscrollbar = tk.Scrollbar(self.canvas, orient="horizontal")

    def _pack_config_scroll(self):
        self.scrollbar.config(command=self.lb.yview)
        self.xscrollbar.config(command=self._xview)
        self.scrollbar.pack(side="right", fill="y")
        self.xscrollbar.pack(side="bottom", fill="x")

    def _onMouseWheel(self, event):
        self.title_lb.yview("scroll", event.delta, "units")
        self.lb.yview("scroll", event.delta, "units")
        return "break"

    def _xview(self, *args):
        """connect the yview action together"""
        self.lb.xview(*args)
        self.title_lb.xview(*args)

################
# MAIN LISTBOX #
################
    def _init_lb(self):
        self.title_lb = tk.Listbox(self.canvas, height=1,
                                   yscrollcommand=self.scrollbar.set,
                                   xscrollcommand=self.xscrollbar.set,
                                   exportselection=False)

        self.lb = tk.Listbox(self.canvas,
                             yscrollcommand=self.scrollbar.set,
                             xscrollcommand=self.xscrollbar.set,
                             exportselection=False,
                             selectmode=tk.EXTENDED)

    def _pack_bind_lb(self):
        self.title_lb.pack(fill=tk.X)
        self.lb.pack(fill="both", expand=True)
        self.title_lb.bind("<MouseWheel>", self._onMouseWheel)
        self.lb.bind("<MouseWheel>", self._onMouseWheel)

    def _fill_listbox(self):
        """ fill the listbox with rows from the dataframe"""
        self.title_lb.insert(tk.END, self.title_string)
        for line in self.sub_datstring[1:]:
            self.lb.insert(tk.END, line)
            self.lb.bind('<ButtonRelease-1>', self._listbox_callback)
        self.lb.select_set(0)

    def _listbox_callback(self, event):
        """ when a listbox item is selected"""
        items = self.lb.curselection()
        if items:
            new_item = items[-1]
            dataVal = str(
                self.df.loc[
                    self.rowmap[new_item],
                    self.opt_var.get()])
            self.entry_box_old.config(state=tk.NORMAL)
            self.entry_box_old.delete(0, tk.END)
            self.entry_box_old.insert(0, dataVal)
            self.entry_box_old.config(state=tk.DISABLED)

#####################
# FRAME FOR EDITING #
#####################
    def _make_editor_frame(self):
        """ make a frame for editing dataframe rows"""
        self.editorFrame = tk.Frame(
            self.main, bd=2, padx=2, pady=2, relief=tk.GROOVE)
        self.editorFrame.pack(fill=tk.BOTH, side=tk.LEFT)

#       column editor
        self.col_sel_lab = tk.Label(
            self.editorFrame,
            text='Select a column to edit:',
            **self.lab_opt)
        self.col_sel_lab.grid(row=0, columnspan=2, sticky=tk.W + tk.E)

        self.opt_var = tk.StringVar()
        self.opt_var.set(self.dat_cols[0])
        self.opt = tk.OptionMenu(
            self.editorFrame,
            self.opt_var,
            *
            list(
                self.df))
        self.opt.grid(row=0, columnspan=2, column=2, sticky=tk.E + tk.W)

        self.old_val_lab = tk.Label(
            self.editorFrame,
            text='Old value:',
            **self.lab_opt)
        self.old_val_lab.grid(row=1, sticky=tk.W, column=0)
        self.entry_box_old = tk.Entry(
            self.editorFrame,
            state=tk.DISABLED,
            bd=2,
            relief=tk.GROOVE)
        self.entry_box_old.grid(row=1, column=1, sticky=tk.E)

#       entry widget
        self.new_val_lab = tk.Label(
            self.editorFrame,
            text='New value:',
            **self.lab_opt)
        self.new_val_lab.grid(row=1, sticky=tk.E, column=2)
        self.entry_box_new = tk.Entry(self.editorFrame, bd=2, relief=tk.GROOVE)
        self.entry_box_new.grid(row=1, column=3, sticky=tk.E + tk.W)

#       make update button
        self.update_b = tk.Button(
            self.editorFrame,
            text='Update selection',
            relief=tk.RAISED,
            command=self._updateDF_multi)
        self.update_b.grid(row=2, columnspan=1, column=3, sticky=tk.W + tk.E)

#       make undo button
        self.undo_b = tk.Button(
            self.editorFrame,
            text='Undo',
            command=self._undo)
        self.undo_b.grid(row=2, columnspan=1, column=1, sticky=tk.W + tk.E)

################
# SELECT MODES #
################
    def _sel_mode(self):
        """ creates a frame for toggling between interaction modes wt"""
        self.mode_frame = tk.Frame(
            self.main, bd=2, padx=2, pady=2, relief=tk.GROOVE)
        self.mode_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        tk.Label(self.mode_frame, text='Selection mode', **
                 self.lab_opt).pack(fill=tk.BOTH, expand=tk.YES)

        self.mode_lb = tk.Listbox(
            self.mode_frame,
            height=2,
            width=16,
            exportselection=False)
        self.mode_lb.pack(fill=tk.BOTH, expand=tk.YES)
        self.mode_lb.insert(tk.END, 'Multiple selection')
        self.mode_lb.bind('<ButtonRelease-1>', self._mode_lb_callback)
        self.mode_lb.insert(tk.END, 'Find and replace')
        self.mode_lb.bind('<ButtonRelease-1>', self._mode_lb_callback)
        self.mode_lb.select_set(0)

    def _mode_lb_callback(self, event):
        items = self.mode_lb.curselection()
        if items[0] == 0:
            self._swap_mode('multi')
        elif items[0] == 1:
            self._swap_mode('findrep')

    def _swap_mode(self, mode='multi'):
        """swap between modes of interaction with database"""
        self.lb.selection_clear(0, tk.END)
        self._swap_lab(mode)
        if mode == 'multi':
            self.lb.config(state=tk.NORMAL)
            self.entry_box_old.config(state=tk.DISABLED)
            self.update_b.config(
                command=self._updateDF_multi,
                text='Update multi selection')
        elif mode == 'findrep':
            self.lb.config(state=tk.DISABLED)
            self.entry_box_old.config(state=tk.NORMAL)
            self.update_b.config(
                command=self._updateDF_findrep,
                text='Find and replace')
        self.entry_box_new.delete(0, tk.END)
        self.entry_box_new.insert(0, "Enter new value")

    def _swap_lab(self, mode='multi'):
        """ alter the labels on the editor frame"""
        if mode == 'multi':
            self.old_val_lab.config(text='Old value:')
            self.new_val_lab.config(text='New value:')
        elif mode == 'findrep':
            self.old_val_lab.config(text='Find:')
            self.new_val_lab.config(text='Replace:')

################
# ALLOCATE GRADE #
################
    def get_grade(x,max_grade_f,max_grade_e,max_grade_d_minus,max_grade_d,max_grade_c_minus,max_grade_c,max_grade_b_minus,max_grade_b,max_grade_a_minus,max_grade_a):
        if(x<max_grade_f):
            return 'F'
        elif(x<max_grade_e and x>=max_grade_f):
            return 'E'
        elif(x<max_grade_d_minus and x>=max_grade_e):
            return 'D-'
        elif(x<max_grade_d and x>=max_grade_d_minus):
            return 'D'
        elif(x<max_grade_c_minus and x>=max_grade_d):
            return 'C-'
        elif(x<max_grade_c and x>=max_grade_c_minus):
            return 'C'
        elif(x<max_grade_b_minus and x>=max_grade_c):
            return 'B-'
        elif(x<max_grade_b and x>=max_grade_b_minus):
            return 'B'
        elif(x<max_grade_a_minus and x>=max_grade_b):
            return 'A-'
        elif(x<max_grade_a and x>=max_grade_a_minus):
            return 'A'
        else:
            return 'OutOfBound'

    def display_excel(self,edit_rows=[]):
        self.dat_cols = list(self.df)
        if edit_rows:
            self.dat_rows = edit_rows
        else:
            self.dat_rows = range(len(self.df))
        self.rowmap = {i: row for i, row in enumerate(self.dat_rows)}

        self.sub_data = self.df.loc[self.dat_rows, self.dat_cols]
        self.sub_datstring = self.sub_data.to_string(
            index=False, col_space=13).split('\n')
        self.title_string = self.sub_datstring[0]
        self._fill_listbox()
        self._make_editor_frame()
        self._sel_mode()
        self._get_line_format(self.title_string)

    def allocate_grade(self):
        calculation_type = self.opt_var1.get()
        if(calculation_type == 'default'):
            self.df['EXPECTED GRADES'] = df['Total150'].apply(lambda x:get_grade(x,30,45,60,67,75,90,105,120,135,150))
            self.df.to_excel('output.xlsx')
            self.display_excel()
        
        elif(calculation_type == 'manual'):

            label20 = tk.Label(root, text='Enter the Max value for grade A: ')
            label20.config(font=('helvetica', 12))
            canvas1.create_window(450, 20, window=label20)

            entry20 = tk.Entry(root) 
            canvas1.create_window(650, 20, window=entry20) 

            label19 = tk.Label(root, text='Enter the Max value for grade A minus: ')
            label19.config(font=('helvetica', 12))
            canvas1.create_window(450, 50, window=label19)

            entry19 = tk.Entry(root) 
            canvas1.create_window(650, 50, window=entry19)

            label18 = tk.Label(root, text='Enter the Max value for grade B: ')
            label18.config(font=('helvetica', 12))
            canvas1.create_window(450, 80, window=label18)

            entry18 = tk.Entry(root) 
            canvas1.create_window(650, 80, window=entry18)

            label17 = tk.Label(root, text='Enter the Max value for grade B minus: ')
            label17.config(font=('helvetica', 12))
            canvas1.create_window(450, 110, window=label17)

            entry17 = tk.Entry(root) 
            canvas1.create_window(650, 110, window=entry17)

            label16 = tk.Label(root, text='Enter the Max value for grade C: ')
            label16.config(font=('helvetica', 12))
            canvas1.create_window(450, 140, window=label16)

            entry16 = tk.Entry(root) 
            canvas1.create_window(650, 140, window=entry16)

            label15 = tk.Label(root, text='Enter the Max value for grade C minus: ')
            label15.config(font=('helvetica', 12))
            canvas1.create_window(450, 170, window=label15)

            entry15 = tk.Entry(root) 
            canvas1.create_window(650, 170, window=entry15)

            label14 = tk.Label(root, text='Enter the Max value for grade D: ')
            label14.config(font=('helvetica', 12))
            canvas1.create_window(450, 200, window=label14)

            entry14 = tk.Entry(root) 
            canvas1.create_window(650, 200, window=entry14)

            label13 = tk.Label(root, text='Enter the Max value for grade D minus: ')
            label13.config(font=('helvetica', 12))
            canvas1.create_window(450, 230, window=label13)

            entry13 = tk.Entry(root) 
            canvas1.create_window(650, 230, window=entry13)

            label12 = tk.Label(root, text='Enter the Max value for grade E: ')
            label12.config(font=('helvetica', 12))
            canvas1.create_window(450, 260, window=label12)

            entry12 = tk.Entry(root) 
            canvas1.create_window(650, 260, window=entry12)

            label11 = tk.Label(root, text='Enter the Max value for grade F: ')
            label11.config(font=('helvetica', 12))
            canvas1.create_window(450, 290, window=label11)

            entry11 = tk.Entry(root) 
            canvas1.create_window(650, 290, window=entry11)

            calculate = tk.Button(text="Calculate", command=lambda: getGrades(self.df,entry11,entry12,entry13,entry14,entry15,entry16,entry17,entry18,entry19,entry20), bg='green', fg='white', font=('helvetica', 10, 'bold'))
            canvas1.create_window(530, 320, window=calculate)

        elif(calculation_type == 'fuzzy'):
            data2 = self.df[['Total150', 'Total150']]
            fcm = FCM(n_clusters=10)
            fcm.fit(data2)
            fcm_centers = fcm.centers
            predicted_membership = fcm.predict(data2)
            self.df['EXPECTED GRADES'] = predicted_membership
            fcm_centers.columns = ["Total150","feature"]
            fcm_centers["Cluster_id"] = [0,1,2,3,4,5,6,7,8,9]
            fcm_centers = fcm_centers.sort_values(by="Total150",ascending=[0])
            fcm_centers["Grade"] = ["A","A-","B","B-","C","C-","D","D-","E","F"]
            grade_dict = dict(zip(fcm_centers.Cluster_id, fcm_centers.Grade))
            self.df = self.df.replace({'EXPECTED GRADES': grade_dict})
            self.df.to_excel('output.xlsx')
            self.display_excel()

        elif(calculation_type == '4'):
            pass

        else:
            pass

        
################
# GET EXCEL #
################

    def _get_excel(self):
            self.mode_frame = tk.Frame(self.main, bd=2, padx=2, pady=2, relief=tk.GROOVE)
            self.mode_frame.pack(fill=tk.BOTH, side=tk.LEFT)
            tk.Button(self.mode_frame, text='Get Excel', command=self._open_file).pack()


    def _open_file(self,edit_rows=[]):
        #       the dataframe
        import_file_path = filedialog.askopenfilename()
        self.df = pd.read_excel (import_file_path)

## Adding new select frames
        self.editorFrame = tk.Frame(
            self.main, bd=2, padx=2, pady=2, relief=tk.GROOVE)
        self.editorFrame.pack(fill=tk.BOTH, side=tk.LEFT)

#       column editor
        self.col_sel_lab = tk.Label(
            self.editorFrame,
            text='Choose a option',
            **self.lab_opt)
        self.col_sel_lab.grid(row=0, columnspan=2, sticky=tk.W + tk.E)

        self.opt_var1 = tk.StringVar()
        self.opt_var1.set("default")
        self.opt = tk.OptionMenu(
            self.editorFrame,
            self.opt_var1,
            *
            list(["fuzzy"]))
        self.opt.grid(row=0, columnspan=2, column=4, sticky=tk.E + tk.W)
        self.update_b = tk.Button(
            self.editorFrame,
            text='Allocate Grade',
            relief=tk.RAISED,
            command=lambda:self.allocate_grade())
        self.update_b.grid(row=2, columnspan=1, column=3, sticky=tk.W + tk.E)
        

#################
# EDIT COMMANDS #
#################
    def _updateDF_multi(self):
        """ command for updating via selection"""
        self.col = self.opt_var.get()
        items = self.lb.curselection()
        self._track_items(items)

    def _updateDF_findrep(self):
        """ command for updating via find/replace"""
        self.col = self.opt_var.get()
        old_val = self.entry_box_old.get()
        try:
            items = pandas.np.where(
                self.sub_data[
                    self.col].astype(str) == old_val)[0]
        except TypeError as err:
            self.errmsg(
                '%s: `%s` for column `%s`!' %
                (err, str(old_val), self.col))
            return
        if not items.size:
            self.errmsg(
                'Value`%s` not found in column `%s`!' %
                (str(old_val), self.col))
            return
        else:
            self._track_items(items)
            self.lb.config(state=tk.DISABLED)

    def _undo(self):
        if self.update_history:
            updated_vals = self.update_history.pop()
            for idx, val in updated_vals['vals'].items():
                self.row = self.rowmap[idx]
                self.idx = idx
                self.df.set_value(self.row, updated_vals['col'], val)
                self._rewrite()
            self.sync_subdata()

####################
# HISTORY TRACKING #
####################
    def _track_items(self, items):
        """ this strings several functions together,
        updates database, tracks changes, and updates database viewer"""
        self._init_hist_tracker()
        for i in items:
            self.idx = i
            self.row = self.rowmap[i]
            self._track()
            self._setval()
            self._rewrite()
        self._update_hist_tracker()
#       update sub_data used w find and replace
        self.sync_subdata()

    def _setval(self):
        """ update database"""
        try:
            self.df.set_value(self.row, self.col, self.entry_box_new.get())
        except ValueError:
            self.errmsg(
                'Invalid entry `%s` for column `%s`!' %
                (self.entry_box_new.get(), self.col))

    def _init_hist_tracker(self):
        """ prepare to track a changes to the database"""
        self.prev_vals = {}
        self.prev_vals['col'] = self.col
        self.prev_vals['vals'] = {}

    def _track(self):
        """record a change to the database"""
        self.prev_vals['vals'][self.idx] = str(self.df.loc[self.row, self.col])

    def _update_hist_tracker(self):
        """ record latest changes to database"""
        self.update_history.append(self.prev_vals)

    def sync_subdata(self):
        """ syncs subdata with data"""
        self.sub_data = self.df.loc[self.dat_rows, self.dat_cols]

#################
# ERROR MESSAGE #
#################
    def errmsg(self, message):
        """ opens a simple error message"""
        errWin = tk.Toplevel()
        tk.Label(
            errWin,
            text=message,
            foreground='white',
            background='red').pack()
        tk.Button(errWin, text='Ok', command=errWin.destroy).pack()

##################
# UPDATING LINES #
##################
    def _rewrite(self):
        """ re-writing the dataframe string in the listbox"""
        new_col_vals = self.df.loc[self.row, self.dat_cols].astype(str).tolist()
        new_line = self._make_line(new_col_vals)
        if self.lb.cget('state') == tk.DISABLED:
            self.lb.config(state=tk.NORMAL)
            self.lb.delete(self.idx)
            self.lb.insert(self.idx, new_line)
            self.lb.config(state=tk.DISABLED)
        else:
            self.lb.delete(self.idx)
            self.lb.insert(self.idx, new_line)

    def _get_line_format(self, line):
        """ save the format of the title string, stores positions
            of the column breaks"""
        pos = [1 + line.find(' ' + n) + len(n) for n in self.dat_cols]
        self.entry_length = [pos[0]] + \
            [p2 - p1 for p1, p2 in zip(pos[:-1], pos[1:])]

    def _make_line(self, col_entries):
        """ add a new line to the database in the correct format"""
        new_line_entries = [('{0: >%d}' % self.entry_length[i]).format(entry)
                            for i, entry in enumerate(col_entries)]
        new_line = "".join(new_line_entries)
        return new_line


def main():
    #   make a test dataframe here of integers, can be anything really
    df = pd.DataFrame(
        pd.np.random.randint(
            0, 100, (1000, 20)), columns=[
            'col_%d' %
            x for x in range(20)])

    root = tk.Tk()
    editor = EditorApp(root, df)
    root.mainloop()  # until closes window

main()