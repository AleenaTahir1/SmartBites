import customtkinter as ctk
from gui.constants import *
from gui.login_page import LoginPage
from gui.signup_page import SignupPage
from gui.forgot_password_page import ForgotPasswordPage
from gui.home_page import HomePage
from gui.orders_page import OrdersPage
from gui.menu_management_page import MenuManagementPage
from gui.user_management_page import UserManagementPage
from gui.reports_page import ReportsPage
from gui.settings_page import SettingsPage

class SmartBitesApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("SmartBites")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(800, 600)
        
        # Set theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Initialize pages dictionary
        self.pages = {
            "LoginPage": LoginPage,
            "SignupPage": SignupPage,
            "ForgotPasswordPage": ForgotPasswordPage,
            "HomePage": HomePage,
            "OrdersPage": OrdersPage,
            "MenuManagementPage": MenuManagementPage,
            "UserManagementPage": UserManagementPage,
            "ReportsPage": ReportsPage,
            "SettingsPage": SettingsPage
        }
        
        # Create and add pages
        for page_name, Page in self.pages.items():  
            frame = Page(parent=self, controller=self)
            self.pages[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        # Show initial page
        self.show_page("LoginPage")
        
        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
    def show_page(self, page_name):
        """Show a frame for the given page name"""
        page = self.pages[page_name]
        page.tkraise()

    def show_login_page(self):
        self.show_page("LoginPage")

    def show_signup_page(self):
        self.show_page("SignupPage")

    def show_home_page(self):
        self.show_page("HomePage")
        
    def show_orders_page(self):
        self.show_page("OrdersPage")
        
    def show_menu_management_page(self):
        self.show_page("MenuManagementPage")
        
    def show_user_management_page(self):
        self.show_page("UserManagementPage")
        
    def show_reports_page(self):
        self.show_page("ReportsPage")
        
    def show_settings_page(self):
        self.show_page("SettingsPage")

    def show_cart_page(self):
        # This will be implemented when we create the cart page
        pass

    def show_order_status_page(self):
        # This will be implemented when we create the order status page
        pass

if __name__ == "__main__":
    app = SmartBitesApp()
    app.mainloop()
