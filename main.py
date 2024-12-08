import tkinter as tk

root = tk.Tk()
root.geometry('700x700')
root.title('Перекладач')

def translate(event=None):
    print(prompt_obj.get())

prompt_help_sign = tk.Label(root, text="Уведіть будь-яке українське слово у це поле: ", font=('Arial', 14))
prompt_help_sign.pack()
tk.Label(root, font=("Arial", 1)).pack()

prompt_obj = tk.Entry(root, font=('Arial', 12))
prompt_obj.pack()
prompt_obj.bind("<Return>", translate)
tk.Label(root, font=("Arial", 10)).pack()

prompt_submit = tk.Button(root, font=('Arial', 14), text="Перекласти", command=translate)
prompt_submit.pack()



root.mainloop()