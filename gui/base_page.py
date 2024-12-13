import customtkinter as ctk
from gui.constants import *

class BasePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
    def show(self):
        """Show this page"""
        if hasattr(self.controller, 'current_page'):
            if self.controller.current_page:
                self.controller.current_page.grid_forget()
        self.grid(row=0, column=0, sticky="nsew")
        self.controller.current_page = self
        
    def hide(self):
        """Hide this page"""
        self.grid_forget()
