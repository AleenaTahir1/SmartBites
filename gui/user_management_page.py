import customtkinter as ctk
from .admin_base_page import AdminBasePage
from .constants import *

class UserManagementPage(AdminBasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        # Set active button
        self.set_active_button("User Management")
        
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
            text="User Management",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        ).pack(side="left", padx=20)
        
        # Add User button
        self.add_user_btn = ctk.CTkButton(
            self.header,
            text="+ Add User",
            font=ctk.CTkFont(size=14),
            fg_color=SECONDARY_COLOR,
            hover_color="#2A8572"
        )
        self.add_user_btn.pack(side="right", padx=20)
        
        # Main content
        self.content = ctk.CTkFrame(self.content_area, fg_color=BG_COLOR)
        self.content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Stats cards
        self.stats_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        self.stats_frame.pack(fill="x", pady=(0, 20))
        
        stats = [
            ("Total Users", "1,234", "#e6ffe6"),
            ("Active Users", "1,100", "#e6f3ff"),
            ("New Users (This Month)", "45", "#ffe6e6"),
            ("Premium Users", "89", "#e6fff9")
        ]
        
        for title, value, color in stats:
            card = ctk.CTkFrame(self.stats_frame, fg_color=color)
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
            ).pack(pady=(0, 10))
        
        # Filters frame
        self.filters_frame = ctk.CTkFrame(self.content, fg_color="white")
        self.filters_frame.pack(fill="x", pady=(0, 20))
        
        # Role filter
        ctk.CTkLabel(
            self.filters_frame,
            text="Role:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10, pady=10)
        
        self.role_menu = ctk.CTkOptionMenu(
            self.filters_frame,
            values=["All", "Customer", "Premium", "Staff", "Admin"],
            fg_color=PRIMARY_COLOR,
            button_color=PRIMARY_COLOR
        )
        self.role_menu.pack(side="left", padx=10, pady=10)
        
        # Status filter
        ctk.CTkLabel(
            self.filters_frame,
            text="Status:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10, pady=10)
        
        self.status_menu = ctk.CTkOptionMenu(
            self.filters_frame,
            values=["All", "Active", "Inactive", "Blocked"],
            fg_color=PRIMARY_COLOR,
            button_color=PRIMARY_COLOR
        )
        self.status_menu.pack(side="left", padx=10, pady=10)
        
        # Search bar
        self.search_entry = ctk.CTkEntry(
            self.filters_frame,
            placeholder_text="Search users...",
            width=200
        )
        self.search_entry.pack(side="right", padx=10, pady=10)
        
        # Users table
        self.table_frame = ctk.CTkFrame(self.content, fg_color="white")
        self.table_frame.pack(fill="both", expand=True)
        
        # Table header
        headers = ["User ID", "Name", "Email", "Role", "Status", "Joined Date", "Actions"]
        header_frame = ctk.CTkFrame(self.table_frame, fg_color=PRIMARY_COLOR)
        header_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        for header in headers:
            ctk.CTkLabel(
                header_frame,
                text=header,
                font=ctk.CTkFont(weight="bold"),
                text_color="white"
            ).pack(side="left", expand=True, padx=10, pady=5)
        
        # Dummy users data
        users = [
            ["#001", "John Doe", "john@example.com", "Customer", "Active", "2024-01-15"],
            ["#002", "Jane Smith", "jane@example.com", "Premium", "Active", "2024-02-01"],
            ["#003", "Bob Wilson", "bob@example.com", "Staff", "Active", "2023-12-10"],
            ["#004", "Alice Brown", "alice@example.com", "Customer", "Inactive", "2024-01-20"],
            ["#005", "Admin User", "admin@example.com", "Admin", "Active", "2023-11-01"]
        ]
        
        # Add users to table
        for user in users:
            row_frame = ctk.CTkFrame(self.table_frame, fg_color="transparent")
            row_frame.pack(fill="x", padx=10, pady=5)
            
            for i, item in enumerate(user):
                if i == 4:  # Status column
                    status_color = "#32CD32" if item == "Active" else "#DC143C"
                    status_label = ctk.CTkLabel(
                        row_frame,
                        text=item,
                        font=ctk.CTkFont(size=12),
                        fg_color=status_color,
                        corner_radius=5,
                        text_color="white"
                    )
                    status_label.pack(side="left", expand=True, padx=10)
                else:
                    ctk.CTkLabel(
                        row_frame,
                        text=item,
                        font=ctk.CTkFont(size=12)
                    ).pack(side="left", expand=True, padx=10)
            
            # Action buttons
            actions_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            actions_frame.pack(side="left", expand=True, padx=10)
            
            ctk.CTkButton(
                actions_frame,
                text="Edit",
                font=ctk.CTkFont(size=12),
                fg_color=PRIMARY_COLOR,
                hover_color=SECONDARY_COLOR,
                width=60
            ).pack(side="left", padx=2)
            
            ctk.CTkButton(
                actions_frame,
                text="Block",
                font=ctk.CTkFont(size=12),
                fg_color="#DC143C",
                hover_color="#B22222",
                width=60
            ).pack(side="left", padx=2)
        
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
