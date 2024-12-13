import customtkinter as ctk
from .admin_base_page import AdminBasePage
from .constants import *

class OrdersPage(AdminBasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        # Set active button
        self.set_active_button("Orders")
        
        # Header
        self.header = ctk.CTkFrame(
            self.content_area,
            fg_color=PRIMARY_COLOR,
            height=60,
            corner_radius=10
        )
        self.header.pack(fill="x", padx=0, pady=(0, 20))
        
        ctk.CTkLabel(
            self.header,
            text="Orders Management",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        ).pack(side="left", padx=20, pady=10)
        
        # Main content
        self.content = ctk.CTkFrame(self.content_area, fg_color=BG_COLOR)
        self.content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Filters frame
        self.filters_frame = ctk.CTkFrame(self.content, fg_color="white")
        self.filters_frame.pack(fill="x", pady=(0, 20))
        
        # Status filter
        self.status_var = ctk.StringVar(value="All")
        status_options = ["All", "Pending", "Processing", "Completed", "Cancelled"]
        
        ctk.CTkLabel(
            self.filters_frame,
            text="Status:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10, pady=10)
        
        self.status_menu = ctk.CTkOptionMenu(
            self.filters_frame,
            values=status_options,
            variable=self.status_var,
            fg_color=PRIMARY_COLOR,
            button_color=PRIMARY_COLOR
        )
        self.status_menu.pack(side="left", padx=10, pady=10)
        
        # Date filter
        ctk.CTkLabel(
            self.filters_frame,
            text="Date Range:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10, pady=10)
        
        self.date_menu = ctk.CTkOptionMenu(
            self.filters_frame,
            values=["Today", "Last 7 days", "Last 30 days", "Custom"],
            fg_color=PRIMARY_COLOR,
            button_color=PRIMARY_COLOR
        )
        self.date_menu.pack(side="left", padx=10, pady=10)
        
        # Search bar
        self.search_entry = ctk.CTkEntry(
            self.filters_frame,
            placeholder_text="Search orders...",
            width=200
        )
        self.search_entry.pack(side="right", padx=10, pady=10)
        
        # Orders table
        self.table_frame = ctk.CTkFrame(self.content, fg_color="white")
        self.table_frame.pack(fill="both", expand=True)
        
        # Table header
        headers = ["Order ID", "Customer", "Items", "Total", "Status", "Date", "Actions"]
        header_frame = ctk.CTkFrame(self.table_frame, fg_color=PRIMARY_COLOR)
        header_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        for header in headers:
            ctk.CTkLabel(
                header_frame,
                text=header,
                font=ctk.CTkFont(weight="bold"),
                text_color="white"
            ).pack(side="left", expand=True, padx=10, pady=5)
        
        # Dummy orders data
        orders = [
            ["#12345", "John Doe", "2 items", "$25.00", "Pending", "2024-12-13", "View"],
            ["#12344", "Jane Smith", "1 item", "$15.50", "Processing", "2024-12-13", "View"],
            ["#12343", "Bob Wilson", "3 items", "$45.00", "Completed", "2024-12-12", "View"],
            ["#12342", "Alice Brown", "4 items", "$60.00", "Cancelled", "2024-12-12", "View"],
            ["#12341", "Charlie Davis", "2 items", "$30.00", "Completed", "2024-12-11", "View"],
        ]
        
        # Add orders to table
        for order in orders:
            row_frame = ctk.CTkFrame(self.table_frame, fg_color="transparent")
            row_frame.pack(fill="x", padx=10, pady=5)
            
            for i, item in enumerate(order):
                if i == 4:  # Status column
                    status_color = {
                        "Pending": "#FFA500",
                        "Processing": "#4169E1",
                        "Completed": "#32CD32",
                        "Cancelled": "#DC143C"
                    }.get(item, "gray")
                    
                    status_label = ctk.CTkLabel(
                        row_frame,
                        text=item,
                        font=ctk.CTkFont(size=12),
                        fg_color=status_color,
                        corner_radius=5,
                        text_color="white"
                    )
                    status_label.pack(side="left", expand=True, padx=10)
                elif i == 6:  # Actions column
                    view_btn = ctk.CTkButton(
                        row_frame,
                        text="View",
                        font=ctk.CTkFont(size=12),
                        fg_color=PRIMARY_COLOR,
                        hover_color=SECONDARY_COLOR,
                        width=60,
                        height=24
                    )
                    view_btn.pack(side="left", expand=True, padx=10)
                else:
                    ctk.CTkLabel(
                        row_frame,
                        text=item,
                        font=ctk.CTkFont(size=12)
                    ).pack(side="left", expand=True, padx=10)
        
        # Pagination
        self.pagination_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        self.pagination_frame.pack(fill="x", pady=20)
        
        ctk.CTkButton(
            self.pagination_frame,
            text="Previous",
            fg_color=PRIMARY_COLOR,
            hover_color=SECONDARY_COLOR,
            width=80
        ).pack(side="left", padx=5)
        
        for i in range(1, 6):
            ctk.CTkButton(
                self.pagination_frame,
                text=str(i),
                fg_color=PRIMARY_COLOR if i == 1 else "transparent",
                hover_color=SECONDARY_COLOR,
                text_color="white" if i == 1 else "black",
                width=40
            ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            self.pagination_frame,
            text="Next",
            fg_color=PRIMARY_COLOR,
            hover_color=SECONDARY_COLOR,
            width=80
        ).pack(side="left", padx=5)
