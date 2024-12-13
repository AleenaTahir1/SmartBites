import customtkinter as ctk
from .admin_base_page import AdminBasePage
from .constants import *

class ReportsPage(AdminBasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        # Set active button
        self.set_active_button("Reports")
        
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
            text="Reports & Analytics",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        ).pack(side="left", padx=20)
        
        # Export button
        self.export_btn = ctk.CTkButton(
            self.header,
            text="Export Report",
            font=ctk.CTkFont(size=14),
            fg_color=SECONDARY_COLOR,
            hover_color="#2A8572"
        )
        self.export_btn.pack(side="right", padx=20)
        
        # Main content
        self.content = ctk.CTkFrame(self.content_area, fg_color=BG_COLOR)
        self.content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Time period selector
        self.period_frame = ctk.CTkFrame(self.content, fg_color="white")
        self.period_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            self.period_frame,
            text="Time Period:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10, pady=10)
        
        self.period_menu = ctk.CTkOptionMenu(
            self.period_frame,
            values=["Today", "This Week", "This Month", "Last 3 Months", "Custom"],
            fg_color=PRIMARY_COLOR,
            button_color=PRIMARY_COLOR
        )
        self.period_menu.pack(side="left", padx=10, pady=10)
        
        # Key metrics
        self.metrics_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        self.metrics_frame.pack(fill="x", pady=(0, 20))
        
        metrics = [
            ("Total Revenue", "$45,678", "+12.5%", "#e6ffe6"),
            ("Total Orders", "1,234", "+8.3%", "#e6f3ff"),
            ("Average Order Value", "$37.02", "+5.2%", "#ffe6e6"),
            ("Active Users", "890", "+15.7%", "#e6fff9")
        ]
        
        for title, value, change, color in metrics:
            card = ctk.CTkFrame(self.metrics_frame, fg_color=color)
            card.pack(side="left", padx=5, fill="x", expand=True)
            
            ctk.CTkLabel(
                card,
                text=title,
                font=ctk.CTkFont(size=14)
            ).pack(pady=(10, 5))
            
            ctk.CTkLabel(
                card,
                text=value,
                font=ctk.CTkFont(size=24, weight="bold")
            ).pack(pady=(0, 5))
            
            ctk.CTkLabel(
                card,
                text=change,
                font=ctk.CTkFont(size=12),
                text_color="green"
            ).pack(pady=(0, 10))
        
        # Reports sections
        reports_sections = [
            ("Top Selling Items", [
                ("Spicy Chicken Burger", "234 orders", "$2,808"),
                ("Caesar Salad", "156 orders", "$1,404"),
                ("Chocolate Brownie", "145 orders", "$870"),
                ("Iced Latte", "123 orders", "$615")
            ]),
            ("Customer Demographics", [
                ("New Customers", "45%", ""),
                ("Returning Customers", "55%", ""),
                ("Premium Members", "15%", ""),
                ("Regular Members", "85%", "")
            ]),
            ("Order Statistics", [
                ("Completed Orders", "92%", "1,135 orders"),
                ("Cancelled Orders", "3%", "37 orders"),
                ("Processing Orders", "5%", "62 orders")
            ])
        ]
        
        # Create report sections
        for title, items in reports_sections:
            section = ctk.CTkFrame(self.content, fg_color="white")
            section.pack(fill="x", pady=10)
            
            # Section header
            ctk.CTkLabel(
                section,
                text=title,
                font=ctk.CTkFont(size=16, weight="bold")
            ).pack(anchor="w", padx=15, pady=10)
            
            # Section content
            for item in items:
                item_frame = ctk.CTkFrame(section, fg_color="transparent")
                item_frame.pack(fill="x", padx=15, pady=5)
                
                ctk.CTkLabel(
                    item_frame,
                    text=item[0],
                    font=ctk.CTkFont(size=12)
                ).pack(side="left")
                
                ctk.CTkLabel(
                    item_frame,
                    text=item[1],
                    font=ctk.CTkFont(size=12, weight="bold")
                ).pack(side="right", padx=(0, 10))
                
                if item[2]:
                    ctk.CTkLabel(
                        item_frame,
                        text=item[2],
                        font=ctk.CTkFont(size=12),
                        text_color="gray"
                    ).pack(side="right", padx=10)
