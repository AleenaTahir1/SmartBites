import customtkinter as ctk
from gui.constants import *
from gui.login_page import LoginPage
from gui.signup_page import SignupPage
from gui.forgot_password_page import ForgotPasswordPage

class SmartBitesApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("SmartBites")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(800, 500)
        
        # Set theme
        ctk.set_appearance_mode("light")  # Changed to light mode for better visibility
        ctk.set_default_color_theme("blue")

        # Initialize pages dictionary
        self.pages = {
            "LoginPage": LoginPage,
            "SignupPage": SignupPage,
            "ForgotPasswordPage": ForgotPasswordPage
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
        if hasattr(self, 'login_page'):
            self.login_page.show()

    def show_signup_page(self):
        self.show_page("SignupPage")

    def show_menu_page(self):
        # This will be implemented when we create the menu page
        pass

    def show_cart_page(self):
        # This will be implemented when we create the cart page
        pass

    def show_order_status_page(self):
        # This will be implemented when we create the order status page
        pass

if __name__ == "__main__":
    app = SmartBitesApp()
    app.mainloop()
