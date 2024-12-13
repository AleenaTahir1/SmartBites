import customtkinter as ctk
from .base_page import BasePage
from .constants import *

class AdminBasePage(BasePage):
    SIDEBAR_WIDTH = 280
    BUTTON_HEIGHT = 40
    BUTTON_CORNER_RADIUS = 8
    PROFILE_BG_COLOR = "#424949"  # Dark gray for profile section
    ACTIVE_BUTTON_COLOR = "#515A5A"  # Slightly lighter gray for active button
    HOVER_COLOR = "#424949"  # Same as profile background for consistency

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.configure(fg_color=BG_COLOR)
        
        # Create main container with grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_rowconfigure(0, weight=1)
        
        # Create side navigation bar
        self.sidebar = ctk.CTkFrame(
            self,
            fg_color=PRIMARY_COLOR,
            width=self.SIDEBAR_WIDTH,
            height=800,
            corner_radius=0
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        self.sidebar.pack_propagate(False)
        
        # Profile section container
        self.profile_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color=self.PROFILE_BG_COLOR,
            width=self.SIDEBAR_WIDTH,
            height=180,
            corner_radius=15
        )
        self.profile_frame.pack(pady=(20, 15), padx=15)
        self.profile_frame.pack_propagate(False)
        
        # Profile image with circular background
        self.profile_bg = ctk.CTkFrame(
            self.profile_frame,
            fg_color="#E5E7E9",  # Light gray for profile circle
            width=60,
            height=60,
            corner_radius=30
        )
        self.profile_bg.place(relx=0.5, rely=0.25, anchor="center")
        self.profile_bg.pack_propagate(False)
        
        self.profile_image = ctk.CTkLabel(
            self.profile_bg,
            text="👤",
            font=ctk.CTkFont(size=30),
            text_color="#424949"  # Dark gray for icon
        )
        self.profile_image.place(relx=0.5, rely=0.5, anchor="center")
        
        # Admin info container
        self.admin_info = ctk.CTkFrame(
            self.profile_frame,
            fg_color="transparent"
        )
        self.admin_info.place(relx=0.5, rely=0.7, anchor="center")
        
        self.admin_label = ctk.CTkLabel(
            self.admin_info,
            text="Administrator",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white"
        )
        self.admin_label.pack()
        
        self.location_label = ctk.CTkLabel(
            self.admin_info,
            text="Branch Location",
            font=ctk.CTkFont(size=12),
            text_color="#D5D8DC"  # Light gray for secondary text
        )
        self.location_label.pack()
        
        self.location_value = ctk.CTkLabel(
            self.admin_info,
            text="Jl Daeng Barat",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white"
        )
        self.location_value.pack()
        
        # Navigation container
        self.nav_container = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent",
            width=self.SIDEBAR_WIDTH
        )
        self.nav_container.pack(fill="both", expand=True, pady=(10, 0))
        
        # Navigation buttons
        nav_buttons = [
            ("Dashboard", "🏠", self.show_dashboard),
            ("Orders", "📋", self.show_orders),
            ("Menu Management", "🍽", self.show_menu_management),
            ("User Management", "👥", self.show_user_management),
            ("Reports", "📊", self.show_reports),
            ("Settings", "⚙️", self.show_settings),
        ]
        
        self.nav_buttons = {}
        
        for text, icon, command in nav_buttons:
            button_frame = ctk.CTkFrame(
                self.nav_container,
                fg_color="transparent",
                width=self.SIDEBAR_WIDTH - 30,
                height=self.BUTTON_HEIGHT + 10
            )
            button_frame.pack(pady=3)
            button_frame.pack_propagate(False)
            
            btn = ctk.CTkButton(
                button_frame,
                text=f"{icon} {text}",  # Added a single space between icon and text
                font=ctk.CTkFont(size=15),
                fg_color="transparent",
                text_color="white",
                hover_color=self.HOVER_COLOR,
                anchor="w",
                height=self.BUTTON_HEIGHT,
                width=self.SIDEBAR_WIDTH - 30,
                corner_radius=self.BUTTON_CORNER_RADIUS,
                command=command
            )
            btn.place(relx=0.5, rely=0.5, anchor="center")
            self.nav_buttons[text] = btn
        
        # Bottom frame for logout
        self.bottom_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent",
            width=self.SIDEBAR_WIDTH,
            height=80
        )
        self.bottom_frame.pack(fill="x", pady=20)
        self.bottom_frame.pack_propagate(False)
        
        # Separator above logout
        self.separator = ctk.CTkFrame(
            self.bottom_frame,
            fg_color="#D5D8DC",  # Light gray for separator
            height=1
        )
        self.separator.pack(fill="x", padx=15, pady=(0, 15))
        
        # Logout button
        self.logout_btn = ctk.CTkButton(
            self.bottom_frame,
            text="🚪 Log Out",
            font=ctk.CTkFont(size=15),
            fg_color="#DC143C",  # Original red color
            hover_color="#B22222",  # Original hover color
            height=self.BUTTON_HEIGHT,
            width=self.SIDEBAR_WIDTH - 30,
            corner_radius=self.BUTTON_CORNER_RADIUS,
            command=self.logout
        )
        self.logout_btn.pack(padx=15)
        
        # Content area
        self.content_area = ctk.CTkFrame(
            self,
            fg_color=BG_COLOR,
            corner_radius=15
        )
        self.content_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.content_area.grid_columnconfigure(0, weight=1)
        self.content_area.grid_rowconfigure(1, weight=1)
    
    def set_active_button(self, active_text):
        """Set the active state of navigation buttons"""
        for text, btn in self.nav_buttons.items():
            if text == active_text:
                btn.configure(
                    fg_color=self.ACTIVE_BUTTON_COLOR,
                    hover_color=self.ACTIVE_BUTTON_COLOR
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    hover_color=self.HOVER_COLOR
                )
    
    def show_dashboard(self):
        self.controller.show_home_page()
        self.set_active_button("Dashboard")
    
    def show_orders(self):
        self.controller.show_orders_page()
        self.set_active_button("Orders")
    
    def show_menu_management(self):
        self.controller.show_menu_management_page()
        self.set_active_button("Menu Management")
    
    def show_user_management(self):
        self.controller.show_user_management_page()
        self.set_active_button("User Management")
    
    def show_reports(self):
        self.controller.show_reports_page()
        self.set_active_button("Reports")
    
    def show_settings(self):
        self.controller.show_settings_page()
        self.set_active_button("Settings")
    
    def logout(self):
        self.controller.show_login_page()
