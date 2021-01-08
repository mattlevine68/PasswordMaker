import tkinter as tk
import password_data


conn_string = "host='localhost' dbname='password_holder' user='matt_password' password='PasswordMaker'"

#Uses tkinter to create a GUI to present to class
#Each queryx_widget has either labels, entries or buttons to work with queries
#all of the caller functions are if a query has an entry it gets the result first then calls the query in database.py
class Application(tk.Frame):
    def __init__(self, master=None, query_options = None):
        super().__init__(master)
        self.master = master
        self.query_options = query_options
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.setup_widget()
        self.update_password_widget()
        self.new_password_widget()
        self.see_password_website_widget()
        self.see_password_company_widget()
        self.see_old_password_widget()
        self.quit_widget()


    def setup_widget(self):
        self.setup_button = tk.Button(self)
        self.setup_button['text'] = 'Set Up'
        self.setup_button['command'] = self.query_options.setUp
        self.setup_button.grid(row=0, column=4, pady=2)

    def update_password_caller(self):
        self.query_options.update_password(self.entry_update_password.get())

    def update_password_widget(self):
        self.label_update_password = tk.Label(self, text='Url:')
        self.label_update_password.grid(row=1, column=0, pady=2)

        self.entry_update_password = tk.Entry(self)
        self.entry_update_password.grid(row=1, column=1, pady=2)

        self.update_password_button = tk.Button(self)
        self.update_password_button['text'] = 'Update Password'
        self.update_password_button['command'] = self.update_password_caller
        self.update_password_button.grid(row=1, column=4, pady=2)

    def new_password_caller(self):
        self.query_options.new_password(self.entry_new_password_url.get(), self.entry_new_password_name.get())

    def new_password_widget(self):
        self.label_new_password_url = tk.Label(self, text='Url:')
        self.label_new_password_url.grid(row=2, column=0, pady=2)

        self.entry_new_password_url = tk.Entry(self)
        self.entry_new_password_url.grid(row=2, column=1, pady=2)

        self.label_new_password_name = tk.Label(self, text='Name:')
        self.label_new_password_name.grid(row=2, column=2, pady=2)

        self.entry_new_password_name = tk.Entry(self)
        self.entry_new_password_name.grid(row=2, column=3, pady=2)

        self.new_password_button = tk.Button(self)
        self.new_password_button['text'] = 'Add New Password'
        self.new_password_button['command'] = self.new_password_caller
        self.new_password_button.grid(row=2, column=4, pady=2)

    def see_password_website_caller(self):
        self.query_options.see_password_website(self.entry_password_website_url.get())

    def see_password_website_widget(self):
        self.label_password_website_url = tk.Label(self, text='Url:')
        self.label_password_website_url.grid(row=3, column=0, pady=2)

        self.entry_password_website_url = tk.Entry(self)
        self.entry_password_website_url.grid(row=3, column=1, pady=2)

        self.password_website_button = tk.Button(self)
        self.password_website_button['text'] = 'View Password'
        self.password_website_button['command'] = self.see_password_website_caller
        self.password_website_button.grid(row=3, column=4, pady=2)

    def see_password_company_caller(self):
        self.query_options.see_password_company(self.entry_password_company_name.get())

    def see_password_company_widget(self):
        self.label_password_company_name = tk.Label(self, text='Name:')
        self.label_password_company_name.grid(row=4, column=0, pady=2)

        self.entry_password_company_name = tk.Entry(self)
        self.entry_password_company_name.grid(row=4, column=1, pady=2)

        self.password_company_button = tk.Button(self)
        self.password_company_button['text'] = 'View Password'
        self.password_company_button['command'] = self.see_password_company_caller
        self.password_company_button.grid(row=4, column=4, pady=2)

    def see_old_password_caller(self):
        self.query_options.see_old_password(self.entry_old_password_url.get())

    def see_old_password_widget(self):
        self.label_old_password_url = tk.Label(self, text='Url:')
        self.label_old_password_url.grid(row=5, column=0, pady=2)

        self.entry_old_password_url = tk.Entry(self)
        self.entry_old_password_url.grid(row=5, column=1, pady=2)

        self.old_password_button = tk.Button(self)
        self.old_password_button['text'] = 'View Old Passwords'
        self.old_password_button['command'] = self.see_old_password_caller
        self.old_password_button.grid(row=5, column=4, pady=2)

    def quit_widget(self):
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.grid(row=6, column=4, pady=2)


if __name__ == '__main__':
    query_options = password_data.PasswordData(conn_string)
    root = tk.Tk()
    app = Application(master=root, query_options = query_options)
    app.master.title('Password Databse Queries')
    app.master.maxsize(1000,400)
    app.mainloop()
