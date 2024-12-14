import customtkinter as ctk
from gui.login_page import LoginPage
from gui.home_page import HomePage
from gui.menu_page import MenuPage
from gui.orders_page import OrdersPage
from gui.reports_page import ReportsPage
from gui.settings_page import SettingsPage
from gui.user_management_page import UserManagementPage
from gui.menu_management_page import MenuManagementPage
from gui.signup_page import SignupPage
from gui.forgot_password_page import ForgotPasswordPage
from database.init_db import init_database

class SmartBitesApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Initialize database
        init_database()

        # Configure window
        self.title("SmartBites")
        self.geometry(f"{1200}x{800}")
        self.minsize(800, 600)

        # Initialize current user
        self.current_user = None

        # Set theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create container
        container = ctk.CTkFrame(self)
        container.grid(row=0, column=0, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Dictionary to store frames
        self.frames = {}

        # Create frames
        for F in (LoginPage, HomePage, MenuPage, OrdersPage, ReportsPage, 
                 SettingsPage, UserManagementPage, MenuManagementPage,
                 SignupPage, ForgotPasswordPage):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show login page
        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if hasattr(frame, 'reset_form'):
            frame.reset_form()

    def show_page(self, page_name):
        self.show_frame(page_name)

    def show_home_page(self):
        self.show_frame("HomePage")

    def logout(self):
        self.current_user = None
        self.show_frame("LoginPage")

    def show_login_page(self):
        self.show_frame("LoginPage")

    def show_signup_page(self):
        self.show_frame("SignupPage")

    def show_orders_page(self):
        self.show_frame("OrdersPage")

    def show_menu_management_page(self):
        self.show_frame("MenuManagementPage")

    def show_user_management_page(self):
        self.show_frame("UserManagementPage")

    def show_reports_page(self):
        self.show_frame("ReportsPage")

    def show_settings_page(self):
        self.show_frame("SettingsPage")

    def show_cart_page(self):
        # This will be implemented when we create the cart page
        pass

    def show_order_status_page(self):
        # This will be implemented when we create the order status page
        pass

if __name__ == "__main__":
    app = SmartBitesApp()
    app.mainloop()
