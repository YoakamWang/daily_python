import tkinter as tk
from tkinter import font
from sys import exit
from datetime import datetime

#配色
color_dic = {
    'win_bg':'#5D6D7E',#底板
    'btn_equal':'#F5B041',#等于按钮
    'btn_operator':'#AEB6BF',#运算按钮
    'btn_number':'#EBEDEF',#数字按钮
    'text_fg':'#CB4335',#显示器文字
    'text_bg':'#17202A',#显示器背景
    'author_fg':'#85929E'#作者信息
}

win = tk.Tk()
win.title('Teri的计算器')
win.geometry('320x466')
win.columnconfigure(1,weight=1)
win.resizable(False,False)
win.protocol('WM_DELETE_WINDOW',exit)
win['bg'] = color_dic['win_bg']
font_num = font.Font(family='微软雅黑',size=16)
font_op = font.Font(family='微软雅黑',size=20)
font_scr = font.Font(family='微软雅黑',size=20)
font_txt = font.Font(family='微软雅黑',size=8)
frame = tk.Frame(win)
frame['bg'] = color_dic['win_bg']
txtbox1=tk.Text(win,font=font_scr,height=3)
txtbox1.tag_configure('overstrike',overstrike=True)
txtbox1['bg'] = color_dic['text_bg']
txtbox1['fg'] = color_dic['text_fg']
txtbox1['insertbackground'] = color_dic['text_bg']
lab = tk.Label(win, text='© Teri 2019', font=font_txt)
lab['bg'] = color_dic['win_bg']
lab['fg'] = color_dic['author_fg']
txtbox1.grid(column=0,row=0,columnspan=2,rowspan=1,sticky='nsew',padx=6,pady=6)
frame.grid(column=0, row=3,columnspan=2,padx=6,pady=2)
lab.grid(column=0, row=4,columnspan=5, sticky='s',padx=6)
btn_gp=[]
calculated = False
cn_char = '加减乘除' \
              '零。一二三四五六七八九' \
              '（）'
num_char = '+-×÷' \
               '0.123456789' \
               '()'

def set_button():
    '''第1行'''
    x,y = 0,0
    for txt in ['c','÷','×']:
        btn_gp.append(tk.Button(frame, text=txt, font=font_num))
        btn_gp[-1].grid(column=x, row=y, sticky='nsew')
        btn_gp[-1].bind('<Button-1>', widget_callback)
        btn_gp[-1]['bg'] = color_dic['btn_operator']
        x += 1

    '''第4列'''
    x,y = 3,0
    for txt in ['-','+','=']:
        btn_gp.append(tk.Button(frame, text=txt, font=font_op))
        btn_gp[-1].grid(column=x, row=y*2,  rowspan= 1 if txt=='-' else 2, sticky='nsew', ipadx=18)
        btn_gp[-1].bind('<Button-1>', widget_callback)
        btn_gp[-1]['bg'] = color_dic['btn_equal'] if txt=='=' else color_dic['btn_operator']
        y += 1

    '''9宫格'''
    x,y = 0,2
    for i in range(9):
        if x == 3:
            x = 0
            y += 1
        id = 9-i
        btn_gp.append(tk.Button(frame, text=str(id),font=font_num))
        btn_gp[-1].grid(column=2-x,row=y,sticky='nsew',ipadx=22,ipady=8)
        btn_gp[-1].bind('<Button-1>',widget_callback)
        btn_gp[-1]['bg'] = color_dic['btn_number']
        x += 1

    '''第6行'''
    x,y = 0,5
    for txt in ['0','.']:
        btn_gp.append(tk.Button(frame, text=txt, font=font_num))
        btn_gp[-1].grid(column=x*2, row=y, columnspan= 2 if txt=='0' else 1, sticky='nsew',ipadx=22,ipady=8)
        btn_gp[-1].bind('<Button-1>', widget_callback)
        btn_gp[-1]['bg'] = color_dic['btn_number']
        x += 1

def break_Return(event): #替换按键的默认值
    input_txt('=')
    return 'break'
def break_KeyPress(event): #替换按键的默认值
    txt=event.char
    if txt:
        if txt in '/*':
            txt = txt.replace('/', '÷').replace('*', '×')
        input_txt(txt)
    return 'break'
def break_BackSpace(event):
    pass
def widget_callback(event):
    input_txt(event.widget['text'])
def input_txt(txt):
    global calculated
    get_txt = txtbox1.get(0.0, 'end')
    if txt == '=':
        if not get_txt == '\n':
            result = calculation(get_txt)
            edit_Text('c')
            edit_Text('input', result)
            calculated = True
    elif txt == 'c':
        edit_Text('c')
        calculated = False
    elif txt in '0.123456789':
        if calculated:
            if Result_C(txtbox1.get(0.0, 'end')):
                edit_Text('c')
                calculated = False
        edit_Text('input', txt)
    elif txt in '+-×÷':
        txt = ' ' + txt + ' '
        edit_Text('input', txt)
    elif txt in cn_char+'()':
        edit_Text('input', txt)
def edit_Text(type,txt=''):
    if type == 'input':
        txtbox1.insert('end', txt)
        txtbox1.see('end')
    elif type == 'c':
        txtbox1.delete(0.0, 'end')
def calculation(get_txt):
    for i in range(len(cn_char)):
        get_txt = get_txt.replace(cn_char[i], num_char[i])
    txt_list = get_txt.split('=')
    t = txt_list[-1].strip().strip('\n')
    x = False
    for i in '+-×÷':
        if i in t:
            x = True
            break
    if x:
        try:
            if t.find('=') == -1:
                t1 = t.replace('×', '*').replace('÷', '/')
                t1 = t1.replace('*  *','**')
                t = t.replace('×  ×','次方')
                result = eval(t1)
                t += '\n= {}'.format(round(result, 4))
                #写入历史记录
                #write_txt(t)
        except:
            pass
    return t
def write_txt(txt):
    log = datetime.now().strftime('#%Y/%m/%d-%H:%M:%S')+'\n'
    log += txt + '\n\n'
    with open('cal-History.txt', 'a') as file:
        file.writelines(log)
        file.close()
def Result_C(get_txt):
    endline = get_txt.split('\n')[-2].strip().strip('\n')
    if endline:
        for i in '+-×÷':
            if i in endline:
                return False
        return True
    return False

set_button()
txtbox1.bind('<KeyPress>',break_KeyPress)
txtbox1.bind('<Return>',break_Return)
txtbox1.bind('<BackSpace>',break_BackSpace)
txtbox1.focus_set()

win.mainloop()


# """
# Code illustration: 2.07
#
# Adding features:
#     File > New
#     File > Open
#     File > Save
#     File > Save As
#
#
# @Tkinter GUI Application Development Blueprints
# """
# import os
# from tkinter import Tk, PhotoImage, Menu, Frame, Text, Scrollbar, IntVar, \
#     StringVar, END
#
# import tkinter.filedialog
#
#
# PROGRAM_NAME = "Footprint Editor"
# file_name = None
#
# root = Tk()
# root.geometry('350x350')
# root.title(PROGRAM_NAME)
#
# # new_file, open_file, save, save_as implementation
#
#
# def new_file(event=None):
#     root.title("Untitled")
#     global file_name
#     file_name = None
#     content_text.delete(1.0, END)
#
#
# def open_file(event=None):
#     input_file_name = tkinter.filedialog.askopenfilename(defaultextension=".txt",
#                                                          filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
#     if input_file_name:
#         global file_name
#         file_name = input_file_name
#         root.title('{} - {}'.format(os.path.basename(file_name), PROGRAM_NAME))
#         content_text.delete(1.0, END)
#         with open(file_name) as _file:
#             content_text.insert(1.0, _file.read())
#
#
# def write_to_file(file_name):
#     try:
#         content = content_text.get(1.0, 'end')
#         with open(file_name, 'w') as the_file:
#             the_file.write(content)
#     except IOError:
#         pass  # in actual we will show a error message box.
#         # we discuss message boxes in the next section so ignored here.
#
#
# def save_as(event=None):
#     input_file_name = tkinter.filedialog.asksaveasfilename(defaultextension=".txt",
#                                                            filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
#     if input_file_name:
#         global file_name
#         file_name = input_file_name
#         write_to_file(file_name)
#         root.title('{} - {}'.format(os.path.basename(file_name), PROGRAM_NAME))
#     return "break"
#
#
# def save(event=None):
#     global file_name
#     if not file_name:
#         save_as()
#     else:
#         write_to_file(file_name)
#     return "break"
#
# # End of iteration
#
#
# def select_all(event=None):
#     content_text.tag_add('sel', '1.0', 'end')
#     return "break"
#
#
# def find_text(event=None):
#     search_toplevel = Toplevel(root)
#     search_toplevel.title('Find Text')
#     search_toplevel.transient(root)
#     search_toplevel.resizable(False, False)
#     Label(search_toplevel, text="Find All:").grid(row=0, column=0, sticky='e')
#     search_entry_widget = Entry(
#         search_toplevel, width=25)
#     search_entry_widget.grid(row=0, column=1, padx=2, pady=2, sticky='we')
#     search_entry_widget.focus_set()
#     ignore_case_value = IntVar()
#     Checkbutton(search_toplevel, text='Ignore Case', variable=ignore_case_value).grid(
#         row=1, column=1, sticky='e', padx=2, pady=2)
#     Button(search_toplevel, text="Find All", underline=0,
#            command=lambda: search_output(
#                search_entry_widget.get(), ignore_case_value.get(),
#                content_text, search_toplevel, search_entry_widget)
#            ).grid(row=0, column=2, sticky='e' + 'w', padx=2, pady=2)
#
#     def close_search_window():
#         content_text.tag_remove('match', '1.0', END)
#         search_toplevel.destroy()
#     search_toplevel.protocol('WM_DELETE_WINDOW', close_search_window)
#     return "break"
#
#
# def search_output(needle, if_ignore_case, content_text,
#                   search_toplevel, search_box):
#     content_text.tag_remove('match', '1.0', END)
#     matches_found = 0
#     if needle:
#         start_pos = '1.0'
#         while True:
#             start_pos = content_text.search(needle, start_pos,
#                                             nocase=if_ignore_case, stopindex=END)
#             if not start_pos:
#                 break
#             end_pos = '{}+{}c'.format(start_pos, len(needle))
#             content_text.tag_add('match', start_pos, end_pos)
#             matches_found += 1
#             start_pos = end_pos
#         content_text.tag_config(
#             'match', foreground='red', background='yellow')
#     search_box.focus_set()
#     search_toplevel.title('{} matches found'.format(matches_found))
#
#
# def cut():
#     content_text.event_generate("<<Cut>>")
#     return "break"
#
#
# def copy():
#     content_text.event_generate("<<Copy>>")
#     return "break"
#
#
# def paste():
#     content_text.event_generate("<<Paste>>")
#     return "break"
#
#
# def undo():
#     content_text.event_generate("<<Undo>>")
#     return "break"
#
#
# def redo(event=None):
#     content_text.event_generate("<<Redo>>")
#     return 'break'
#
# new_file_icon = PhotoImage(file='icons/new_file.gif')
# open_file_icon = PhotoImage(file='icons/open_file.gif')
# save_file_icon = PhotoImage(file='icons/save.gif')
# cut_icon = PhotoImage(file='icons/cut.gif')
# copy_icon = PhotoImage(file='icons/copy.gif')
# paste_icon = PhotoImage(file='icons/paste.gif')
# undo_icon = PhotoImage(file='icons/undo.gif')
# redo_icon = PhotoImage(file='icons/redo.gif')
#
# menu_bar = Menu(root)
# file_menu = Menu(menu_bar, tearoff=0)
# file_menu.add_command(label='New', accelerator='Ctrl+N', compound='left',
#                       image=new_file_icon, underline=0, command=new_file)
# file_menu.add_command(label='Open', accelerator='Ctrl+O', compound='left',
#                       image=open_file_icon, underline=0, command=open_file)
# file_menu.add_command(label='Save', accelerator='Ctrl+S',
#                       compound='left', image=save_file_icon, underline=0, command=save)
# file_menu.add_command(
#     label='Save as', accelerator='Shift+Ctrl+S', command=save_as)
# file_menu.add_separator()
# file_menu.add_command(label='Exit', accelerator='Alt+F4')
# menu_bar.add_cascade(label='File', menu=file_menu)
#
# edit_menu = Menu(menu_bar, tearoff=0)
# edit_menu.add_command(label='Undo', accelerator='Ctrl+Z',
#                       compound='left', image=undo_icon, command=undo)
# edit_menu.add_command(label='Redo', accelerator='Ctrl+Y',
#                       compound='left', image=redo_icon, command=redo)
# edit_menu.add_separator()
# edit_menu.add_command(label='Cut', accelerator='Ctrl+X',
#                       compound='left', image=cut_icon, command=cut)
# edit_menu.add_command(label='Copy', accelerator='Ctrl+C',
#                       compound='left', image=copy_icon, command=copy)
# edit_menu.add_command(label='Paste', accelerator='Ctrl+V',
#                       compound='left', image=paste_icon, command=paste)
# edit_menu.add_separator()
# edit_menu.add_command(label='Find', underline=0,
#                       accelerator='Ctrl+F', command=find_text)
# edit_menu.add_separator()
# edit_menu.add_command(label='Select All', underline=7,
#                       accelerator='Ctrl+A', command=select_all)
# menu_bar.add_cascade(label='Edit', menu=edit_menu)
#
#
# view_menu = Menu(menu_bar, tearoff=0)
# show_line_number = IntVar()
# show_line_number.set(1)
# view_menu.add_checkbutton(label='Show Line Number', variable=show_line_number)
# show_cursor_info = IntVar()
# show_cursor_info.set(1)
# view_menu.add_checkbutton(
#     label='Show Cursor Location at Bottom', variable=show_cursor_info)
# highlight_line = IntVar()
# view_menu.add_checkbutton(label='Highlight Current Line', onvalue=1,
#                           offvalue=0, variable=highlight_line)
# themes_menu = Menu(menu_bar, tearoff=0)
# view_menu.add_cascade(label='Themes', menu=themes_menu)
#
# color_schemes = {
#     'Default': '#000000.#FFFFFF',
#     'Greygarious': '#83406A.#D1D4D1',
#     'Aquamarine': '#5B8340.#D1E7E0',
#     'Bold Beige': '#4B4620.#FFF0E1',
#     'Cobalt Blue': '#ffffBB.#3333aa',
#     'Olive Green': '#D1E7E0.#5B8340',
#     'Night Mode': '#FFFFFF.#000000',
# }
#
# theme_choice = StringVar()
# theme_choice.set('Default')
# for k in sorted(color_schemes):
#     themes_menu.add_radiobutton(label=k, variable=theme_choice)
# menu_bar.add_cascade(label='View', menu=view_menu)
#
# about_menu = Menu(menu_bar, tearoff=0)
# about_menu.add_command(label='About')
# about_menu.add_command(label='Help')
# menu_bar.add_cascade(label='About',  menu=about_menu)
# root.config(menu=menu_bar)
#
# shortcut_bar = Frame(root,  height=25, background='light sea green')
# shortcut_bar.pack(expand='no', fill='x')
# line_number_bar = Text(root, width=4, padx=3, takefocus=0,  border=0,
#                        background='khaki', state='disabled',  wrap='none')
# line_number_bar.pack(side='left',  fill='y')
#
# content_text = Text(root, wrap='word', undo=1)
# content_text.pack(expand='yes', fill='both')
# scroll_bar = Scrollbar(content_text)
# content_text.configure(yscrollcommand=scroll_bar.set)
# scroll_bar.config(command=content_text.yview)
# scroll_bar.pack(side='right', fill='y')
#
# # Shortcut key bindings for this iteration
# content_text.bind('<Control-N>', new_file)
# content_text.bind('<Control-n>', new_file)
# content_text.bind('<Control-O>', open_file)
# content_text.bind('<Control-o>', open_file)
# content_text.bind('<Control-S>', save)
# content_text.bind('<Control-s>', save)
# # Iteration ends
#
# content_text.bind('<Control-f>', find_text)
# content_text.bind('<Control-F>', find_text)
# content_text.bind('<Control-A>', select_all)
# content_text.bind('<Control-a>', select_all)
# content_text.bind('<Control-y>', redo)
# content_text.bind('<Control-Y>', redo)
#
#
# root.mainloop()

# import tkinter as tk
#
# class App(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         group_1 = tk.LabelFrame(self, padx=15, pady=10,
#                                 text="Personal Information")
#         group_1.pack(padx=10, pady=5)
#
#         tk.Label(group_1, text="First name").grid(row=0)
#         tk.Label(group_1, text="Last name").grid(row=1)
#         tk.Entry(group_1).grid(row=0, column=1, sticky=tk.W)
#         tk.Entry(group_1).grid(row=1, column=1, sticky=tk.W)
#
#         group_2 = tk.LabelFrame(self, padx=15, pady=10,
#                                 text="Address")
#         group_2.pack(padx=10, pady=5)
#
#         tk.Label(group_2, text="Street").grid(row=0)
#         tk.Label(group_2, text="City").grid(row=1)
#         tk.Label(group_2, text="ZIP Code").grid(row=2)
#         tk.Entry(group_2).grid(row=0, column=1, sticky=tk.W)
#         tk.Entry(group_2).grid(row=1, column=1, sticky=tk.W)
#         tk.Entry(group_2, width=8).grid(row=2, column=1,
#                                         sticky=tk.W)
#
#         self.btn_submit = tk.Button(self, text="Submit")
#         self.btn_submit.pack(padx=10, pady=10, side=tk.RIGHT)
#
# if __name__ == "__main__":
#     app = App()
#     app.mainloop()


# import tkinter as tk
#
# class App(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         label_a = tk.Label(self, text="Label A", bg="yellow")
#         label_b = tk.Label(self, text="Label B", bg="orange")
#         label_c = tk.Label(self, text="Label C", bg="red")
#         label_d = tk.Label(self, text="Label D", bg="green")
#         label_e = tk.Label(self, text="Label E", bg="blue")
#
#         opts = { 'ipadx': 10, 'ipady': 10, 'fill': tk.BOTH }
#         label_a.pack(side=tk.TOP, **opts)
#         label_b.pack(side=tk.TOP, **opts)
#         label_c.pack(side=tk.LEFT, **opts)
#         label_d.pack(side=tk.LEFT, **opts)
#         label_e.pack(side=tk.LEFT, **opts)
#
# if __name__ == "__main__":
#     app = App()
#     app.mainloop()

# import tkinter as tk
#
# class ListFrame(tk.Frame):
#     def __init__(self, master, items=[]):
#         super().__init__(master)
#         self.list = tk.Listbox(self)
#         self.scroll = tk.Scrollbar(self, orient=tk.VERTICAL,
#                                    command=self.list.yview)
#         self.list.config(yscrollcommand=self.scroll.set)
#         self.list.insert(0, *items)
#         self.list.pack(side=tk.LEFT)
#         self.scroll.pack(side=tk.LEFT, fill=tk.Y)
#
#     def pop_selection(self):
#         index = self.list.curselection()
#         if index:
#             value = self.list.get(index)
#             self.list.delete(index)
#             return value
#
#     def insert_item(self, item):
#         self.list.insert(tk.END, item)
#
# class App(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         months = ["January", "February", "March", "April",
#                   "May", "June", "July", "August", "September",
#                   "October", "November", "December"]
#         self.frame_a = ListFrame(self, months)
#         self.frame_b = ListFrame(self)
#         self.btn_right = tk.Button(self, text=">",
#                                    command=self.move_right)
#         self.btn_left = tk.Button(self, text="<",
#                                   command=self.move_left)
#
#         self.frame_a.pack(side=tk.LEFT, padx=10, pady=10)
#         self.frame_b.pack(side=tk.RIGHT, padx=10, pady=10)
#         self.btn_right.pack(expand=True, ipadx=5)
#         self.btn_left.pack(expand=True, ipadx=5)
#
#     def move_right(self):
#         self.move(self.frame_a, self.frame_b)
#
#     def move_left(self):
#         self.move(self.frame_b, self.frame_a)
#
#     def move(self, frame_from, frame_to):
#         value = frame_from.pop_selection()
#         if value:
#             frame_to.insert_item(value)
#
# if __name__ == "__main__":
#     app = App()
#     app.mainloop()

# import tkinter as tk
# from tkinter.filedialog import askopenfilename, asksaveasfilename
#
#
# def open_file():
#     """Open a file for editing."""
#     filepath = askopenfilename(
#         filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
#     )
#     if not filepath:
#         return
#     txt_edit.delete("1.0", tk.END)
#     with open(filepath, mode="rb") as input_file:
#
#         text = input_file.read().decode("utf-8")
#         # except Exception:
#         #     text=input_file.read()
#         txt_edit.insert(tk.END, text)
#     window.title(f"Simple Text Editor - {filepath}")
#
#
# def save_file():
#     """Save the current file as a new file."""
#     filepath = asksaveasfilename(
#         defaultextension=".txt",
#         filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
#     )
#     if not filepath:
#         return
#     with open(filepath, mode="wb", encoding="utf-8") as output_file:
#         text = txt_edit.get("1.0", tk.END)
#         output_file.write(text)
#     window.title(f"Simple Text Editor - {filepath}")
#
#
# window = tk.Tk()
# window.title("Simple Text Editor")
#
# window.rowconfigure(0, minsize=800, weight=1)
# window.columnconfigure(1, minsize=800, weight=1)
#
# txt_edit = tk.Text(window)
# frm_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
# btn_open = tk.Button(frm_buttons, text="Open", command=open_file)
# btn_save = tk.Button(frm_buttons, text="Save As...", command=save_file)
#
# btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
# btn_save.grid(row=1, column=0, sticky="ew", padx=5)
#
# frm_buttons.grid(row=0, column=0, sticky="ns")
# txt_edit.grid(row=0, column=1, sticky="nsew")
#
# window.mainloop()

# import tkinter as tk
#
#
# def decrease():
#     value = int(lbl_value["text"])
#     lbl_value["text"] = f"{value - 1}"
#
#
# def increase():
#     value = int(lbl_value["text"])
#     lbl_value["text"] = f"{value + 1}"
#
#
# root = tk.Tk()
# message = tk.Label(root, text="Hello TKinter!")
# root.title("test tk")
# # root.geometry('600x400+50+50')
# btn_decrease = tk.Button(master=root, text="-", command=decrease)
# btn_decrease.grid(row=0, column=0, sticky="nsew")
#
# lbl_value = tk.Label(master=root, text="0")
# lbl_value.grid(row=0, column=1)
#
# btn_increase = tk.Button(master=root, text="+", command=increase)
# btn_increase.grid(row=0, column=2, sticky="nsew")
#
# # message.pack()
#
# root.mainloop()
