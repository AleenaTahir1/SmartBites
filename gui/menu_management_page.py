import customtkinter as ctk
from .admin_base_page import AdminBasePage
from .constants import *

class MenuManagementPage(AdminBasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        # Set active button
        self.set_active_button("Menu Management")
        
        # Header
        self.header = ctk.CTkFrame(
            self.content_area,
            fg_color=PRIMARY_COLOR,
            height=60,
            corner_radius=10
        )
        self.header.pack(fill="x", padx=0, pady=(0, 20))
        
        # Add Menu Item button
        self.add_item_btn = ctk.CTkButton(
            self.header,
            text="+ Add Menu Item",
            font=ctk.CTkFont(size=14),
            fg_color=SECONDARY_COLOR,
            hover_color="#2A8572"
        )
        self.add_item_btn.pack(side="right", padx=20)
        
        # Main content
        self.main_content = ctk.CTkFrame(self.content_area, fg_color=BG_COLOR)
        self.main_content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Filters and search
        self.filters_frame = ctk.CTkFrame(self.main_content, fg_color="white")
        self.filters_frame.pack(fill="x", pady=(0, 20))
        
        # Category filter
        ctk.CTkLabel(
            self.filters_frame,
            text="Category:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10, pady=10)
        
        self.category_menu = ctk.CTkOptionMenu(
            self.filters_frame,
            values=["All", "Main Course", "Appetizers", "Desserts", "Beverages"],
            fg_color=PRIMARY_COLOR,
            button_color=PRIMARY_COLOR
        )
        self.category_menu.pack(side="left", padx=10, pady=10)
        
        # Search bar
        self.search_entry = ctk.CTkEntry(
            self.filters_frame,
            placeholder_text="Search menu items...",
            width=200
        )
        self.search_entry.pack(side="right", padx=10, pady=10)
        
        # Menu items grid
        self.grid_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        self.grid_frame.pack(fill="both", expand=True)
        
        # Dummy menu items
        menu_items = [
            {
                "name": "Spicy Chicken Burger",
                "category": "Main Course",
                "price": "$12.99",
                "status": "Available"
            },
            {
                "name": "Caesar Salad",
                "category": "Appetizers",
                "price": "$8.99",
                "status": "Available"
            },
            {
                "name": "Chocolate Brownie",
                "category": "Desserts",
                "price": "$6.99",
                "status": "Out of Stock"
            },
            {
                "name": "Iced Latte",
                "category": "Beverages",
                "price": "$4.99",
                "status": "Available"
            }
        ]
        
        # Create menu item cards
        for i, item in enumerate(menu_items):
            row = i // 2
            col = i % 2
            
            card = ctk.CTkFrame(self.grid_frame, fg_color="white")
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            # Item image placeholder
            img_placeholder = ctk.CTkFrame(
                card,
                fg_color="#E0E0E0",
                width=150,
                height=150
            )
            img_placeholder.pack(padx=10, pady=10)
            
            ctk.CTkLabel(
                img_placeholder,
                text="🍽️",
                font=ctk.CTkFont(size=48)
            ).place(relx=0.5, rely=0.5, anchor="center")
            
            # Item details
            ctk.CTkLabel(
                card,
                text=item["name"],
                font=ctk.CTkFont(size=16, weight="bold")
            ).pack(pady=5)
            
            ctk.CTkLabel(
                card,
                text=item["category"],
                font=ctk.CTkFont(size=12),
                text_color="gray"
            ).pack()
            
            ctk.CTkLabel(
                card,
                text=item["price"],
                font=ctk.CTkFont(size=14, weight="bold")
            ).pack(pady=5)
            
            status_color = "#32CD32" if item["status"] == "Available" else "#DC143C"
            ctk.CTkLabel(
                card,
                text=item["status"],
                font=ctk.CTkFont(size=12),
                fg_color=status_color,
                corner_radius=5,
                text_color="white"
            ).pack(pady=5)
            
            # Action buttons
            buttons_frame = ctk.CTkFrame(card, fg_color="transparent")
            buttons_frame.pack(pady=10)
            
            ctk.CTkButton(
                buttons_frame,
                text="Edit",
                font=ctk.CTkFont(size=12),
                fg_color=PRIMARY_COLOR,
                hover_color=SECONDARY_COLOR,
                width=60
            ).pack(side="left", padx=5)
            
            ctk.CTkButton(
                buttons_frame,
                text="Delete",
                font=ctk.CTkFont(size=12),
                fg_color="#DC143C",
                hover_color="#B22222",
                width=60
            ).pack(side="left", padx=5)
        
        # Configure grid weights
        self.grid_frame.grid_columnconfigure(0, weight=1)
        self.grid_frame.grid_columnconfigure(1, weight=1)
