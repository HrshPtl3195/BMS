import tkinter as tk
from tkinter import ttk, messagebox, StringVar, IntVar, Tk, Toplevel
from PIL import Image, ImageTk, ImageFilter
import mysql.connector
from mysql.connector import Error
from tkcalendar import DateEntry
from datetime import datetime
import re, csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import timedelta
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, letter

def connect_to_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="mybms"
        )
    except Error as e:
        messagebox.showerror("Database Connection Error", f"An error occurred: {str(e)}")
        return None

current_user = None
customer = None

def set_current_user(username):
    global current_user
    current_user = username
    
def set_customer(username):
    global customer
    customer = username
    
def get_current_user():
    return current_user

def get_customer():
    return customer




#=================================================================================================================================================
#                                                                   MAIN WINDOW                                                                  #
#=================================================================================================================================================
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("BANK MANAGEMENT SYSTEM")
        self.root.iconbitmap('/MYBM/bank.ico')
        self.root.resizable(0,0)
        self.root.state("zoomed")
        
        self.container = ttk.Frame(self.root)
        self.container.pack(expand=True, fill="both")
        
        self.frames = {}
        
        self.show_frame(LoginPage)

    def show_frame(self, page_class):
        frame = self.frames.get(page_class)
        if not frame:
            frame = page_class(parent=self.container, controller=self)
            self.frames[page_class] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise() 
    



#=================================================================================================================================================
#                                                                   SYSTEM LOGIN                                                                 #
#=================================================================================================================================================
class LoginPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.setup_background()
        self.create_shadow_frame()
        self.create_login_form()
        self.username_entry.focus_set()
        
    def setup_background(self):
        background_image = Image.open("/MYBM/rupee.jpg")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        background_image = background_image.resize((screen_width, screen_height), Image.LANCZOS)
        background_image = background_image.filter(ImageFilter.GaussianBlur(0))
        background_photo = ImageTk.PhotoImage(background_image)
        
        canvas = tk.Canvas(self, width=screen_width, height=screen_height)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=background_photo, anchor="nw")
        self.background_photo = background_photo

    def create_shadow_frame(self):
        style = ttk.Style()
        style.configure('Shadow.TFrame', background='#499A51')
        shadow_frame = ttk.Frame(self, style="Shadow.TFrame")
        shadow_frame.place(relx=0.5, rely=0.5, anchor="center", width=500, height=580)
    
    def create_login_form(self):
        login_frame = ttk.Frame(self, padding=(60, 30, 60, 10))
        login_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.head_image = Image.open("/MYBM/circle.png")
        self.head_image = self.head_image.resize((70, 70), Image.LANCZOS)
        self.head_photo = ImageTk.PhotoImage(self.head_image)

        self.body_image = Image.open("/MYBM/body.png")
        self.body_image = self.body_image.resize((150, 70), Image.LANCZOS)
        self.body_photo = ImageTk.PhotoImage(self.body_image)

        image_label1 = ttk.Label(login_frame, image=self.head_photo)
        image_label1.pack(pady=(0, 10))

        image_label2 = ttk.Label(login_frame, image=self.body_photo)
        image_label2.pack(pady=(0, 10)) 

        login_label = ttk.Label(login_frame, text="LOGIN PAGE", font=("Times New Roman", 20, "bold"), foreground="#499A51")
        login_label.pack(pady=(0, 20))

        username_label = ttk.Label(login_frame, text="Username:", font=("Times New Roman", 14), foreground="#499A51")
        username_label.pack(anchor="w", pady=5)
        self.username_entry = ttk.Entry(login_frame, font=("Times New Roman", 18, 'bold'), width=30, foreground="#499A51")
        self.username_entry.pack(fill="x", pady=5)

        password_label = ttk.Label(login_frame, text="Password:", font=("Times New Roman", 14), foreground="#499A51")
        password_label.pack(anchor="w", pady=5)
        self.password_entry = ttk.Entry(login_frame, font=("Times New Roman", 18, 'bold'), show="*", width=30, foreground="#499A51")
        self.password_entry.pack(fill="x", pady=5)

        user_type_label = ttk.Label(login_frame, text="User Type:", font=("Times New Roman", 14), foreground="#499A51")
        user_type_label.pack(anchor="w", pady=5)

        radio_frame = ttk.Frame(login_frame)
        radio_frame.pack(pady=5)

        style = ttk.Style()
        style.configure('TRadiobutton', font=('Times New Roman', 14), foreground="#499A51")

        self.user_type_var = tk.StringVar(value="Admin")

        admin_rb = ttk.Radiobutton(radio_frame, text="Admin", variable=self.user_type_var, value="Admin", style='TRadiobutton')
        admin_rb.pack(side="left", padx=10)

        staff_rb = ttk.Radiobutton(radio_frame, text="Staff", variable=self.user_type_var, value="Staff", style='TRadiobutton')
        staff_rb.pack(side="left", padx=10)

        customer_rb = ttk.Radiobutton(radio_frame, text="Customer", variable=self.user_type_var, value="Customer", style='TRadiobutton')
        customer_rb.pack(side="left", padx=10)
        
        style.configure('TButton', font=('Times New Roman', 18, 'bold'), foreground="#499A51")
        sign_in_button = ttk.Button(login_frame, text="Login", style='TButton', command=self.login)
        sign_in_button.pack(pady=20)
        
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_type = self.user_type_var.get()
            
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT username, password, user_type FROM users WHERE username=\'{}\' AND user_type=\'{}\'".format(username, user_type))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if username and password:
            if result and result[1] == password:
                set_current_user(username)
                if result[2].lower() == "admin":
                    messagebox.showinfo("Login Successfull","Logged in as ADMIN")
                    self.controller.show_frame(AdminPage)
                    print(f"{username} Logged In")
                elif result[2].lower() == "staff":
                    messagebox.showinfo("Login Successfull","Logged in as STAFF MEMBER")
                    self.controller.show_frame(StaffPage)
                    print(f"{username} Logged In")
                elif result[2].lower() == "customer":
                    messagebox.showinfo("Login Successfull","Logged in as CUSTOMER")
                    set_customer(current_user)
                    self.controller.show_frame(UserPage)
                    print(f"{username} Logged In")
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")
        else:
            messagebox.showerror("Login Failed", "Please fill in all details.")
    
    def reset_fields(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.user_type_var.set("Admin")
        self.username_entry.focus_set()
    
    
    
    
#=================================================================================================================================================
#                                                                    ADMIN PAGE                                                                  #
#=================================================================================================================================================            
class AdminPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.setup_ui()

    def setup_ui(self):
        title_panel = ttk.Frame(self, style='TitlePanel.TFrame', padding=(0,20,0,20))
        title_panel.pack(side='top', fill='x')
        
        button_panel = ttk.Frame(self, style='ButtonPanel.TFrame', padding=(20,12,20,10))
        button_panel.pack(side='left', fill='y')
        
        title_label = ttk.Label(title_panel, text="ADMIN DASHBOARD", background="#499A51",font=("Times New Roman", 32, 'bold'), foreground="#ffffff")
        title_label.pack(pady=10)
        
        user_management_button = ttk.Button(button_panel, text="User Management", command=self.go_to_user_management, style="Custom.TButton")
        user_management_button.pack(pady=10, fill="x")
        
        transaction_history_button = ttk.Button(button_panel, text="View Transaction History", command=self.go_to_transaction_history, style="Custom.TButton")
        transaction_history_button.pack(pady=10, fill="x")
        
        report_generation_button = ttk.Button(button_panel, text="Generate Reports", command=self.go_to_report_generation, style="Custom.TButton")
        report_generation_button.pack(pady=10, fill="x")
        
        interest_fee_management_button = ttk.Button(button_panel, text="Interest & Fee Management", command=self.go_to_interest_fee_management, style="Custom.TButton")
        interest_fee_management_button.pack(pady=10, fill="x")
        
        logout_button = ttk.Button(button_panel, text="Logout", command=self.logout, style="Custom.TButton")
        logout_button.pack(pady=10, fill="x")
        
        style = ttk.Style()
        style.configure('Custom.TButton',
                font=("Times New Roman", 18, 'bold'),
                foreground='#499A51',
                background='#499A51',
                padding=10)
        style.configure('TitlePanel.TFrame', background='#499A51')
        style.configure('ButtonPanel.TFrame', background='#499A51')
        
        self.content_area = ttk.Frame(self)
        self.content_area.pack(side='right', fill='both', expand=True, padx=10, pady=10)
        
        self.show_content(UserManagementPage)

    def show_content(self, page_class):
        content_frame = self.content_area.children.get(page_class.__name__)
        if not content_frame:
            content_frame = page_class(parent=self.content_area, controller=self.controller)
            self.content_area.children[page_class.__name__] = content_frame
        content_frame.grid(row=0, column=0, sticky="nsew")
        content_frame.tkraise()

    def go_to_user_management(self):
        self.show_content(UserManagementPage)

    def go_to_transaction_history(self):
        self.show_content(TransactionHistoryPage)

    def go_to_report_generation(self):
        self.show_content(ReportGenerationPage)

    def go_to_interest_fee_management(self):
        self.show_content(InterestFeeManagementPage)

    def logout(self):
        login_page = self.controller.frames[LoginPage]
        login_page.reset_fields()
        self.controller.show_frame(LoginPage)
        print(f"{current_user} Logged Out")

#====================================
#        USER MANAGEMENT PAGE       #
#====================================
class UserManagementPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()
        self.load_users()

    def setup_ui(self):
        style = ttk.Style()

        style.configure("Custom.Treeview", font=("Times New Roman", 14), foreground='#499A51', padding=15)
        style.configure("Custom.Treeview.Heading", font=("Times New Roman", 18, 'bold'), foreground='#499A51', padding=10)

        # Title
        ttk.Label(self, text="User Management", style='TLabel', font=("Times New Roman", 24, 'bold'), foreground='#499A51').pack(pady=20, anchor="center")
        
        button_frame = ttk.Frame(self)
        button_frame.pack(fill='x', padx=500, pady=10, anchor="center")

        self.add_button = ttk.Button(button_frame, text="Add Staff", command=self.add_user)
        self.add_button.pack(side='left', padx=5)

        self.edit_button = ttk.Button(button_frame, text="Edit User", command=self.edit_user)
        self.edit_button.pack(side='left', padx=5)

        self.delete_button = ttk.Button(button_frame, text="Delete User", command=self.delete_user)
        self.delete_button.pack(side='left', padx=5)
        
        self.table_frame = ttk.Frame(self, borderwidth=2, relief="solid")
        self.table_frame.pack(fill='both', expand=False, padx=450, pady=10)

        self.tree_um = ttk.Treeview(self.table_frame, columns=("username", "user_type"), style="Custom.Treeview", show='headings')
        self.tree_um.heading("username", text="Username", anchor='center')
        self.tree_um.heading("user_type", text="User Type", anchor='center')
        self.tree_um.pack(fill='both', expand=True)
        self.tree_um.tag_configure("heading", foreground='#499A51')

    def load_users(self):
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT username, user_type FROM users")
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            for row in self.tree_um.get_children():
                self.tree_um.delete(row)

            for row in rows:
                self.tree_um.insert("", tk.END, values=row)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))

    def add_user(self):
        AddUserDialog(self)

    def edit_user(self):
        selected_item = self.tree_um.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a user to edit.")
            return

        username = self.tree_um.item(selected_item[0])['values'][0]
        EditUserDialog(self, username)

    def delete_user(self):
        selected_item = self.tree_um.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a user to delete.")
            return

        username = self.tree_um.item(selected_item[0])['values'][0]
        response = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete user '{username}'?")
        if response:
            try:
                conn = connect_to_db()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM users WHERE username=\'{}\'".format(username,))
                conn.commit()
                cursor.close()
                conn.close()
                self.load_users()
                messagebox.showinfo("Success", "User deleted successfully.")
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", str(err))

class AddUserDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Add Staff")
        self.geometry("300x220")
        self.iconbitmap('/MYBM/bank.ico')
        self.resizable(0,0)
        self.grab_set()
        
        self.update_idletasks()
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_right = int((screen_width / 2) - (window_width / 2))
        position_down = int((screen_height / 2) - (window_height / 2))
        self.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

        self.create_widgets()
        
    def create_widgets(self):
        style = ttk.Style()
        style.configure('TLabel', font=("Times New Roman", 14), foreground="#499A51")
        style.configure('TEntry', font=("Times New Roman", 18, 'bold'), foreground="#499A51")
        style.configure('TRadiobutton', font=('Times New Roman', 14), foreground="#499A51")
        style.configure('TButton', font=('Times New Roman', 18, 'bold'), foreground="#499A51")

        ttk.Label(self, text="Username:", font=("Times New Roman", 14), foreground="#499A51").pack(anchor="w", padx=25, pady=5)
        self.username_entry = ttk.Entry(self, font=("Times New Roman", 18, 'bold'), width=20, foreground="#499A51")
        self.username_entry.pack(pady=5)

        ttk.Label(self, text="Password:", font=("Times New Roman", 14), foreground="#499A51").pack(anchor="w", padx=25, pady=5)
        self.password_entry = ttk.Entry(self, font=("Times New Roman", 18, 'bold'), show="*", width=20, foreground="#499A51")
        self.password_entry.pack(pady=5)

        ttk.Button(self, text="Add Staff", command=self.add_user).pack(pady=10)

    def add_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Input Error", "Please fill in all fields.")
            return
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password, user_type) VALUES (\'{}\', \'{}\', \'Staff\')".format(username, password))
            conn.commit()
            cursor.close()
            conn.close()
            self.parent.load_users()
            self.destroy()
            messagebox.showinfo("Success", "Staff member added successfully.")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))

class EditUserDialog(tk.Toplevel):
    def __init__(self, parent, username):
        super().__init__(parent)
        self.parent = parent
        self.username = username
        self.title("Edit User")
        self.geometry("300x300")
        self.iconbitmap('/MYBM/bank.ico')
        self.resizable(0,0)
        self.grab_set()
        
        self.update_idletasks()
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_right = int((screen_width / 2) - (window_width / 2))
        position_down = int((screen_height / 2) - (window_height / 2))
        self.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

        
        self.create_widgets()
        self.load_user()

    def create_widgets(self):
        style = ttk.Style()
        style.configure('TLabel', font=("Times New Roman", 14), foreground="#499A51")
        style.configure('TEntry', font=("Times New Roman", 18, 'bold'), foreground="#499A51")
        style.configure('TRadiobutton', font=('Times New Roman', 14), foreground="#499A51")
        style.configure('TButton', font=('Times New Roman', 18, 'bold'), foreground="#499A51")

        ttk.Label(self, text="Username:", font=("Times New Roman", 14), foreground="#499A51").pack(anchor="w", padx=25, pady=5)
        self.username_entry = ttk.Entry(self, font=("Times New Roman", 18, 'bold'), width=20, foreground="#499A51")
        self.username_entry.pack(pady=5)

        ttk.Label(self, text="New Password:", font=("Times New Roman", 14), foreground="#499A51").pack(anchor="w", padx=25, pady=5)
        self.password_entry = ttk.Entry(self, font=("Times New Roman", 18, 'bold'), show="*", width=20, foreground="#499A51")
        self.password_entry.pack(pady=5)

        ttk.Label(self, text="User Type:", font=("Times New Roman", 14), foreground="#499A51").pack(anchor="w", padx=25, pady=5)

        radio_frame = ttk.Frame(self)
        radio_frame.pack(pady=5)
        self.user_type_var = tk.StringVar(value="Staff")
        ttk.Radiobutton(radio_frame, text="Staff", variable=self.user_type_var, value="Staff").pack(side="left", padx=5)
        ttk.Radiobutton(radio_frame, text="Customer", variable=self.user_type_var, value="Customer").pack(side="left", padx=5)

        ttk.Button(self, text="Save Changes", command=self.save_changes).pack(pady=10)
        
    def load_user(self):
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT password, user_type FROM users WHERE username=\'{}\'".format(self.username))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                self.username_entry.config(state='normal')
                self.username_entry.insert(0, self.username)
                self.username_entry.config(state='readonly')
                self.password_entry.insert(0, user[0])
                self.user_type_var.set(user[1])
            else:
                messagebox.showerror("Error", "User not found.")
                self.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))

    def save_changes(self):
        password = self.password_entry.get()
        user_type = self.user_type_var.get()

        if not password:
            messagebox.showerror("Input Error", "Please enter a new password.")
            return
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET password=\'{}\', user_type=\'{}\' WHERE username=\'{}\'".format(password, user_type, self.username))
            conn.commit()
            cursor.close()
            conn.close()
            self.parent.load_users()
            self.destroy()
            messagebox.showinfo("Success", "User updated successfully.")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))

#========================================
#        TRANSACTION HISTORY PAGE       #
#========================================
class TransactionHistoryPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        styleth = ttk.Style()
        styleth.configure('TLabel', font=("Times New Roman", 14), foreground="#499A51")
        styleth.configure('TEntry', font=("Times New Roman", 18, 'bold'), foreground="#499A51")
        styleth.configure("Custom.Treeview", font=("Times New Roman", 14), foreground='#499A51', padding=5)
        styleth.configure("Custom.Treeview.Heading", font=("Times New Roman", 16, 'bold'), foreground='#499A51', padding=10)
        styleth.configure("TCombobox", font=("Times New Roman", 18, 'bold'), foreground="#499A51")
        styleth.map('TCombobox', fieldbackground=[('readonly', '#ffffff')], foreground=[('readonly', '#499A51')])
       
        # Title
        ttk.Label(self, text="Transaction History", style='TLabel', font=("Times New Roman", 24, 'bold')).pack(pady=20)
        # Filters Frame
        filters_frame = ttk.Frame(self)
        filters_frame.pack(pady=10, padx=10, fill="x")
        
        # From Date
        from_date_frame = ttk.Frame(filters_frame, padding=(0,0,20,0))
        from_date_frame.pack(side="left", padx=5, pady=5)
        ttk.Label(from_date_frame, text="From Date:", style='TLabel').pack(side="left", padx=10)
        self.from_date = ttk.Entry(from_date_frame, style='TEntry', font=("Times New Roman", 14, 'bold'), width=20)
        self.from_date.pack(side="left", ipady=2)
        
        # To Date
        to_date_frame = ttk.Frame(filters_frame, padding=(0,0,20,0))
        to_date_frame.pack(side="left", padx=5, pady=5)
        ttk.Label(to_date_frame, text="To Date:", style='TLabel').pack(side="left", padx=10)
        self.to_date = ttk.Entry(to_date_frame, style='TEntry', font=("Times New Roman", 14, 'bold'), width=20)
        self.to_date.pack(side="left", ipady=2)
        
        # Transaction Type
        transaction_type_frame = ttk.Frame(filters_frame, padding=(0,0,20,0))
        transaction_type_frame.pack(side="left", padx=5, pady=5)
        ttk.Label(transaction_type_frame, text="Transaction Type:", style='TLabel').pack(side="left")
        self.transaction_type = ttk.Combobox(transaction_type_frame, values=["All", "Deposit", "Withdrawal", "Transfer"], style="TCombobox", font=("Times New Roman", 14, 'bold'),state="readonly")
        self.transaction_type.pack(side="left", ipady=2)
        self.transaction_type.current(0)
        
        # Search Button
        search_button = ttk.Button(filters_frame, text="Search", command=self.load_transactions, width=20, style="TButton")
        search_button.pack(side="left", padx=5, pady=5)
        
        # Transaction History Table
        self.tree_th = ttk.Treeview(self, columns=("ID", "Date", "Time", "Account", "Type", "Amount", "Balance_Before", "Balance_After"), style="Custom.Treeview", show='headings')
        self.tree_th.heading("ID", text="TID")
        self.tree_th.heading("Date", text="Date")
        self.tree_th.heading("Time", text="Time")
        self.tree_th.heading("Account", text="Account")
        self.tree_th.heading("Type", text="Type")
        self.tree_th.heading("Amount", text="Amount")
        self.tree_th.heading("Balance_Before", text="Balance Before")
        self.tree_th.heading("Balance_After", text="Balance After")
        
        self.tree_th.column("ID", width=5)
        self.tree_th.column("Date", width=20)
        self.tree_th.column("Time", width=20)
        self.tree_th.column("Account", width=30)
        self.tree_th.column("Type", width=20)
        self.tree_th.column("Amount", width=30)
        self.tree_th.column("Balance_Before", width=60)
        self.tree_th.column("Balance_After", width=60)
        
        self.tree_th.pack(pady=10, padx=10, fill="both", expand=True)

        # Disable column sorting
        self.tree_th.heading("ID", command=lambda: None)
        self.tree_th.heading("Date", command=lambda: None)
        self.tree_th.heading("Time", command=lambda: None)
        self.tree_th.heading("Account", command=lambda: None)
        self.tree_th.heading("Type", command=lambda: None)
        self.tree_th.heading("Amount", command=lambda: None)
        self.tree_th.heading("Balance_Before", command=lambda: None)
        self.tree_th.heading("Balance_After", command=lambda: None)
        
    def load_transactions(self):
        from_date = self.from_date.get()
        to_date = self.to_date.get()
        transaction_type = self.transaction_type.get()

        conn = connect_to_db()
        cursor = conn.cursor()
        
        # Base query
        queryAll = f"SELECT transaction_id, transaction_date, transaction_time, account_number, transaction_type, amount, balance_before, balance_after FROM transaction_history where\
            transaction_date >= \'{from_date}\' and transaction_date <= \'{to_date}\'"
            
        querySingle = f"SELECT transaction_id, transaction_date, transaction_time, account_number, transaction_type, amount, balance_before, balance_after FROM transaction_history where\
            transaction_date >= \'{from_date}\' and transaction_date <= \'{to_date}\' and transaction_type = \'{transaction_type}\'"
        
        query = ""
        if transaction_type != 'All':
            query = querySingle
        else:
            query = queryAll
        cursor.execute(query)
        rows = cursor.fetchall()
        # print(rows)
        for row in self.tree_th.get_children():
            self.tree_th.delete(row)

        for row in rows:
            self.tree_th.insert("", tk.END, values=row)

#======================================
#        REPORT GENERATION PAGE       #
#======================================
class ReportGenerationPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        style = ttk.Style()
        style.configure('TLabel', font=("Times New Roman", 14), foreground="#499A51")
        style.configure('TButton', font=("Times New Roman", 18, 'bold'), foreground="#499A51")

        ttk.Label(self, text="Generate Report", style='TLabel', font=("Times New Roman", 24, 'bold')).pack(pady=20)

        filters_frame = ttk.Frame(self)
        filters_frame.pack(pady=10, padx=10, fill="x", anchor="center")

        from_date_frame = ttk.Frame(filters_frame, padding=(370, 0, 20, 0))
        from_date_frame.pack(side="left", padx=5, pady=5)
        ttk.Label(from_date_frame, text="From Date:", style='TLabel').pack(side="left", padx=10)
        self.from_date = DateEntry(from_date_frame, date_pattern='yyyy-mm-dd', width=20,
                                    background='#ffffff', foreground='#499A51',
                                    font=("Times New Roman", 14, 'bold'))
        self.from_date.pack(side="left", ipady=2)

        to_date_frame = ttk.Frame(filters_frame, padding=(0, 0, 20, 0))
        to_date_frame.pack(side="left", padx=5, pady=5)
        ttk.Label(to_date_frame, text="To Date:", style='TLabel').pack(side="left", padx=10)
        self.to_date = DateEntry(to_date_frame, date_pattern='yyyy-mm-dd', width=20,
                                  background='#ffffff', foreground='#499A51',
                                  font=("Times New Roman", 14, 'bold'))
        self.to_date.pack(side="left", ipady=2)

        button_frame = ttk.Frame(self, padding=(450, 0, 20, 0))
        button_frame.pack(pady=10, padx=10, fill="x", anchor="center")

        transaction_summary_button = ttk.Button(button_frame, text="Transaction Report", command=self.generate_transaction_summary, style="TButton", width=20)
        transaction_summary_button.pack(side="left", padx=10, pady=5)

        monthly_reports_button = ttk.Button(button_frame, text="Customer Demo.", command=self.generate_customer_demo, style="TButton", width=20)
        monthly_reports_button.pack(side="left", padx=10, pady=5)


    def generate_transaction_summary(self):
        from_date = self.from_date.get()
        to_date = self.to_date.get()
        
        transactions = self.fetch_transaction_data(from_date, to_date)
        
        if transactions:
            try:
                self.create_pdf(transactions)
                messagebox.showinfo("Success", "Transaction report generated successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate the report: {str(e)}")
        else:
            messagebox.showerror("Error", "No transactions found for the given date range.")

    def fetch_transaction_data(self, from_date, to_date):
        conn = connect_to_db()
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT transaction_id, account_number, transaction_date, transaction_time,
               transaction_type, amount, balance_before, balance_after, description
        FROM transaction_history
        WHERE transaction_date BETWEEN %s AND %s
        """
        
        cursor.execute(query, (from_date, to_date))
        transactions = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return transactions

    def create_pdf(self, transactions):
        pdf_file = "transaction_report.pdf"
        c = canvas.Canvas(pdf_file, pagesize=landscape(letter))
        width, height = landscape(letter) 
        
        c.setFont("Times-Roman", 24)
        c.drawString(72, height - 72, "Transaction Summary Report")
        
        header = f"{'Trans. ID':^12}|{'Account No.':^14}|{'Date':^14}|{'Time':^14}|{'Type':^12}|{'Amount':^16}|{'Before':^18}|{'After':^18}|{'Description':^40}|"
        c.setFont("Times-Roman", 12)
        c.drawString(72, height - 120, header)
        c.line(72, height - 122, width - 72, height - 122)
        
        print("\n\nGenerated Transaction Report: \n")
        print(header)
        
        y = height - 140 
        for transaction in transactions:
            if isinstance(transaction['transaction_time'], timedelta):
                total_seconds = int(transaction['transaction_time'].total_seconds())
                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                transaction_time = f"{hours:02}:{minutes:02}:{seconds:02}"
            else:
                transaction_time = transaction['transaction_time'].strftime("%H:%M:%S") if transaction['transaction_time'] else "N/A"
                
            tid = transaction['transaction_id']
            acn = transaction['account_number']
            tdate = str(transaction['transaction_date'])
            ttype = transaction['transaction_type']
            amt = transaction['amount']
            bb = transaction['balance_before']
            ba = transaction['balance_after']
            desc = str(transaction['description'])
            
            row = f"|{tid:^11}|{acn:^14}|{tdate:^14}|{transaction_time:^14}|{ttype:<12}|{amt:<16.2f}|{bb:<18.2f}|{ba:<18.2f}|{desc:<40}|"
            print(row)
            
            c.drawString(72, y, row)
            y -= 20 

            if y < 72:  
                c.showPage()
                c.setFont("Times-Roman", 24)
                c.drawString(72, height - 72, "Transaction Summary Report")
                c.setFont("Times-Roman", 12)
                c.drawString(72, height - 120, header)
                c.line(72, height - 122, width - 72, height - 122)
                y = height - 140

        c.save()
    
    def generate_customer_demo(self):
        customers = self.fetch_customer_data()
        
        if customers:
            try:
                self.create_customer_pdf(customers)
                messagebox.showinfo("Success", "Customer demographic report generated successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate the report: {str(e)}")
        else:
            messagebox.showerror("Error", "No customer data found.")

    def fetch_customer_data(self):
        conn = connect_to_db()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT account_number, first_name, middle_name, last_name, gender, dob, 
            address, phone_number, email, branch_id
        FROM accounts
        WHERE status = 'Active'
        """
        
        cursor.execute(query)
        customers = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return customers

    def create_customer_pdf(self, customers):
        pdf_file = "customer_demographic_report.pdf"
        c = canvas.Canvas(pdf_file, pagesize=landscape(letter))
        width, height = landscape(letter) 
        
        c.setFont("Times-Roman", 24)
        c.drawString(72, height - 72, "Customer Demographic Report")

        c.setFont("Times-Roman", 12)
        header = f"|{'Acc. No.':^10}|{'First Name':^15}|{'Last Name':^15}|{'Middle Name':^15}|{'Gender':^8}|{'DOB':^12}|{'Address':^55}|{'Phone':^12}|{'Email':^25}|{'Branch ID':^10}|"
        c.drawString(72, height - 120, header)
        c.line(72, height - 122, width - 72, height - 122)
        
        print("\n\nGenerated Customer Demographic Report: \n")
        print(header)
        
        y = height - 140
        for customer in customers:
            acc_num = customer['account_number']
            first_name = customer['first_name']
            middle_name = customer['middle_name'] if customer['middle_name'] else ""
            last_name = customer['last_name']
            gender = customer['gender']
            dob = customer['dob'].strftime("%Y-%m-%d") if customer['dob'] else "N/A"
            address = customer['address']
            phone = customer['phone_number']
            email = customer['email'] if customer['email'] else "N/A"
            branch_id = customer['branch_id']

            row = f"|{acc_num:^10}|{first_name:<15}|{middle_name:<15}|{last_name:<15}|{gender:<8}|{dob:^12}|{address:<55}|{phone:^12}|{email:<25}|{branch_id:^10}|"
            c.drawString(72, y, row)
            y -= 20  
            print(row)
            
            if y < 72:
                c.showPage()
                c.setFont("Times-Roman", 24)
                c.drawString(72, height - 72, "Customer Demographic Report")
                c.setFont("Times-Roman", 12)
                c.drawString(72, height - 120, header)
                c.line(72, height - 122, width - 72, height - 122)
                y = height - 140

        c.save()
            
#==============================================
#        INTEREST & FEE MANAGEMENT PAGE       #
#==============================================
class InterestFeeManagementPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.setupui()
        self.load_label_data()
        
    def setupui(self):
        style = ttk.Style()
        style.configure('TLabel', font=("Times New Roman", 14), foreground="#499A51")
        style.configure('TButton', font=("Times New Roman", 18, 'bold'), foreground="#499A51")

        # Page Title
        title_label = ttk.Label(self, text="Interest and Fee Management", style='TLabel', font=("Times New Roman", 24,'bold'), padding=(550,0,5,0))
        title_label.pack(pady=(10, 20), anchor="w")

        # Label Frame
        label_frame = ttk.Frame(self)
        label_frame.pack(padx=500,pady=15, anchor="w")
        
        # Interest Rate Label
        self.interest_rate_label = ttk.Label(label_frame, text="Current Interest Rate :", style='TLabel',font=("Times New Roman", 16))
        self.interest_rate_label.grid(row=0, column=1, padx=40, pady=10, sticky='w')
        
        # Interest Rate Entry
        self.interest_rate_entry = ttk.Entry(label_frame, font=("Times New Roman", 18, 'bold'), width=20, foreground="#499A51")
        self.interest_rate_entry.grid(row=0, column=2, padx=10, pady=10)
        
        # Fee Label
        self.fee_label = ttk.Label(label_frame, text="Current Fees :", style='TLabel',font=("Times New Roman", 16))
        self.fee_label.grid(row=1, column=1, padx=40, pady=10, sticky='w')
        
        # Fee Entry
        self.fee_entry = ttk.Entry(label_frame, font=("Times New Roman", 18, 'bold'), width=20, foreground="#499A51")
        self.fee_entry.grid(row=1, column=2, padx=10, pady=10)

        # Change Rate and Fee Button
        change_button = ttk.Button(label_frame, text="Change Interest Rate", command=self.change_rate, width=20, style="TButton")
        change_button.grid(row=2, column=1, padx=10, pady=10)

        # Apply Changes Button
        apply_button = ttk.Button(label_frame, text="Change Fee", command=self.change_fee, width=20, style="TButton")
        apply_button.grid(row=2, column=2, padx=10, pady=10)
        
        # Change Rate and Fee Button
        change_button = ttk.Button(label_frame, text="Apply Interest Rate", command=self.apply_changes_rate, width=20, style="TButton")
        change_button.grid(row=3, column=1, padx=10, pady=10)
        
        # Apply Changes Button
        apply_button = ttk.Button(label_frame, text="Deduct Fee", command=self.deduct_fee, width=20, style="TButton")
        apply_button.grid(row=3, column=2, padx=10, pady=10)
        
        self.load_label_data()
        
    def load_label_data(self):
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT interest_rate, fee from interest_fee_management")
            details = cursor.fetchone()
            fee = details[1]
            interest = details[0]
            
            if details:
                self.interest_rate_entry.config(state="normal")
                self.interest_rate_entry.delete(0, tk.END)
                self.interest_rate_entry.insert(0, f"{interest:.2f}%")
                self.interest_rate_entry.config(state="readonly")
                
                self.fee_entry.config(state="normal")
                self.fee_entry.delete(0, tk.END)
                self.fee_entry.insert(0, f"${fee:.2f}")
                self.fee_entry.config(state="readonly")
            else:
                messagebox.showerror("Error", "Interest Rates and Fee not set.")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        finally:
            cursor.close()
            conn.close()
        
    def change_rate(self):
        ChangeRateDialog(self)
        
    def change_fee(self):
        ChangeFeeDialog(self)
        
    def deduct_fee(self):
        response = messagebox.askyesno("Confirm Deduction", f"Are you sure you want to deduct fee?")
        if response:
            try:
                conn = connect_to_db()
                cursor = conn.cursor()
                cursor.execute("select fee from interest_fee_management")
                fee = cursor.fetchone()
                cursor.execute("update accounts set balance = balance - {}".format(float(fee[0])))
                conn.commit()
                cursor.close()
                conn.close()
                
                messagebox.showinfo("Success", "Fees deducted from all accounts successfully.")
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", str(err))

    def apply_changes_rate(self):
        response = messagebox.askyesno("Confirm Rates", f"Are you sure you want to provide interest rate?")
        if response:
            try:
                conn = connect_to_db()
                cursor = conn.cursor()
                cursor.execute("select interest_rate from interest_fee_management")
                interest_rate = cursor.fetchone()
                cursor.execute("update accounts set balance = balance + (balance * {} /100)".format(float(interest_rate[0])))
                conn.commit()
                cursor.close()
                conn.close()
                
                messagebox.showinfo("Success", "Interest applied to all accounts successfully.")
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", str(err))

class ChangeRateDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Change Rate")
        self.geometry("220x140")
        self.iconbitmap('/MYBM/bank.ico')
        self.resizable(0,0)
        self.grab_set()
        
        self.update_idletasks()
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_right = int((screen_width / 2) - (window_width / 2))
        position_down = int((screen_height / 2) - (window_height / 2))
        self.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.configure('TLabel', font=("Times New Roman", 14), foreground="#499A51")
        style.configure('TEntry', font=("Times New Roman", 18, 'bold'), foreground="#499A51")
        style.configure('TButton', font=('Times New Roman', 18, 'bold'), foreground="#499A51")

        ttk.Label(self, text="New Interest Rate (%):", font=("Times New Roman", 14), foreground="#499A51").pack(anchor="w", padx=15, pady=5)
        self.new_interest_rate_entry = ttk.Entry(self, font=("Times New Roman", 18, 'bold'), width=17, foreground="#499A51")
        self.new_interest_rate_entry.pack(pady=5, anchor='w', padx=15)

        ttk.Button(self, text="Save Changes", command=self.save_changes).pack(pady=10, anchor="center")

    def save_changes(self):
        try:
            self.new_interest_rate = float(self.new_interest_rate_entry.get())
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("update interest_fee_management set interest_rate = {}".format(self.new_interest_rate))
            conn.commit()
            cursor.close()
            conn.close()
            self.parent.load_label_data()
            self.destroy()
            messagebox.showinfo("Success", "Interest Rate updated. Click 'Apply Interest Rate' to apply rates.")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for interest rate.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
                  
class ChangeFeeDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Change Fee")
        self.geometry("220x140")
        self.iconbitmap('/MYBM/bank.ico')
        self.resizable(0,0)
        self.grab_set()
        
        self.update_idletasks()
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_right = int((screen_width / 2) - (window_width / 2))
        position_down = int((screen_height / 2) - (window_height / 2))
        self.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.configure('TLabel', font=("Times New Roman", 14), foreground="#499A51")
        style.configure('TEntry', font=("Times New Roman", 18, 'bold'), foreground="#499A51")
        style.configure('TButton', font=('Times New Roman', 18, 'bold'), foreground="#499A51")

        ttk.Label(self, text="New Fee:", font=("Times New Roman", 14), foreground="#499A51").pack(anchor="w", padx=15, pady=5)
        self.new_fee_entry = ttk.Entry(self, font=("Times New Roman", 18, 'bold'), width=17, foreground="#499A51")
        self.new_fee_entry.pack(pady=5, anchor='w', padx=15)

        ttk.Button(self, text="Save Changes", command=self.save_changes).pack(pady=10, anchor="center")

    def save_changes(self):
        try:
            self.new_fee = float(self.new_fee_entry.get())
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("update interest_fee_management set fee = {}".format(self.new_fee))
            conn.commit()
            cursor.close()
            conn.close()
            self.parent.load_label_data()
            self.destroy()
            messagebox.showinfo("Success", "Fee updated. Click 'Deduct Fee' to deduct maintenance fees.")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for fee.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            



#=================================================================================================================================================
#                                                                    STAFF PAGE                                                                  #
#=================================================================================================================================================   
class StaffPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        title_panel = ttk.Frame(self, style='TitlePanel.TFrame', padding=(0, 20, 0, 20))
        title_panel.pack(side='top', fill='x')

        button_panel = ttk.Frame(self, style='ButtonPanel.TFrame', padding=(20, 12, 20, 10))
        button_panel.pack(side='left', fill='y')

        title_label = ttk.Label(title_panel, text="STAFF DASHBOARD", background="#499A51", font=("Times New Roman", 32, 'bold'), foreground="#ffffff")
        title_label.pack(pady=10)

        # Create Account Button
        create_account_button = ttk.Button(button_panel, text="Create Account", command=self.create_account, style="Custom.TButton")
        create_account_button.pack(pady=10, fill="x")

        # Update Account Button
        update_account_button = ttk.Button(button_panel, text="Update Account", command=self.update_account, style="Custom.TButton")
        update_account_button.pack(pady=10, fill="x")

        # Close Account Button
        close_account_button = ttk.Button(button_panel, text="Close Account", command=self.close_account, style="Custom.TButton")
        close_account_button.pack(pady=10, fill="x")

        # Account Details Button
        account_details_button = ttk.Button(button_panel, text="Account Details", command=self.account_details, style="Custom.TButton")
        account_details_button.pack(pady=10, fill="x")

        # Reset Passwords Button
        reset_passwords_button = ttk.Button(button_panel, text="Reset Passwords", command=self.reset_passwords, style="Custom.TButton")
        reset_passwords_button.pack(pady=10, fill="x")

        # Logout Button
        logout_button = ttk.Button(button_panel, text="Logout", command=self.logout, style="Custom.TButton")
        logout_button.pack(pady=10, fill="x")

        # Style configuration
        style = ttk.Style()
        style.configure('Custom.TButton',
                        font=("Times New Roman", 18, 'bold'),
                        foreground='#499A51',
                        background='#499A51',
                        padding=10)
        style.configure('TitlePanel.TFrame', background='#499A51')
        style.configure('ButtonPanel.TFrame', background='#499A51')

        self.content_area = ttk.Frame(self)
        self.content_area.pack(side='right', fill='both', expand=True, padx=10, pady=10)

        self.show_content(CreateAccountPage)

    def show_content(self, content):
        for widget in self.content_area.winfo_children():
            widget.destroy()

        if content is not None:
            content_frame = content(self.content_area, self.controller)
            content_frame.pack(fill="both", expand=True)

    def create_account(self):
        self.show_content(CreateAccountPage)

    def update_account(self):
        self.show_content(UpdateAccountPage)

    def close_account(self):
        self.show_content(CloseAccountPage)

    def account_details(self):
        self.show_content(AccountDetailsPage)

    def reset_passwords(self):
        self.show_content(ResetPasswordPage)

    def logout(self):
        login_page = self.controller.frames[LoginPage]
        login_page.reset_fields()
        self.controller.show_frame(LoginPage)
        print(f"{current_user} Logged Out")

#==================================
#       CREATE ACCOUNT PAGE       #
#==================================
class CreateAccountPage(ttk.Frame):
    def __init__(self, parent, c):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        self.first_name_entry.focus_set()
        self.load_account_number()

    def setup_ui(self):
        # Title
        title_label = ttk.Label(self, text="Create New Account", font=("Times New Roman", 24, 'bold'), foreground='#499A51', padding=(700,0,5,0))
        title_label.pack(pady=10, anchor='w')
        
        # Form Frame
        form_frame = ttk.Frame(self)
        form_frame.pack(pady=20, padx=600, fill='x')

        # Account Number
        container1 = ttk.Frame(form_frame)
        container1.pack(anchor='w', pady=5, padx=5, fill='x')

        account_number_label = ttk.Label(container1, text="Account Number :", font=("Times New Roman", 14), foreground='#499A51')
        account_number_label.pack(side='left', padx=(5, 23))
        self.account_number_entry = ttk.Entry(container1, font=("Times New Roman", 16, 'bold'), width=26, state='readonly', foreground='#499A51')
        self.account_number_entry.pack(side='left', padx=5)

        # First Name
        container2 = ttk.Frame(form_frame)
        container2.pack(anchor='w', pady=5, padx=5, fill='x')

        first_name_label = ttk.Label(container2, text="First Name :", font=("Times New Roman", 14), foreground='#499A51')
        first_name_label.pack(side='left', padx=(5, 70))
        self.first_name_entry = ttk.Entry(container2, font=("Times New Roman", 16, 'bold'), width=26, foreground='#499A51')
        self.first_name_entry.pack(side='left', padx=5)

        # Middle Name
        container3 = ttk.Frame(form_frame)
        container3.pack(anchor='w', pady=5, padx=5, fill='x')

        middle_name_label = ttk.Label(container3, text="Middle Name :", font=("Times New Roman", 14), foreground='#499A51')
        middle_name_label.pack(side='left', padx=(5, 52))
        self.middle_name_entry = ttk.Entry(container3, font=("Times New Roman", 16, 'bold'), width=26, foreground='#499A51')
        self.middle_name_entry.pack(side='left', padx=5)

        # Last Name
        container4 = ttk.Frame(form_frame)
        container4.pack(anchor='w', pady=5, padx=5, fill='x')

        last_name_label = ttk.Label(container4, text="Last Name :", font=("Times New Roman", 14), foreground='#499A51')
        last_name_label.pack(side='left', padx=(5, 72))
        self.last_name_entry = ttk.Entry(container4, font=("Times New Roman", 16, 'bold'), width=26, foreground='#499A51')
        self.last_name_entry.pack(side='left', padx=5)

        # Gender
        container5 = ttk.Frame(form_frame)
        container5.pack(anchor='w', pady=5, padx=5, fill='x')

        gender_label = ttk.Label(container5, text="Gender :", font=("Times New Roman", 14), foreground='#499A51')
        gender_label.pack(side='left', padx=(5, 91))
        self.gender_var = tk.StringVar(value="Male")
        gender_frame = ttk.Frame(container5)
        gender_frame.pack(side='left', padx=5)
        ttk.Radiobutton(gender_frame, text="Male", variable=self.gender_var, value="Male").pack(side='left', padx=5)
        ttk.Radiobutton(gender_frame, text="Female", variable=self.gender_var, value="Female").pack(side='left', padx=5)
        ttk.Radiobutton(gender_frame, text="Other", variable=self.gender_var, value="Other").pack(side='left', padx=5)

        # Phone Number
        container6 = ttk.Frame(form_frame)
        container6.pack(anchor='w', pady=5, padx=5, fill='x')

        phone_number_label = ttk.Label(container6, text="Phone Number :", font=("Times New Roman", 14), foreground='#499A51')
        phone_number_label.pack(side='left', padx=(5, 39))
        self.phone_number_entry = ttk.Entry(container6, font=("Times New Roman", 16, 'bold'), width=26, foreground='#499A51')
        self.phone_number_entry.pack(side='left', padx=5)

        # Email
        container7 = ttk.Frame(form_frame)
        container7.pack(anchor='w', pady=5, padx=5, fill='x')
        
        email_label = ttk.Label(container7, text="Email :", font=("Times New Roman", 14), foreground='#499A51')
        email_label.pack(side='left', padx=(5, 110))
        self.email_entry = ttk.Entry(container7, font=("Times New Roman", 16, 'bold'), width=26, foreground='#499A51')
        self.email_entry.pack(side='left', padx=5)

        # Date of Birth
        container8 = ttk.Frame(form_frame)
        container8.pack(anchor='w', pady=5, padx=5, fill='x')

        dob_label = ttk.Label(container8, text="Date of Birth :", font=("Times New Roman", 14), foreground='#499A51')
        dob_label.pack(side='left', padx=(5, 56))
        self.dob_entry = ttk.Entry(container8, font=("Times New Roman", 16,'bold'), width=12, state='readonly', foreground='#499A51')
        self.dob_entry.pack(side='left', padx=5)

        self.dob_button = ttk.Button(container8, text="Select Date", command=self.select_date)
        self.dob_button.pack(side='left', padx=5)

        # Address
        container9 = ttk.Frame(form_frame)
        container9.pack(anchor='w', pady=5, padx=5, fill='x')

        address_label = ttk.Label(container9, text="Address :", font=("Times New Roman", 14), foreground='#499A51')
        address_label.pack(side='left', padx=(5, 88))
        self.address_entry = ttk.Entry(container9, font=("Times New Roman", 16, 'bold'), width=26, foreground='#499A51')
        self.address_entry.pack(side='left', padx=5)

        # Account Type
        container12 = ttk.Frame(form_frame)
        container12.pack(anchor='w', pady=5, padx=5, fill='x')

        account_type_label = ttk.Label(container12, text="Account Type :", font=("Times New Roman", 14), foreground='#499A51')
        account_type_label.pack(side='left', padx=(5, 46))
        self.account_type_combobox = ttk.Combobox(container12, font=("Times New Roman", 16, 'bold'), width=24, state='normal', foreground='#499A51')
        self.account_type_combobox['values'] = ("Savings", "Current")
        self.account_type_combobox.pack(side='left', padx=5)
        self.account_type_combobox.set('Savings')
        
        # Initial Balance
        container11 = ttk.Frame(form_frame)
        container11.pack(anchor='w', pady=5, padx=5, fill='x')

        initial_balance_label = ttk.Label(container11, text="Initial Balance :", font=("Times New Roman", 14), foreground='#499A51')
        initial_balance_label.pack(side='left', padx=(5, 49))
        self.initial_balance_entry = ttk.Entry(container11, font=("Times New Roman", 16, 'bold'), width=26, foreground='#499A51')
        self.initial_balance_entry.pack(side='left', padx=5)

        # Branch ID
        container10 = ttk.Frame(form_frame)
        container10.pack(anchor='w', pady=5, padx=5, fill='x')

        branch_id_label = ttk.Label(container10, text="Branch ID :", font=("Times New Roman", 14), foreground='#499A51')
        branch_id_label.pack(side='left', padx=(5, 75))
        self.branch_id_entry = ttk.Entry(container10, font=("Times New Roman", 16, 'bold'), width=26, foreground='#499A51')
        self.branch_id_entry.pack(side='left', padx=5)


        # Username
        container11 = ttk.Frame(form_frame)
        container11.pack(anchor='w', pady=5, padx=5, fill='x')

        username_label = ttk.Label(container11, text="Username :", font=("Times New Roman", 14), foreground='#499A51')
        username_label.pack(side='left', padx=(5, 77))
        self.username_entry = ttk.Entry(container11, font=("Times New Roman", 16, 'bold'), width=26, foreground='#499A51')
        self.username_entry.pack(side='left', padx=5)
        
        # Password
        container12 = ttk.Frame(form_frame)
        container12.pack(anchor='w', pady=5, padx=5, fill='x')

        password_label = ttk.Label(container12, text="Password :", font=("Times New Roman", 14), foreground='#499A51')
        password_label.pack(side='left', padx=(5, 77))
        self.password_entry = ttk.Entry(container12, font=("Times New Roman", 16, 'bold'), show="*", width=26, foreground='#499A51')
        self.password_entry.pack(side='left', padx=5)
        
        # Confirm Password
        container13 = ttk.Frame(form_frame)
        container13.pack(anchor='w', pady=5, padx=5, fill='x')

        confirm_password_label = ttk.Label(container13, text="Confirm Password :", font=("Times New Roman", 14), foreground='#499A51')
        confirm_password_label.pack(side='left', padx=(5, 10))
        self.confirm_password_entry = ttk.Entry(container13, font=("Times New Roman", 16, 'bold'), show="*", width=26, foreground='#499A51')
        self.confirm_password_entry.pack(side='left', padx=5)
        
        # Create Account Button
        button_frame = ttk.Frame(self)
        button_frame.pack(padx=5, anchor='w')

        self.create_button = ttk.Button(button_frame, text="Create Account", command=self.submit_form, style="TButton", width=20)
        self.create_button.pack(padx=725)

    def validate_email(self, email):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(email_regex, email):
            return True
        else:
            messagebox.showerror("Invalid Email", "Please enter a valid email address.")
            return False
    
    def validate_initial_balance(self, balance):
        try:
            balance = float(balance)
            if balance >= 0:
                return True
            else:
                messagebox.showerror("Invalid Balance", "Initial balance must be a non-negative number.")
                return False
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for the initial balance.")
            return False
    
    def validate_phone_number(self, phone_number):
        if phone_number.isdigit() and len(phone_number) == 10:
            return True
        else:
            messagebox.showerror("Invalid Phone Number", "Please enter a valid 10-digit phone number.")
            return False

    def submit_form(self):
        email = self.email_entry.get()
        balance = self.initial_balance_entry.get()
        phone_number = self.phone_number_entry.get()
        
        if not self.validate_phone_number(phone_number):
            return
        if not self.validate_email(email):
            return
        if not self.validate_initial_balance(balance):
            return
        
        self.create_account()

    def load_account_number(self):
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT MAX(account_number) FROM accounts")
            max_account_number = cursor.fetchone()[0]
            if max_account_number is None:
                next_account_number = 10001
            else:
                next_account_number = max_account_number + 1
            self.account_number_entry.config(state='normal')
            self.account_number_entry.delete(0, tk.END)
            self.account_number_entry.insert(0, str(next_account_number))
            self.account_number_entry.config(state='readonly')
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))

    def select_date(self):
        date_window = tk.Toplevel(self)
        date_window.title("Select Date")
        date_window.geometry("160x100")
        date_window.iconbitmap('/MYBM/bank.ico')
        date_window.resizable(0,0)
        date_window.grab_set()

        date_window.update_idletasks()
        window_width = date_window.winfo_width()
        window_height = date_window.winfo_height()
        screen_width = date_window.winfo_screenwidth()
        screen_height = date_window.winfo_screenheight()
        position_right = int((screen_width / 2) - (window_width / 2))
        position_down = int((screen_height / 2) - (window_height / 2))
        date_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

        date_entry = DateEntry(date_window, 
                            date_pattern='yyyy-mm-dd', 
                            width=11,
                            background='#ffffff', 
                            foreground='#499A51',
                            font=("Times New Roman", 14, 'bold'))
        date_entry.pack(pady=10)

        select_button = ttk.Button(date_window, text="Select", command=lambda: self.set_date(date_entry, date_window), width=11)
        select_button.pack(pady=5)

    def set_date(self, date_entry, date_window):
        selected_date = date_entry.get_date().strftime('%Y-%m-%d')
        self.dob_entry.config(state='normal')
        self.dob_entry.delete(0, tk.END)
        self.dob_entry.insert(0, selected_date)
        self.dob_entry.config(state='readonly')
        date_window.destroy()
        
    def clear_entries(self):
        self.first_name_entry.delete(0, tk.END)
        self.middle_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)
        self.gender_var.set("Male")
        self.phone_number_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.dob_entry.config(state='normal')
        self.dob_entry.delete(0, tk.END)
        self.dob_entry.config(state='readonly')
        self.address_entry.delete(0, tk.END)
        self.branch_id_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.confirm_password_entry.delete(0, tk.END)
        self.account_type_combobox.set('Savings')
        self.initial_balance_entry.delete(0, tk.END)
        self.load_account_number() 
        
    def create_account(self):
        account_number = self.account_number_entry.get()
        first_name = self.first_name_entry.get()
        middle_name = self.middle_name_entry.get()
        last_name = self.last_name_entry.get()
        gender = self.gender_var.get()
        phone_number = self.phone_number_entry.get()
        email = self.email_entry.get()
        dob = self.dob_entry.get()
        address = self.address_entry.get()
        branch_id = self.branch_id_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        con_password = self.confirm_password_entry.get()
        account_type = self.account_type_combobox.get()
        initial_balance = self.initial_balance_entry.get()
        
        if account_type == "":
            account_type = 'Savings'
        if initial_balance == "":
            initial_balance = 1000
        
        if not all([first_name, last_name, gender, phone_number, email, dob, address, branch_id, username, password, con_password]):
            messagebox.showerror("Input Error", "Please fill in all required fields.")
            return
        
        if password != con_password:
            messagebox.showerror("Password Mismatch", "Passwords didn't match\nPlease try again.")
            return
        
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO users (username, password, user_type) VALUES (%s, %s, 'customer')
            """, (username, password))
            
            cursor.execute("""
                INSERT INTO accounts (
                    account_number, username, account_type, balance, branch_id,
                    first_name, middle_name, last_name, address, phone_number, dob, gender, email
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (account_number, username, account_type, initial_balance, branch_id, 
                first_name, middle_name, last_name, address, phone_number, dob, gender, email))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            messagebox.showinfo("Success", "Account created successfully.")
            self.clear_entries()    
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))

#==================================
#       UPDATE ACCOUNT PAGE       #
#==================================
class UpdateAccountPage(ttk.Frame):
    def __init__(self, parent, c):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        self.account_number_entry.focus_set()

    def setup_ui(self):
        self.open_find_dialog()
        
        self.title_label = ttk.Label(self, text="Update Account", font=("Times New Roman", 24, 'bold'), foreground='#499A51', padding=(90,0,5,20))
        self.title_label.grid(row=0, column=0, pady=10, sticky='w', padx=630)

        self.create_find_frame()
        
    def create_find_frame(self):
        self.find_frame = ttk.Frame(self, padding=(630,0,0,0))
        self.find_frame.grid(row=1, column=0, padx=5, pady=5, sticky='w')

        self.update_button = ttk.Button(self.find_frame, text="Find Account", command=self.open_find_dialog, style="TButton", width=18)
        self.update_button.grid(row=0, column=0, padx=85)
        
    def open_find_dialog(self):
        find_dialog = tk.Toplevel(self)
        find_dialog.title("Find Account")
        find_dialog.geometry("200x120")
        find_dialog.iconbitmap('/MYBM/bank.ico')
        find_dialog.resizable(0,0)
        find_dialog.grab_set()

        tk.Label(find_dialog, text="Account Number:", font=("Times New Roman", 14), foreground='#499A51').pack(ipadx=13, anchor='w')

        self.account_number_entry = ttk.Entry(find_dialog, font=("Times New Roman", 16, 'bold'), foreground='#499A51', width=15)
        self.account_number_entry.pack(pady=5)
        self.account_number_entry.focus_set()
        
        find_button = ttk.Button(find_dialog, text="Find", command=lambda: self.find_account(find_dialog))
        find_button.pack(pady=5)
        
        find_dialog.update_idletasks()
        window_width = find_dialog.winfo_width()
        window_height = find_dialog.winfo_height()
        screen_width = find_dialog.winfo_screenwidth()
        screen_height = find_dialog.winfo_screenheight()
        position_right = int((screen_width / 2) - (window_width / 2))
        position_down = int((screen_height / 2) - (window_height / 2))
        find_dialog.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

    def find_account(self, dialog):
        self.account_number = self.account_number_entry.get()
        if not self.account_number:
            messagebox.showerror("Input Error", "Please enter an account number.")
            return
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM accounts WHERE account_number = %s", (self.account_number,))
            account = cursor.fetchone()
            if account:
                messagebox.showinfo("Success", "Account found.")
                dialog.destroy()
                self.open_update_form(self.account_number)
            else:
                messagebox.showerror("Error", "Account not found.")
                self.account_number_entry.delete(0, tk.END)
                self.account_number_entry.focus_set()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        finally:
            cursor.close()
            conn.close()

    def open_update_form(self, account_number):
        self.find_frame.destroy()

        self.update_frame = ttk.Frame(self, padding=(600,10,0,0))
        self.update_frame.grid(row=1, column=0, padx=5, pady=5, sticky='w')

        self.create_update_fields(account_number)

        button_frame = ttk.Frame(self.update_frame)
        button_frame.grid(row=10, column=0, columnspan=2, pady=10)

        update_button = ttk.Button(button_frame, text="Update", command=self.update_account)
        update_button.grid(row=0, column=0, padx=10)

        cancel_button = ttk.Button(button_frame, text="Cancel", command=self.cancel_update)
        cancel_button.grid(row=0, column=1, padx=10)

    def create_update_fields(self, account_number):
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT first_name, middle_name, last_name, phone_number, email, address, account_type, username FROM accounts WHERE account_number = {}".format(account_number))
            account = cursor.fetchone()
            
            if account:
            # Create Labels and Entry Boxes manually
                ttk.Label(self.update_frame, text="First Name:", font=("Times New Roman", 14), foreground='#499A51').grid(row=0, column=0, sticky='w', padx=10, pady=5)
                self.first_name_entry = ttk.Entry(self.update_frame, font=("Times New Roman", 16, 'bold'), foreground='#499A51', width=25)
                self.first_name_entry.grid(row=0, column=1, padx=10, pady=5)
                self.first_name_entry.insert(0, account[0])

                ttk.Label(self.update_frame, text="Middle Name:", font=("Times New Roman", 14), foreground='#499A51').grid(row=1, column=0, sticky='w', padx=10, pady=5)
                self.middle_name_entry = ttk.Entry(self.update_frame, font=("Times New Roman", 16, 'bold'), foreground='#499A51', width=25)
                self.middle_name_entry.grid(row=1, column=1, padx=10, pady=5)
                self.middle_name_entry.insert(0, account[1])

                ttk.Label(self.update_frame, text="Last Name:", font=("Times New Roman", 14), foreground='#499A51').grid(row=2, column=0, sticky='w', padx=10, pady=5)
                self.last_name_entry = ttk.Entry(self.update_frame, font=("Times New Roman", 16, 'bold'), foreground='#499A51', width=25)
                self.last_name_entry.grid(row=2, column=1, padx=10, pady=5)
                self.last_name_entry.insert(0, account[2])

                ttk.Label(self.update_frame, text="Phone Number:", font=("Times New Roman", 14), foreground='#499A51').grid(row=3, column=0, sticky='w', padx=10, pady=5)
                self.phone_number_entry = ttk.Entry(self.update_frame, font=("Times New Roman", 16, 'bold'), foreground='#499A51', width=25)
                self.phone_number_entry.grid(row=3, column=1, padx=10, pady=5)
                self.phone_number_entry.insert(0, account[3])

                ttk.Label(self.update_frame, text="Email:", font=("Times New Roman", 14), foreground='#499A51').grid(row=4, column=0, sticky='w', padx=10, pady=5)
                self.email_entry = ttk.Entry(self.update_frame, font=("Times New Roman", 16, 'bold'), foreground='#499A51', width=25)
                self.email_entry.grid(row=4, column=1, padx=10, pady=5)
                self.email_entry.insert(0, account[4])

                ttk.Label(self.update_frame, text="Address:", font=("Times New Roman", 14), foreground='#499A51').grid(row=5, column=0, sticky='w', padx=10, pady=5)
                self.address_entry = ttk.Entry(self.update_frame, font=("Times New Roman", 16, 'bold'), foreground='#499A51', width=25)
                self.address_entry.grid(row=5, column=1, padx=10, pady=5)
                self.address_entry.insert(0, account[5])

                ttk.Label(self.update_frame, text="Account Type:", font=("Times New Roman", 14), foreground='#499A51').grid(row=6, column=0, sticky='w', padx=10, pady=5)
                self.account_type_entry = ttk.Entry(self.update_frame, font=("Times New Roman", 16, 'bold'), foreground='#499A51', width=25)
                self.account_type_entry.grid(row=6, column=1, padx=10, pady=5)
                self.account_type_entry.insert(0, account[6])

                ttk.Label(self.update_frame, text="Username:", font=("Times New Roman", 14), foreground='#499A51').grid(row=7, column=0, sticky='w', padx=10, pady=5)
                self.username_entry = ttk.Entry(self.update_frame, font=("Times New Roman", 16, 'bold'), foreground='#499A51', width=25)
                self.username_entry.grid(row=7, column=1, padx=10, pady=5)
                self.username_entry.insert(0, account[7])

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        finally:
            cursor.close()
            conn.close()

    def update_account(self):
        first_name = self.first_name_entry.get()
        middle_name = self.middle_name_entry.get()
        last_name = self.last_name_entry.get()
        phone_number = self.phone_number_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()
        account_type = self.account_type_entry.get()
        username = self.username_entry.get()

        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute(f"""UPDATE accounts SET first_name = \'{first_name}\', middle_name = \'{middle_name}\', last_name = \'{last_name}\', phone_number = {phone_number}, email = \'{email}\',
                address = \'{address}\', account_type = \'{account_type}\', username = \'{username}\' WHERE account_number = {self.account_number}""")
            conn.commit()
            messagebox.showinfo("Success", "Account updated successfully.")
            self.cancel_update()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        finally:
            cursor.close()
            conn.close()
            
    def clear_entries(self):
        self.first_name_entry.delete(0, tk.END)
        self.middle_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)
        self.phone_number_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.account_type_entry.delete(0,tk.END)
        self.username_entry.delete(0, tk.END)
        
    def cancel_update(self):
        self.update_frame.destroy()
        self.create_find_frame()
        self.title_label.grid(row=0, column=0, pady=10, sticky='w')

#==================================
#       CLOSE ACCOUNT PAGE        #
#==================================
class CloseAccountPage(ttk.Frame):  
    def __init__(self, parent, c):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        self.account_number_entry.focus_set()
        
    def setup_ui(self):
        self.open_find_dialog()
        
        self.title_label = ttk.Label(self, text="Close Account", font=("Times New Roman", 24, 'bold'), foreground='#499A51', padding=(90,0,5,20))
        self.title_label.grid(row=0, column=0, pady=10, sticky='w', padx=630)

        self.create_find_frame()
        
    def create_find_frame(self):
        self.find_frame = ttk.Frame(self, padding=(630,0,0,0))
        self.find_frame.grid(row=1, column=0, padx=5, pady=5, sticky='w')

        self.close_button = ttk.Button(self.find_frame, text="Close Account", command=self.open_find_dialog, style="TButton", width=18)
        self.close_button.grid(row=0, column=0, padx=85)

    def open_find_dialog(self):
        find_dialog = tk.Toplevel(self)
        find_dialog.title("Close Account")
        find_dialog.geometry("200x120")
        find_dialog.iconbitmap('/MYBM/bank.ico')
        find_dialog.resizable(0,0)
        find_dialog.grab_set()

        tk.Label(find_dialog, text="Account Number :", font=("Times New Roman", 14), foreground='#499A51').pack(ipadx=13, anchor='w')

        self.account_number_entry = ttk.Entry(find_dialog, font=("Times New Roman", 16, 'bold'), foreground='#499A51', width=15)
        self.account_number_entry.pack(pady=5)
        self.account_number_entry.focus_set()
        
        find_button = ttk.Button(find_dialog, text="Close", command=lambda: self.find_account(find_dialog))
        find_button.pack(pady=5)

        find_dialog.update_idletasks()
        window_width = find_dialog.winfo_width()
        window_height = find_dialog.winfo_height()
        screen_width = find_dialog.winfo_screenwidth()
        screen_height = find_dialog.winfo_screenheight()
        position_right = int((screen_width / 2) - (window_width / 2))
        position_down = int((screen_height / 2) - (window_height / 2))
        find_dialog.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")
    
    def find_account(self, dialog):
        self.account_number = self.account_number_entry.get()
        if not self.account_number:
            messagebox.showerror("Input Error", "Please enter an account number.")
            return
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM accounts WHERE account_number = %s", (self.account_number,))
            account = cursor.fetchone()
            if account:
                messagebox.showinfo("Success", "Account found.")
                dialog.destroy()
                self.open_delete_form(self.account_number)
            else:
                messagebox.showerror("Error", "Account not found.")
                self.account_number_entry.delete(0, tk.END)
                self.account_number_entry.focus_set()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        finally:
            cursor.close()
            conn.close()
            
    def open_delete_form(self, account_number):
        self.find_frame.destroy()

        self.delete_frame = ttk.Frame(self, padding=(600,10,0,0))
        self.delete_frame.grid(row=1, column=0, padx=5, pady=5, sticky='w')

        self.create_delete_fields(account_number)

        button_frame = ttk.Frame(self.delete_frame)
        button_frame.grid(row=10, column=0, columnspan=2, pady=10)

        delete_button = ttk.Button(button_frame, text="Delete", command=self.delete_account)
        delete_button.grid(row=0, column=0, padx=10)

        cancel_button = ttk.Button(button_frame, text="Cancel", command=self.refresh_page)
        cancel_button.grid(row=0, column=1, padx=10)

    def create_delete_fields(self, account_number):
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT first_name, middle_name, last_name, phone_number, email, address, account_type, username FROM accounts WHERE account_number = {}".format(account_number))
            account = cursor.fetchone()
            
            if account:
            # Create Labels and Entry Boxes manually
                ttk.Label(self.delete_frame, text="First Name :", font=("Times New Roman", 14), foreground='#499A51').grid(row=0, column=0, sticky='w', padx=10, pady=5)
                self.first_name_entry = ttk.Entry(self.delete_frame, font=("Times New Roman", 16, 'bold'), foreground='#499A51', width=25)
                self.first_name_entry.grid(row=0, column=1, padx=10, pady=5)

                ttk.Label(self.delete_frame, text="Middle Name :", font=("Times New Roman", 14), foreground='#499A51').grid(row=1, column=0, sticky='w', padx=10, pady=5)
                self.middle_name_entry = ttk.Entry(self.delete_frame, font=("Times New Roman", 16, 'bold'), foreground='#499A51', width=25)
                self.middle_name_entry.grid(row=1, column=1, padx=10, pady=5)

                ttk.Label(self.delete_frame, text="Last Name :", font=("Times New Roman", 14), foreground='#499A51').grid(row=2, column=0, sticky='w', padx=10, pady=5)
                self.last_name_entry = ttk.Entry(self.delete_frame, font=("Times New Roman", 16, 'bold'), foreground='#499A51', width=25)
                self.last_name_entry.grid(row=2, column=1, padx=10, pady=5)

                ttk.Label(self.delete_frame, text="Phone Number :", font=("Times New Roman", 14), foreground='#499A51').grid(row=3, column=0, sticky='w', padx=10, pady=5)
                self.phone_number_entry = ttk.Entry(self.delete_frame, font=("Times New Roman", 16, 'bold'), foreground='#499A51', width=25)
                self.phone_number_entry.grid(row=3, column=1, padx=10, pady=5)

                ttk.Label(self.delete_frame, text="Email :", font=("Times New Roman", 14), foreground='#499A51').grid(row=4, column=0, sticky='w', padx=10, pady=5)
                self.email_entry = ttk.Entry(self.delete_frame, font=("Times New Roman", 16, 'bold'), foreground='#499A51', width=25)
                self.email_entry.grid(row=4, column=1, padx=10, pady=5)

                ttk.Label(self.delete_frame, text="Address :", font=("Times New Roman", 14), foreground='#499A51').grid(row=5, column=0, sticky='w', padx=10, pady=5)
                self.address_entry = ttk.Entry(self.delete_frame, font=("Times New Roman", 16, 'bold'), foreground='#499A51', width=25)
                self.address_entry.grid(row=5, column=1, padx=10, pady=5)

                ttk.Label(self.delete_frame, text="Account Type :", font=("Times New Roman", 14), foreground='#499A51').grid(row=6, column=0, sticky='w', padx=10, pady=5)
                self.account_type_entry = ttk.Entry(self.delete_frame, font=("Times New Roman", 16, 'bold'), foreground='#499A51', width=25)
                self.account_type_entry.grid(row=6, column=1, padx=10, pady=5)

                ttk.Label(self.delete_frame, text="Username :", font=("Times New Roman", 14), foreground='#499A51').grid(row=7, column=0, sticky='w', padx=10, pady=5)
                self.username_entry = ttk.Entry(self.delete_frame, font=("Times New Roman", 16, 'bold'), foreground='#499A51', width=25)
                self.username_entry.grid(row=7, column=1, padx=10, pady=5)
                
                self.first_name_entry.config(state='normal')
                self.first_name_entry.delete(0, tk.END)
                self.first_name_entry.insert(0, account[0])
                self.first_name_entry.config(state='readonly')
                
                self.middle_name_entry.config(state='normal')
                self.middle_name_entry.delete(0, tk.END)
                self.middle_name_entry.insert(0, account[1])
                self.middle_name_entry.config(state='readonly')
                
                self.last_name_entry.config(state='normal')
                self.last_name_entry.delete(0, tk.END)
                self.last_name_entry.insert(0, account[2])
                self.last_name_entry.config(state='readonly')
                
                self.phone_number_entry.config(state='normal')
                self.phone_number_entry.delete(0, tk.END)
                self.phone_number_entry.insert(0, account[3])
                self.phone_number_entry.config(state='readonly')
                
                self.email_entry.config(state='normal')
                self.email_entry.delete(0, tk.END)
                self.email_entry.insert(0, account[4])
                self.email_entry.config(state='readonly')
                
                self.address_entry.config(state='normal')
                self.address_entry.delete(0, tk.END)
                self.address_entry.insert(0, account[5])
                self.address_entry.config(state='readonly')
                
                self.account_type_entry.config(state='normal')
                self.account_type_entry.delete(0, tk.END)
                self.account_type_entry.insert(0, account[6])
                self.account_type_entry.config(state='readonly')
                
                self.username_entry.config(state='normal')
                self.username_entry.delete(0, tk.END)
                self.username_entry.insert(0, account[7])
                self.username_entry.config(state='readonly')
                
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        finally:
            cursor.close()
            conn.close()

    def delete_account(self):
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to close this account?")
        if not confirm:
            messagebox.showinfo("Not Closed", "Account Not CLosed.")
            self.refresh_page()
        else:
            try:
                conn = connect_to_db()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM accounts WHERE account_number = {}".format(self.account_number,))
                account = cursor.fetchone()
                if account:
                    cursor.execute("DELETE FROM accounts WHERE account_number = {}".format(self.account_number,))
                    conn.commit()
                    messagebox.showinfo("Success", "Account closed successfully.")
                    self.refresh_page()
                else:
                    messagebox.showerror("Error", "Account not found.")
                    self.account_number_entry.delete(0, tk.END)
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", str(err))
            finally:
                cursor.close()
                conn.close()
    
    def refresh_page(self):
        self.delete_frame.destroy()
        self.create_find_frame()
        self.title_label.grid(row=0, column=0, pady=10, sticky='w')

#==================================
#       ACCOUNT DETAILS PAGE      #
#==================================
class AccountDetailsPage(ttk.Frame):
    def __init__(self, parent, c):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        self.title_label = ttk.Label(self, text="Account Details", font=("Times New Roman", 24, 'bold'), foreground='#499A51', padding=(90,0,5,0))
        self.title_label.pack(pady=10, anchor='w', padx=630)
        
        self.main_frame = ttk.Frame(self, padding=(580,0,0,0))
        self.main_frame.pack(padx=20, pady=20, fill='both', expand=True)

        ttk.Label(self.main_frame, text="Account Number :", font=("Times New Roman", 14), foreground='#499A51').grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.account_number_entry = ttk.Entry(self.main_frame, font=("Times New Roman", 16, 'bold'), foreground='#499A51', width=13)
        self.account_number_entry.grid(row=1, column=1, padx=10, pady=5, columnspan=2, sticky='w')
        self.account_number_entry.focus_set()

        search_button = ttk.Button(self.main_frame, text="Search", command=self.find_account)
        search_button.grid(row=1, column=1, padx=5, columnspan=2, pady=10, sticky='e')

        self.create_account_details_fields()

        clear_button = ttk.Button(self.main_frame, text="Clear", command=self.clear_fields)
        clear_button.grid(row=15, column=0, columnspan=2, pady=20)

    def create_account_details_fields(self):
        labels = ["First Name", "Middle Name", "Last Name", "Gender", "Phone Number", "Email", "Date of Birth", "Address", "Account Type", "Balance"]
        self.entries = {}

        for i, label_text in enumerate(labels):
            row = i + 2
            ttk.Label(self.main_frame, text=f"{label_text} :", font=("Times New Roman", 14), foreground='#499A51').grid(row=row, column=0, sticky='w', padx=10, pady=5)
            entry = ttk.Entry(self.main_frame, font=("Times New Roman", 16, 'bold'), foreground='#499A51', width=25, state="readonly")
            entry.grid(row=row, column=1, padx=10, pady=5)
            self.entries[label_text] = entry

    def find_account(self):
        account_number = self.account_number_entry.get()
        if not account_number:
            messagebox.showerror("Input Error", "Please enter an account number.")
            return
        try:
            conn = connect_to_db() 
            cursor = conn.cursor()
            cursor.execute("SELECT first_name, middle_name, last_name, gender, phone_number, email, dob, address, account_type, balance FROM accounts WHERE account_number = %s", (account_number,))
            account = cursor.fetchone()
            if account:
                self.display_account_details(account)
            else:
                messagebox.showerror("Error", "Account not found.")
                self.clear_fields()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        finally:
            cursor.close()

    def display_account_details(self, account):
        for key, entry in zip(self.entries.keys(), account):
            self.entries[key].config(state="normal")
            self.entries[key].delete(0, tk.END)
            self.entries[key].insert(0, entry)
            self.entries[key].config(state="readonly")

    def clear_fields(self):
        self.account_number_entry.delete(0, tk.END)
        for entry in self.entries.values():
            entry.config(state="normal")
            entry.delete(0, tk.END)
            entry.config(state="readonly")

#==================================
#       RESET PASSWORD PAGE       #
#==================================
class ResetPasswordPage(ttk.Frame):
    def __init__(self, parent, c):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        self.account_number_entry.focus_set()
        
    def setup_ui(self):
        self.open_find_dialog()
        
        self.title_label = ttk.Label(self, text="Reset Password", font=("Times New Roman", 24, 'bold'), foreground='#499A51', padding=(90,0,5,10))
        self.title_label.grid(row=0, column=0, pady=10, sticky='w', padx=630)

        self.create_find_frame()
        
    def create_find_frame(self):
        self.find_frame = ttk.Frame(self, padding=(630,0,0,0))
        self.find_frame.grid(row=1, column=0, padx=5, pady=5, sticky='w')

        self.close_button = ttk.Button(self.find_frame, text="Reset Password", command=self.open_find_dialog, style="TButton", width=18)
        self.close_button.grid(row=0, column=0, padx=90)

    def open_find_dialog(self):
        find_dialog = tk.Toplevel(self)
        find_dialog.title("Reset Password")
        find_dialog.geometry("200x120")
        find_dialog.iconbitmap('/MYBM/bank.ico')
        find_dialog.resizable(0,0)
        find_dialog.grab_set()

        tk.Label(find_dialog, text="Account Number :", font=("Times New Roman", 14), foreground='#499A51').pack(ipadx=13, anchor='w')

        self.account_number_entry = ttk.Entry(find_dialog, font=("Times New Roman", 16, 'bold'), foreground='#499A51', width=15)
        self.account_number_entry.pack(pady=5)
        self.account_number_entry.focus_set()
        
        find_button = ttk.Button(find_dialog, text="Reset", command=lambda: self.find_account(find_dialog))
        find_button.pack(pady=5)

        find_dialog.update_idletasks()
        window_width = find_dialog.winfo_width()
        window_height = find_dialog.winfo_height()
        screen_width = find_dialog.winfo_screenwidth()
        screen_height = find_dialog.winfo_screenheight()
        position_right = int((screen_width / 2) - (window_width / 2))
        position_down = int((screen_height / 2) - (window_height / 2))
        find_dialog.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")
    
    def find_account(self, dialog):
        self.account_number = self.account_number_entry.get()
        if not self.account_number:
            messagebox.showerror("Input Error", "Please enter an account number.")
            return
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM accounts WHERE account_number = {}".format(self.account_number))
            account = cursor.fetchone()
            if account:
                messagebox.showinfo("Success", "Account found.")
                dialog.destroy()
                self.open_reset_password_form(self.account_number)
            else:
                messagebox.showerror("Error", "Account not found.")
                self.account_number_entry.delete(0, tk.END)
                self.account_number_entry.focus_set()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        finally:
            cursor.close()
            conn.close()

    def open_reset_password_form(self, account_number):
        self.find_frame.destroy()
        
        self.reset_password_frame = ttk.Frame(self, padding=(560,10,0,0))
        self.reset_password_frame.grid(row=1, column=0, padx=5, pady=5, sticky='w')

        self.create_reset_password_fields(account_number)

        self.load_account_details()
        button_frame = ttk.Frame(self.reset_password_frame)
        button_frame.grid(row=10, column=0, columnspan=2, pady=10)

        reset_password_button = ttk.Button(button_frame, text="Reset", command=self.reset_password)
        reset_password_button.grid(row=0, column=0, padx=10)

        cancel_button = ttk.Button(button_frame, text="Cancel", command=self.refresh_page)
        cancel_button.grid(row=0, column=1, padx=10)
    
    def create_reset_password_fields(self, account_number):
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM accounts WHERE account_number = {}".format(account_number))
            account = cursor.fetchone()
            
            if account:
                ttk.Label(self.reset_password_frame, text="Account Number :", font=("Times New Roman", 14), foreground='#499A51').grid(row=0, column=0, sticky='w', padx=10, pady=5)
                self.account_number_entryf = ttk.Entry(self.reset_password_frame, font=("Times New Roman", 16, 'bold'), foreground='#499A51', state="readonly", width=30)
                self.account_number_entryf.grid(row=0, column=1, padx=10, pady=5)
                
                ttk.Label(self.reset_password_frame, text="Account Holder :", font=("Times New Roman", 14), foreground='#499A51').grid(row=1, column=0, sticky='w', padx=10, pady=5)
                self.account_holder_entry = ttk.Entry(self.reset_password_frame, font=("Times New Roman", 16, 'bold'), foreground='#499A51', state="readonly", width=30)
                self.account_holder_entry.grid(row=1, column=1, padx=10, pady=5)

                ttk.Label(self.reset_password_frame, text="Phone Number :", font=("Times New Roman", 14), foreground='#499A51').grid(row=2, column=0, sticky='w', padx=10, pady=5)
                self.phone_number_entry = ttk.Entry(self.reset_password_frame, font=("Times New Roman", 16, 'bold'), foreground='#499A51', state="readonly", width=30)
                self.phone_number_entry.grid(row=2, column=1, padx=10, pady=5)

                ttk.Label(self.reset_password_frame, text="Email :", font=("Times New Roman", 14), foreground='#499A51').grid(row=3, column=0, sticky='w', padx=10, pady=5)
                self.email_entry = ttk.Entry(self.reset_password_frame, font=("Times New Roman", 16, 'bold'), foreground='#499A51', state="readonly", width=30)
                self.email_entry.grid(row=3, column=1, padx=10, pady=5)

                ttk.Label(self.reset_password_frame, text="Username :", font=("Times New Roman", 14), foreground='#499A51').grid(row=4, column=0, sticky='w', padx=10, pady=5)
                self.username_entry = ttk.Entry(self.reset_password_frame, font=("Times New Roman", 16, 'bold'), foreground='#499A51', state="readonly", width=30)
                self.username_entry.grid(row=4, column=1, padx=10, pady=5)
                
                ttk.Label(self.reset_password_frame, text="Password :", font=("Times New Roman", 14), foreground='#499A51').grid(row=5, column=0, sticky='w', padx=10, pady=5)
                self.password_entry = ttk.Entry(self.reset_password_frame, font=("Times New Roman", 16, 'bold'), foreground='#499A51', width=30)
                self.password_entry.grid(row=5, column=1, padx=10, pady=5)
                
                ttk.Label(self.reset_password_frame, text="Confirm Password :", font=("Times New Roman", 14), foreground='#499A51').grid(row=6, column=0, sticky='w', padx=10, pady=5)
                self.confirm_password_entry = ttk.Entry(self.reset_password_frame, font=("Times New Roman", 16, 'bold'), foreground='#499A51', width=30)
                self.confirm_password_entry.grid(row=6, column=1, padx=10, pady=5)
                
                self.username = self.username_entry.get()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        finally:
            cursor.close()
            conn.close()
    
    def load_account_details(self):
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT first_name, middle_name, last_name, phone_number, email, username FROM accounts WHERE account_number = {}".format(self.account_number))
            account = cursor.fetchone()
            
            cursor.execute("SELECT username, password from users where username=\'{}\'".format(account[5]))
            password = cursor.fetchone()
            self.username=password[1]
            
            account_holder = account[0] + " " + account[1] + " " + account[2]
            
            self.account_number_entryf.config(state='normal')
            self.account_number_entryf.delete(0, tk.END)
            self.account_number_entryf.insert(0, str(self.account_number))
            self.account_number_entryf.config(state='readonly')
            
            self.account_holder_entry.config(state='normal')
            self.account_holder_entry.delete(0, tk.END)
            self.account_holder_entry.insert(0, str(account_holder))
            self.account_holder_entry.config(state='readonly')
            
            self.phone_number_entry.config(state='normal')
            self.phone_number_entry.delete(0, tk.END)
            self.phone_number_entry.insert(0, str(account[3]))
            self.phone_number_entry.config(state='readonly')
            
            self.email_entry.config(state='normal')
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, str(account[4]))
            self.email_entry.config(state='readonly')
            
            self.username_entry.config(state='normal')
            self.username_entry.delete(0, tk.END)
            self.username_entry.insert(0, str(account[5]))
            self.username_entry.config(state='readonly')
            
            self.password_entry.config(state='normal')
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, str(password[1]))
            self.password_entry.config(state='normal')
            
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))

    def reset_password(self):
        usrnm = self.username_entry.get()
        pwd = self.password_entry.get()
        cpwd = self.confirm_password_entry.get()
        
        if pwd == cpwd:
            try:
                conn = connect_to_db()
                cursor = conn.cursor()
                cursor.execute("SELECT username FROM users WHERE username = \'{}\'".format(usrnm))
                account = cursor.fetchone()
                if account:
                    cursor.execute("update users set password=\'{}\' where username=\'{}\'".format(pwd, usrnm))
                    conn.commit()
                    messagebox.showinfo("Success", "Password Reset Successfully.")
                    self.refresh_page()
                else:
                    messagebox.showerror("Error", "Account not found.")
                    self.account_number_entry.delete(0, tk.END)
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", str(err))
            finally:
                cursor.close()
                conn.close()
        else:
            messagebox.showerror("Password Mismatch", "Password didn't match\nTry again")
    
    def refresh_page(self):
        self.reset_password_frame.destroy()
        self.create_find_frame()
        self.title_label.grid(row=0, column=0, pady=10, sticky='w')    
    
        
        

#=================================================================================================================================================
#                                                                     USER PAGE                                                                  #
#=================================================================================================================================================  
class UserPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        # Title Panel
        title_panel = ttk.Frame(self, style='TitlePanel.TFrame', padding=(0, 20, 0, 20))
        title_panel.pack(side='top', fill='x')

        # Button Panel
        button_panel = ttk.Frame(self, style='ButtonPanel.TFrame', padding=(20, 12, 20, 10))
        button_panel.pack(side='left', fill='y')

        # Title Label
        title_label = ttk.Label(title_panel, text="USER DASHBOARD", background="#499A51", font=("Times New Roman", 32, 'bold'), foreground="#ffffff")
        title_label.pack(pady=10)

        # Balance Enquiry Button
        balance_enquiry_button = ttk.Button(button_panel, text="Balance Enquiry", command=self.balance_enquiry, style="Custom.TButton")
        balance_enquiry_button.pack(pady=10, fill="x")

        # Withdraw Button
        withdraw_button = ttk.Button(button_panel, text="Withdraw", command=self.withdraw, style="Custom.TButton")
        withdraw_button.pack(pady=10, fill="x")

        # Deposit Button
        deposit_button = ttk.Button(button_panel, text="Deposit", command=self.deposit, style="Custom.TButton")
        deposit_button.pack(pady=10, fill="x")

        # Account Statement Button
        account_statement_button = ttk.Button(button_panel, text="Account Statement", command=self.account_statement, style="Custom.TButton")
        account_statement_button.pack(pady=10, fill="x")

        # Transfer Button
        transfer_button = ttk.Button(button_panel, text="Transfer", command=self.transfer, style="Custom.TButton")
        transfer_button.pack(pady=10, fill="x")

        # Logout Button
        logout_button = ttk.Button(button_panel, text="Logout", command=self.logout, style="Custom.TButton")
        logout_button.pack(pady=10, fill="x")

        # Style configuration
        style = ttk.Style()
        style.configure('Custom.TButton',
                        font=("Times New Roman", 18, 'bold'),
                        foreground='#499A51',
                        background='#499A51',
                        padding=10)
        style.configure('TitlePanel.TFrame', background='#499A51')
        style.configure('ButtonPanel.TFrame', background='#499A51')

        # Content Area
        self.content_area = ttk.Frame(self)
        self.content_area.pack(side='right', fill='both', expand=True, padx=10, pady=10)

        
        # Initially show Balance Enquiry
        self.show_content(AccountDetailsPageUserDefault)

    def show_content(self, content):
        for widget in self.content_area.winfo_children():
            widget.destroy()

        if content is not None:
            content_frame = content(self.content_area, self.controller)
            content_frame.pack(fill="both", expand=True)

    def balance_enquiry(self):
        self.show_content(BalanceEnquiryPage)

    def withdraw(self):
        self.show_content(WithdrawPage)

    def deposit(self):
        self.show_content(DepositPage)

    def account_statement(self):
        self.show_content(AccountStatementPage)

    def transfer(self):
        self.show_content(TransferPage)

    def logout(self):
        login_page = self.controller.frames[LoginPage]
        login_page.reset_fields()
        self.controller.show_frame(LoginPage)
        print(f"{current_user} Logged Out")

#==================================================
#       ACCOUNT DETAILS PAGE FOR USER PAGE        #
#==================================================
class AccountDetailsPageUserDefault(ttk.Frame):
    def __init__(self, parent, c=None):
        super().__init__(parent)
        # self.controller = c
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        self.title_label = ttk.Label(self, text="Account Details", font=("Times New Roman", 24, 'bold'), foreground='#499A51', padding=(710,0,5,0))
        self.title_label.pack(pady=10, anchor='w')
        
        self.main_frame = ttk.Frame(self, padding=(570,0,0,0))
        self.main_frame.pack(padx=20, pady=20, fill='both', expand=True)

        self.create_account_details_fields()
        self.find_account()

    def create_account_details_fields(self):
        labels = ["First Name", "Middle Name", "Last Name", "Gender", "Phone Number", "Email", "Date of Birth", "Address", "Account Type"]
        self.entries = {}

        for i, label_text in enumerate(labels):
            row = i + 2
            ttk.Label(self.main_frame, text=f"{label_text} :", font=("Times New Roman", 14), foreground='#499A51').grid(row=row, column=0, sticky='w', padx=10, pady=5)
            entry = ttk.Entry(self.main_frame, font=("Times New Roman", 16, 'bold'), foreground='#499A51', width=25, state="readonly")
            entry.grid(row=row, column=1, padx=10, pady=5)
            self.entries[label_text] = entry

    def find_account(self):
        try:
            conn = connect_to_db() 
            cursor = conn.cursor()
            cursor.execute("SELECT first_name, middle_name, last_name, gender, phone_number, email, dob, address, account_type FROM accounts WHERE username = \'{}\'".format(get_customer()))
            account = cursor.fetchone()
            if account:
                self.display_account_details(account)
            else:
                messagebox.showerror("Error", "Account not found.")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        finally:
            cursor.close()

    def display_account_details(self, account):
        for key, entry in zip(self.entries.keys(), account):
            self.entries[key].config(state="normal")
            self.entries[key].delete(0, tk.END)
            self.entries[key].insert(0, entry)
            self.entries[key].config(state="readonly")

#====================================
#       BALANCE ENQUIRY PAGE        #
#====================================
class BalanceEnquiryPage(ttk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.title_label = ttk.Label(self, text="Balance Enquiry", font=("Times New Roman", 24, 'bold'), foreground='#499A51', padding=(710,0,5,0))
        self.title_label.pack(pady=10, anchor='w')

        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(padx=620, pady=10, fill='both', expand=True, anchor='w')

        current_balance_label = ttk.Label(self.main_frame, text="Current Balance:", font=("Times New Roman", 16), foreground='#499A51')
        current_balance_label.grid(row=0, column=0, padx=10, pady=10)
        self.current_balance_entry = ttk.Entry(self.main_frame, font=("Times New Roman", 16, 'bold'), foreground='#499A51', width=20, state="readonly")
        self.current_balance_entry.grid(row=0, column=1, padx=10, pady=10)

        self.fetch_and_display_balance()

        back_button = ttk.Button(self.main_frame, text="Back", command=self.go_back)
        back_button.grid(row=1, column=0, columnspan=2, pady=20)

    def fetch_and_display_balance(self):
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            query = "SELECT balance FROM accounts WHERE username = %s"
            cursor.execute(query, (get_customer(),))
            balance = cursor.fetchone()

            if balance:
                self.current_balance_entry.config(state="normal")
                self.current_balance_entry.delete(0, tk.END)
                self.current_balance_entry.insert(0, f"${balance[0]:.2f}")
                self.current_balance_entry.config(state="readonly")
            else:
                self.current_balance_entry.config(state="normal")
                self.current_balance_entry.delete(0, tk.END)
                self.current_balance_entry.config(state="readonly")
                messagebox.showerror("Error", "Account not found.")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        finally:
            cursor.close()
            conn.close()
            
    def show_content(self, content_class):
        for widget in self.winfo_children():
            widget.destroy()
        content_class(self).pack(fill="both", expand=True)

    def go_back(self):
        self.show_content(AccountDetailsPageUserDefault)

#====================================
#           WITHDRAW PAGE           #
#====================================
class WithdrawPage(ttk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()
        
    def setup_ui(self):
        self.title_label = ttk.Label(self, text="Withdraw", font=("Times New Roman", 24, 'bold'), foreground='#499A51', padding=(745,0,5,0))
        self.title_label.pack(pady=10, anchor='w')

        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(padx=620, pady=10, fill='both', expand=True, anchor='w')

        current_balance_label = ttk.Label(self.main_frame, text="Current Balance:", font=("Times New Roman", 16), foreground='#499A51')
        current_balance_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.current_balance_entry = ttk.Entry(self.main_frame, font=("Times New Roman", 16, 'bold'), foreground='#499A51', width=20, state="readonly")
        self.current_balance_entry.grid(row=0, column=1, padx=10, pady=10)

        withdraw_amount_label = ttk.Label(self.main_frame, text="Withdraw Amount:", font=("Times New Roman", 16), foreground='#499A51')
        withdraw_amount_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.withdraw_amount_entry = ttk.Entry(self.main_frame, font=("Times New Roman", 16, 'bold'), foreground='#499A51', width=20)
        self.withdraw_amount_entry.grid(row=1, column=1, padx=10, pady=10)
        self.withdraw_amount_entry.focus_set()
        
        back_button = ttk.Button(self.main_frame, text="Back", command=self.go_back)
        back_button.grid(row=2, column=0, pady=20, padx=30)

        submit_button = ttk.Button(self.main_frame, text="Submit", command=self.process_withdrawal)
        submit_button.grid(row=2, column=1, pady=20)

        self.fetch_and_display_balance()

    def fetch_and_display_balance(self):
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            query = "SELECT balance FROM accounts WHERE username = %s"
            cursor.execute(query, (get_customer(),))
            balance = cursor.fetchone()

            if balance:
                self.current_balance_entry.config(state="normal")
                self.current_balance_entry.delete(0, tk.END)
                self.current_balance_entry.insert(0, f"${balance[0]:.2f}")
                self.current_balance_entry.config(state="readonly")
            else:
                messagebox.showerror("Error", "Account not found.")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        finally:
            cursor.close()
            conn.close()

    def process_withdrawal(self):
        withdraw_amount = self.withdraw_amount_entry.get()
        if not withdraw_amount:
            messagebox.showerror("Input Error", "Please enter an amount to withdraw.")
            return
        try:
            try:
                withdraw_amount = float(withdraw_amount)
            except ValueError as err:
                messagebox.showerror("Input Error", "Withdraw amount must be a numeric value.")
                self.clear_entries()
                return
            
            if withdraw_amount <= 0:
                messagebox.showerror("Input Error", "Withdrawal amount must be greater than zero.")
                self.clear_entries()
                return

            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT account_number, balance FROM accounts WHERE username = %s", (get_customer(),))
            details = cursor.fetchone()
            account_number = details[0]
            balance = details[1]
            
            if details and withdraw_amount <= balance:
                update_query = "UPDATE accounts SET balance = balance - %s WHERE username = %s"
                cursor.execute(update_query, (withdraw_amount, get_customer()))
                conn.commit()
                messagebox.showinfo("Success", "Withdrawal successful.")
                self.fetch_and_display_balance()
                self.log_transaction(account_number, withdraw_amount, balance)
                self.clear_entries()
            else:
                messagebox.showerror("Insufficient Funds", "Insufficient balance for the withdrawal.")
                self.clear_entries()
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
            cursor.close()
            conn.close()
            
    def log_transaction(self, account_number, wa, source_balance):
        try:
            bal = float(source_balance)
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute(f"""insert into transaction_history 
                           (account_number, transaction_type, amount, balance_before, balance_after) 
                           values ({account_number}, 'Withdrawal', {wa:.2f}, {bal:.2f}, {(bal - wa):.2f})""")
            conn.commit()
            cursor.close()
            conn.close()
            print("Transaction Recorded Successfully")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
            self.clear_entries()
            cursor.close()
            conn.close()
                   
    def clear_entries(self):
        self.withdraw_amount_entry.delete(0, tk.END)
        self.withdraw_amount_entry.focus_set()
        
    def go_back(self):
        self.show_content(AccountDetailsPageUserDefault)

    def show_content(self, content_class):
        for widget in self.winfo_children():
            widget.destroy()
        content_class(self).pack(fill="both", expand=True)

#====================================
#           DEPOSIT PAGE            #
#====================================
class DepositPage(ttk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        self.title_label = ttk.Label(self, text="Deposit", font=("Times New Roman", 24, 'bold'), foreground='#499A51', padding=(755, 0, 5, 0))
        self.title_label.pack(pady=10, anchor='w')

        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(padx=620, pady=10, fill='both', expand=True, anchor='w')

        current_balance_label = ttk.Label(self.main_frame, text="Current Balance:", font=("Times New Roman", 16), foreground='#499A51')
        current_balance_label.grid(row=0, column=0, padx=10, pady=10)
        self.current_balance_entry = ttk.Entry(self.main_frame, font=("Times New Roman", 16, 'bold'), foreground='#499A51', width=20, state="readonly")
        self.current_balance_entry.grid(row=0, column=1, padx=10, pady=10)

        deposit_amount_label = ttk.Label(self.main_frame, text="Deposit Amount:", font=("Times New Roman", 16), foreground='#499A51')
        deposit_amount_label.grid(row=1, column=0, padx=10, pady=10)
        self.deposit_amount_entry = ttk.Entry(self.main_frame, font=("Times New Roman", 16, 'bold'), foreground='#499A51', width=20)
        self.deposit_amount_entry.grid(row=1, column=1, padx=10, pady=10)
        self.deposit_amount_entry.focus_set()
        
        back_button = ttk.Button(self.main_frame, text="Back", command=self.go_back)
        back_button.grid(row=2, column=0, pady=20)

        submit_button = ttk.Button(self.main_frame, text="Submit", command=self.process_deposit)
        submit_button.grid(row=2, column=1, pady=20)

        self.fetch_and_display_balance()

    def fetch_and_display_balance(self):
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            query = "SELECT account_number, balance FROM accounts WHERE username = %s"
            cursor.execute(query, (get_customer(),))
            details = cursor.fetchone()
            self.account_number = details[0]
            self.balance = details[1]
            
            if self.balance:
                self.current_balance_entry.config(state="normal")
                self.current_balance_entry.delete(0, tk.END)
                self.current_balance_entry.insert(0, f"${self.balance:.2f}")
                self.current_balance_entry.config(state="readonly")
            else:
                messagebox.showerror("Error", "Account not found.")
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
            cursor.close()
            conn.close()

    def process_deposit(self):
        deposit_amount = self.deposit_amount_entry.get()
        if not deposit_amount:
            messagebox.showerror("Input Error", "Please enter an amount to deposit.")
            return
        try:
            try:
                deposit_amount = float(deposit_amount)
            except ValueError as err:
                messagebox.showerror("Input Error", "Deposit amount must be a numeric value.")
                self.clear_entries()
                return
            
            if deposit_amount <= 0:
                messagebox.showerror("Input Error", "Deposit amount must be greater than zero.")
                self.clear_entries()
                return

            conn = connect_to_db()
            cursor = conn.cursor()
            update_query = "UPDATE accounts SET balance = balance + %s WHERE username = %s"
            cursor.execute(update_query, (deposit_amount, get_customer()))
            conn.commit()
            messagebox.showinfo("Success", "Deposit successful.")
            self.log_transaction(self.account_number, deposit_amount, self.balance)
            self.fetch_and_display_balance()
            self.clear_entries()
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
            self.clear_entries()
            cursor.close()
            conn.close()
            
    def log_transaction(self, account_number, da, source_balance):
        bal = float(source_balance)
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute(f"""insert into transaction_history 
                           (account_number, transaction_type, amount, balance_before, balance_after) 
                           values ({account_number}, 'Deposit', {da:.2f}, {bal:.2f}, {(bal + da):.2f})""")
            conn.commit()
            cursor.close()
            conn.close()
            print("Transaction Recorded Successfully")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
            self.clear_entries()
            cursor.close()
            conn.close()
            
    def clear_entries(self):
        self.deposit_amount_entry.delete(0, tk.END)
        self.deposit_amount_entry.focus_set()
        
    def go_back(self):
        self.show_content(AccountDetailsPageUserDefault)

    def show_content(self, content_class):
        for widget in self.winfo_children():
            widget.destroy()
        content_class(self).pack(fill="both", expand=True)

#====================================
#       ACCOUN STATEMENT PAGE       #
#====================================
class AccountStatementPage(ttk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style()
        style.configure('TLabel', font=("Times New Roman", 14), foreground="#499A51")
        style.configure('TButton', font=("Times New Roman", 18, 'bold'), foreground="#499A51")

        ttk.Label(self, text="Account Statement", style='TLabel', font=("Times New Roman", 24, 'bold')).pack(pady=20)

        filters_frame = ttk.Frame(self)
        filters_frame.pack(pady=10, padx=10, fill="x", anchor="center")

        from_date_frame = ttk.Frame(filters_frame, padding=(460, 0, 20, 0))
        from_date_frame.pack(side="left", padx=5, pady=5)
        ttk.Label(from_date_frame, text="From Date:", style='TLabel').pack(side="left", padx=10)
        self.from_date = DateEntry(from_date_frame, date_pattern='yyyy-mm-dd', width=20,
                                   background='#ffffff', foreground='#499A51',
                                   font=("Times New Roman", 14, 'bold'))
        self.from_date.pack(side="left", ipady=2)

        to_date_frame = ttk.Frame(filters_frame, padding=(0, 0, 20, 0))
        to_date_frame.pack(side="left", padx=5, pady=5)
        ttk.Label(to_date_frame, text="To Date:", style='TLabel').pack(side="left", padx=10)
        self.to_date = DateEntry(to_date_frame, date_pattern='yyyy-mm-dd', width=20,
                                 background='#ffffff', foreground='#499A51',
                                 font=("Times New Roman", 14, 'bold'))
        self.to_date.pack(side="left", ipady=2)

        button_frame = ttk.Frame(self, padding=(660, 0, 20, 0))
        button_frame.pack(pady=10, padx=10, fill="x", anchor="center")

        generate_statement_button = ttk.Button(button_frame, text="Generate Statement", command=self.generate_account_statement, style="TButton", width=20)
        generate_statement_button.pack(side="left", padx=10, pady=5)

    def generate_account_statement(self):
        from_date = self.from_date.get()
        to_date = self.to_date.get()

        if not from_date or not to_date:
            messagebox.showerror("Error", "Please select both From and To dates.")
            return

        account_number = self.get_user_account_number(current_user)
        print(account_number)
        
        if account_number:
            transactions = self.fetch_account_statement_data(account_number, from_date, to_date)
            
            if transactions:
                self.create_account_statement_pdf(transactions)
                messagebox.showinfo("Success", "Account statement has been generated successfully!")
            else:
                messagebox.showinfo("Info", "No transactions found for the selected date range.")
        else:
            messagebox.showerror("Error", "Failed to retrieve account details.")

    def get_user_account_number(self, user):
        conn = connect_to_db()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT account_number FROM accounts
        WHERE username = %s
        """
        cursor.execute(query, (user,))
        account = cursor.fetchone()

        cursor.close()
        conn.close()

        if account:
            return account['account_number']
        else:
            messagebox.showerror("Error", "No account found for the logged-in user.")
            return None

    def fetch_account_statement_data(self, account_number, from_date, to_date):
        conn = connect_to_db()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT transaction_id, transaction_date, transaction_time, transaction_type, 
               amount, balance_before, balance_after, description
        FROM transaction_history
        WHERE account_number = %s AND transaction_date BETWEEN %s AND %s
        ORDER BY transaction_date ASC
        """

        cursor.execute(query, (account_number, from_date, to_date))
        transactions = cursor.fetchall()

        cursor.close()
        conn.close()

        return transactions

    def create_account_statement_pdf(self, transactions):
        pdf_file = f"{current_user}.pdf"
        c = canvas.Canvas(pdf_file, pagesize=landscape(letter))
        width, height = landscape(letter)

        c.setFont("Times-Roman", 24)
        c.drawString(72, height - 72, "Account Statement")

        header = f"|{'Trans. ID':^12}|{'Date':^12}|{'Time':^12}|{'Type':^12}|{'Amount':^16}|{'Before':^16}|{'After':^16}|{'Description':^40}|"
        print(f"\n\nGenerated Account Statement of {current_user}:\n")
        print(header)
        c.setFont("Times-Roman", 12)
        c.drawString(72, height - 120, header)
        c.line(72, height - 122, width - 72, height - 122)

        y = height - 140 
        for transaction in transactions:
            transaction_time = str(transaction['transaction_time']) if transaction['transaction_time'] else "N/A"
            tid = transaction['transaction_id']
            tdate = str(transaction['transaction_date'])
            ttype = transaction['transaction_type']
            amt = transaction['amount']
            bb = transaction['balance_before']
            ba = transaction['balance_after']
            desc = str(transaction['description'])

            row = f"|{tid:^12}|{tdate:^12}|{transaction_time:^12}|{ttype:<12}|{amt:<16.2f}|{bb:<16.2f}|{ba:<16.2f}|{desc:<40}|"
            print(row)
            c.drawString(72, y, row)
            y -= 20

            if y < 72:
                c.showPage()
                c.setFont("Times-Roman", 12)
                c.drawString(72, height - 120, header)
                c.line(72, height - 122, width - 72, height - 122)
                y = height - 140

        c.save()
        print(f"PDF generated: {pdf_file}")

#====================================
#           TRANSFER PAGE           #
#====================================
class TransferPage(ttk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller
        
        self.title_label = ttk.Label(self, text="Transfer Amount", font=("Times New Roman", 24, 'bold'), foreground='#499A51', padding=(710, 0, 5, 0))
        self.title_label.pack(pady=10, anchor='w')
        
        self.setup_ui()
        self.destination_account_entry.focus_set()

    def setup_ui(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(padx=545, pady=10, fill='both', expand=True, anchor='w')

        self.source_balance_label = ttk.Label(self.main_frame, text="Your Current Balance :", font=("Times New Roman", 16), foreground='#499A51')
        self.source_balance_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.source_balance_entry = ttk.Entry(self.main_frame, font=("Times New Roman", 16, 'bold'), foreground='#499A51', width=25, state="readonly")
        self.source_balance_entry.grid(row=0, column=1, padx=10, pady=10)

        self.destination_account_label = ttk.Label(self.main_frame, text="Destination Account Number :", font=("Times New Roman", 16), foreground='#499A51')
        self.destination_account_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.destination_account_entry = ttk.Entry(self.main_frame, font=("Times New Roman", 16, 'bold'), foreground='#499A51', width=25)
        self.destination_account_entry.grid(row=1, column=1, padx=10, pady=10)
        
        self.back_button = ttk.Button(self.main_frame, text="Back", command=self.go_back)
        self.back_button.grid(row=3, column=0, pady=20)

        self.next_button = ttk.Button(self.main_frame, text="Next", command=self.after_account_found)
        self.next_button.grid(row=3, column=1, pady=20)

        self.fetch_and_display_balance()
        
    def after_account_found(self):
        destination_account = self.destination_account_entry.get()

        if not destination_account:
            messagebox.showerror("Input Error", "Please enter the destination account number.")
            self.destination_account_entry.focus_set()
            return
        try:
            conn = connect_to_db()
            cursor = conn.cursor()

            cursor.execute("SELECT first_name, middle_name, last_name, account_number FROM accounts WHERE account_number = %s", (destination_account,))
            details = cursor.fetchone()
            
            
            if details:
                self.receiver_name = details[0] + " " + details[1][0] + " " + details[2]
                # dest_account = details[3]
                self.show_transfer_fields()
            else:
                messagebox.showerror("Error", "Destination account not found.")
                self.destination_account_entry.delete(0, tk.END)
                self.destination_account_entry.focus_set()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        finally:
            cursor.close()
            conn.close()
    
    def show_transfer_fields(self):
        self.destination_account_entry.config(state="readonly")
        
        self.back_button.grid_forget()
        self.next_button.grid_forget()

        self.receiver_label = ttk.Label(self.main_frame, text="Receiver's Name :", font=("Times New Roman", 16), foreground='#499A51')
        self.receiver_label.grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.receiver_entry = ttk.Entry(self.main_frame, font=("Times New Roman", 16, 'bold'), foreground='#499A51', width=25)
        self.receiver_entry.grid(row=2, column=1, padx=10, pady=10)
        self.receiver_entry.insert(0,self.receiver_name)
        self.receiver_entry.config(state="readonly")
        
        self.transfer_amount_label = ttk.Label(self.main_frame, text="Amount to Transfer :", font=("Times New Roman", 16), foreground='#499A51')
        self.transfer_amount_label.grid(row=3, column=0, padx=10, pady=10, sticky='w')
        self.transfer_amount_entry = ttk.Entry(self.main_frame, font=("Times New Roman", 16, 'bold'), foreground='#499A51', width=25)
        self.transfer_amount_entry.grid(row=3, column=1, padx=10, pady=10)
        
        self.description_label = ttk.Label(self.main_frame, text="Description :", font=("Times New Roman", 16), foreground='#499A51')
        self.description_label.grid(row=4, column=0, padx=10, pady=10, sticky='w')
        self.description_entry = ttk.Entry(self.main_frame, font=("Times New Roman", 16, 'bold'), foreground='#499A51', width=25)
        self.description_entry.grid(row=4, column=1, padx=10, pady=10)
        
        self.confirm_button = ttk.Button(self.main_frame, text="Confirm", command=self.process_transfer)
        self.confirm_button.grid(row=5, column=1, pady=20)

        self.cancel_button = ttk.Button(self.main_frame, text="Cancel", command=self.cancel_transfer)
        self.cancel_button.grid(row=5, column=0, pady=20)
    
    def cancel_transfer(self):
        self.main_frame.destroy()
        self.setup_ui()
    
    def clear_entries_before(self):
        self.destination_account_entry.delete(0, tk.END)
        self.transfer_amount_entry.delete(0,tk.END)
        self.description_entry.delete(0,tk.END)
        self.destination_account_entry.focus_set()
    
    def clear_entries_after(self):
        self.destination_account_entry.delete(0, tk.END)
        self.transfer_amount_entry.delete(0,tk.END)
        self.description_entry.delete(0,tk.END)
        self.receiver_entry.delete(0,tk.END)
        self.source_balance_entry.delete(0,tk.END)
        self.destination_account_entry.focus_set()
    
    def fetch_and_display_balance(self):
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT balance FROM accounts WHERE username = \'{}\'".format(get_customer()))
            balance = cursor.fetchone()

            if balance:
                self.source_balance_entry.config(state="normal")
                self.source_balance_entry.delete(0, tk.END)
                self.source_balance_entry.insert(0, f"${balance[0]:.2f}")
                self.source_balance_entry.config(state="readonly")
            else:
                messagebox.showerror("Error", "Account not found.")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        finally:
            cursor.close()
            conn.close()

    def process_transfer(self):
        destination_account = self.destination_account_entry.get()
        transfer_amount = self.transfer_amount_entry.get()
        desc = self.description_entry.get()
            
        self.ta = 0
        self.da = 0
        
        if not destination_account or not transfer_amount:
            messagebox.showerror("Input Error", "Please enter both the destination account number and amount.")
            self.clear_entries_before()
            return
        
        try:
            self.da = float(destination_account)
        except ValueError:
            messagebox.showerror("Input Error", "Destination Account must be a numeric value.")
            self.clear_entries_before()
            return
        
        try:
            self.ta = float(transfer_amount)
        except ValueError:
            messagebox.showerror("Input Error", "Transfer amount must be a numeric value.")
            self.transfer_amount_entry.delete(0,tk.END)
            self.transfer_amount_entry.focus_set()
            return

        try:
            if self.ta <= 0:
                messagebox.showerror("Input Error", "Transfer amount must be greater than zero.")
                self.clear_entries_after()
                return

            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("SELECT account_number, balance FROM accounts WHERE username = \'{}\'".format(get_customer()))
            details = cursor.fetchone()
            account_number = details[0]
            source_balance = details[1]
            self.temp = 0
            # print(">", source_balance)
            # print(">", self.ta)
            # print(">", source_balance >= self.ta)
            if source_balance and float(source_balance) >= self.ta:
                self.temp = 1     
            
            if self.temp == 1:
                cursor.execute("SELECT account_number FROM accounts WHERE account_number = \'{}\'".format(self.da))
                dest_account = cursor.fetchone()
                if dest_account:
                    cursor.execute("UPDATE accounts SET balance = balance - {} WHERE username = \'{}\'".format(self.ta, get_customer()))
                    cursor.execute("UPDATE accounts SET balance = balance + {} WHERE account_number = {}".format(self.ta, self.da))
                    conn.commit()
                    self.fetch_and_display_balance()
                    messagebox.showinfo("Success", "Transfer successful.")
                    self.log_transaction(account_number, self.ta, source_balance, self.da, desc)
                    self.clear_entries_after()
                    self.cancel_transfer()
                else:
                    messagebox.showerror("Error", "Destination account not found.")
                    self.clear_entries_after()
            else:
                messagebox.showerror("Insufficient Funds", "Insufficient balance for the transfer.")
                self.clear_entries_after()
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
            self.clear_entries_after()
            cursor.close()
            conn.close()

    def log_transaction(self, account_number, ta, source_balance, da, desc):
        bal = float(source_balance)
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute(f"""insert into transaction_history 
                           (account_number, transaction_type, amount, balance_before, balance_after, target_account_number, description) 
                           values ({account_number}, 'Transfer', {ta}, {bal:.2f}, {(bal - ta):.2f}, {da:.2f}, \'{desc}\')""")
            conn.commit()
            cursor.close()
            conn.close()
            print("Transaction Recorded Successfully")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
            self.clear_entries_after()
            cursor.close()
            conn.close()
            
    def go_back(self):
        self.show_content(AccountDetailsPageUserDefault)

    def show_content(self, content_class):
        for widget in self.winfo_children():
            widget.destroy()
        content_class(self).pack(fill="both", expand=True)







#=================================================================================================================================================
#                                                                     MAIN PAGE                                                                  #
#=================================================================================================================================================  
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()