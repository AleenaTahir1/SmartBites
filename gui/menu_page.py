import customtkinter as ctk
from PIL import Image
from .base_page import BasePage
from .constants import *
import os

class MenuPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.configure(fg_color=BG_COLOR)
        
        # Create main container
        self.container = ctk.CTkFrame(
            self,
            fg_color=BG_COLOR,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT
        )
        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.grid_columnconfigure(0, weight=1)
        
        # Header Frame
        self.header_frame = ctk.CTkFrame(
            self.container,
            fg_color=PRIMARY_COLOR,
            height=80
        )
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        
        # Logo in header
        self.logo_label = ctk.CTkLabel(
            self.header_frame,
            text="SmartBites",
            font=ctk.CTkFont(family=LOGO_FONT, size=24, weight="bold"),
            text_color="white"
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=20)
        
        # Content Frame
        self.content_frame = ctk.CTkFrame(
            self.container,
            fg_color=BG_COLOR
        )
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=1)
        
        # Menu Categories
        categories = [
            ("Today's Special", "special.png"),
            ("Main Course", "main.png"),
            ("Appetizers", "appetizer.png"),
            ("Desserts", "dessert.png"),
            ("Beverages", "beverage.png"),
            ("My Orders", "orders.png")
        ]
        
        # Create menu category buttons
        for idx, (category, icon_name) in enumerate(categories):
            row = idx // 2
            col = idx % 2
            
            # Category Frame
            category_frame = ctk.CTkFrame(
                self.content_frame,
                fg_color=SECONDARY_COLOR,
                corner_radius=15
            )
            category_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            # Try to load icon if exists
            icon_path = os.path.join("assets", icon_name)
            if os.path.exists(icon_path):
                icon = ctk.CTkImage(
                    light_image=Image.open(icon_path),
                    dark_image=Image.open(icon_path),
                    size=(64, 64)
                )
            else:
                icon = None
            
            # Category Button
            category_btn = ctk.CTkButton(
                category_frame,
                text=category,
                font=ctk.CTkFont(size=16),
                image=icon if icon else None,
                compound="top",
                fg_color="transparent",
                hover_color=PRIMARY_COLOR,
                corner_radius=15,
                command=lambda cat=category: self.show_category(cat)
            )
            category_btn.pack(padx=20, pady=20, expand=True, fill="both")
            
        # Profile button in header
        self.profile_btn = ctk.CTkButton(
            self.header_frame,
            text="Profile",
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            hover_color=SECONDARY_COLOR,
            command=self.show_profile
        )
        self.profile_btn.grid(row=0, column=1, padx=20, sticky="e")
        
    def show_category(self, category):
        # This will be implemented later when connecting to backend
        print(f"Selected category: {category}")
        
    def show_profile(self):
        # This will navigate to profile page when implemented
        print("Navigate to profile")
