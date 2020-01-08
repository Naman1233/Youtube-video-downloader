from __future__ import print_function, absolute_import
from subprocess import Popen, PIPE, STDOUT, check_output, call
from threading import Thread
import tkinter as tk
import tkinter.ttk as ttk
yvd_path = ''
try:
    y = check_output('youtube-dl --help')
except:
    call('pip install -U youtube-dl --user')
try:
    y = check_output('python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())"')
    print(y)
    yvd_path = "\\".join(y.split('\\')[:-2]) + '\\Scripts'
except:
    pass
print(yvd_path)
frame = None
def download(url):
    global frame
    if frame:
        frame.grid_forget()
        frame.destroy()
    def reader_thread():
        with process.stdout as pipe:
            i = 0
            for line in iter(pipe.readline, ''):
                if i < 3:
                    tk.Label(frame, text = line, width=90, anchor='w', wraplength=700).grid(row=i, column=0, columnspan=2)
                    i += 1
                else:
                    tk.Label(frame, text = line, width=90, anchor='w', wraplength=700).grid(row=i, column=0, columnspan=2)
                    pb = ttk.Progressbar(frame, orient = tk.HORIZONTAL, length = 400, mode = 'determinate')
                    try:
                        pb['value'] = float(line.split()[1][:-1])
                    except:
                        pass
                    pb.update_idletasks()
                    pb.grid(row = 8, column = 0, columnspan = 2, sticky='w')
    frame = tk.Frame(root)
    frame.grid(row = 4, column = 0, columnspan = 2)
    process = Popen('youtube-dl ' + url, stdout=PIPE, stderr=STDOUT, universal_newlines=True)
    t = Thread(target=reader_thread)
    t.daemon = True  # close pipe if GUI process exits
    t.start()


root = tk.Tk()
root.title('Youtube Video Downloader')
root.geometry("650x270")
root.resizable(0, 0)
url = tk.Entry(root, width=70)
tk.Label(root, text = "Enter youtube-link here: ", width=30, anchor='c').grid(row = 0, column = 0, sticky='w')
url.grid(row = 0, column = 1, padx = 5, pady = 5, sticky='w')
tk.Button(root, text="Download", command = lambda: download(url.get())).grid(row = 1, column = 1)

tk.mainloop()