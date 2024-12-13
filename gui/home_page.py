import customtkinter as ctk
import os
from PIL import Image
from .admin_base_page import AdminBasePage
from .constants import *

class HomePage(AdminBasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.set_active_button("Dashboard")
        self.current_filter = "All Orders"  # Track current filter
        self.orders_data = [
            {
                "id": "ORD-001",
                "customer": "John Doe",
                "items": "Burger, Fries, Coke",
                "total": "$25.99",
                "status": "Pending",
                "date": "2023-12-13"
            },
            {
                "id": "ORD-002",
                "customer": "Jane Smith",
                "items": "Pizza, Wings",
                "total": "$35.50",
                "status": "Processing",
                "date": "2023-12-13"
            },
            {
                "id": "ORD-003",
                "customer": "Mike Johnson",
                "items": "Salad, Juice",
                "total": "$15.99",
                "status": "Completed",
                "date": "2023-12-12"
            },
            {
                "id": "ORD-004",
                "customer": "Sarah Wilson",
                "items": "Pasta, Garlic Bread",
                "total": "$28.99",
                "status": "Pending",
                "date": "2023-12-13"
            },
            {
                "id": "ORD-005",
                "customer": "David Brown",
                "items": "Steak, Wine",
                "total": "$89.99",
                "status": "Cancelled",
                "date": "2023-12-11"
            },
            {
                "id": "ORD-006",
                "customer": "Emily Davis",
                "items": "Sushi Platter",
                "total": "$75.00",
                "status": "Processing",
                "date": "2023-12-13"
            },
            {
                "id": "ORD-007",
                "customer": "Tom Wilson",
                "items": "Chicken Biryani",
                "total": "$18.99",
                "status": "Completed",
                "date": "2023-12-12"
            },
            {
                "id": "ORD-008",
                "customer": "Lisa Anderson",
                "items": "Fish & Chips",
                "total": "$22.50",
                "status": "Pending",
                "date": "2023-12-13"
            },
            {
                "id": "ORD-009",
                "customer": "James Martin",
                "items": "Vegetarian Pizza",
                "total": "$28.99",
                "status": "Processing",
                "date": "2023-12-13"
            },
            {
                "id": "ORD-010",
                "customer": "Anna White",
                "items": "Ice Cream Sundae",
                "total": "$8.99",
                "status": "Completed",
                "date": "2023-12-12"
            }
        ]
        self.show_dashboard()

    def filter_orders(self, status="All Orders"):
        """Filter orders based on status"""
        self.current_filter = status
        self.show_dashboard()

    def get_filtered_orders(self):
        """Get orders based on current filter"""
        if self.current_filter == "All Orders":
            return self.orders_data
        return [order for order in self.orders_data if order["status"] == self.current_filter]

    def get_status_counts(self):
        """Get counts for each status"""
        counts = {
            "All Orders": len(self.orders_data),
            "Pending": 0,
            "Processing": 0,
            "Completed": 0,
            "Cancelled": 0
        }
        for order in self.orders_data:
            counts[order["status"]] += 1
        return counts

    def show_dashboard(self):
        """Show the main dashboard content"""
        # Clear previous content
        for widget in self.content_area.winfo_children():
            widget.destroy()

        # Main content
        self.main_content = ctk.CTkFrame(
            self.content_area,
            fg_color=BG_COLOR
        )
        self.main_content.pack(fill="both", expand=True)

        # Top bar with search and quick actions
        self.top_bar = ctk.CTkFrame(
            self.main_content,
            fg_color="transparent",
            height=60
        )
        self.top_bar.pack(fill="x", pady=(0, 20))
        
        # Logo and brand section
        self.brand_frame = ctk.CTkFrame(
            self.top_bar,
            fg_color="transparent",
            height=60
        )
        self.brand_frame.pack(side="left", padx=(0, 20))
        
        try:
            logo_path = os.path.join("assets", "images", "myLogo.png")
            self.logo_image = ctk.CTkImage(
                light_image=Image.open(logo_path),
                dark_image=Image.open(logo_path),
                size=(30, 30)
            )
            self.logo_label = ctk.CTkLabel(
                self.brand_frame,
                image=self.logo_image,
                text=""
            )
            self.logo_label.pack(side="left", padx=(0, 10))
        except Exception as e:
            print(f"Error loading logo: {e}")
        
        self.brand_label = ctk.CTkLabel(
            self.brand_frame,
            text="SmartBites",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=TEXT_COLOR
        )
        self.brand_label.pack(side="left")

        # Search bar
        self.search_frame = ctk.CTkFrame(
            self.top_bar,
            fg_color="transparent"
        )
        self.search_frame.pack(side="left", fill="x", expand=True, padx=20)

        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Search orders, users, or menu items",
            height=40,
            width=400,
            corner_radius=8
        )
        self.search_entry.pack(side="left")

        self.search_btn = ctk.CTkButton(
            self.search_frame,
            text="",
            width=40,
            height=40,
            fg_color=PRIMARY_COLOR,
            hover_color=SECONDARY_COLOR,
            corner_radius=8
        )
        self.search_btn.pack(side="left", padx=(10, 0))

        # Quick action buttons
        self.quick_actions = ctk.CTkFrame(
            self.top_bar,
            fg_color="transparent"
        )
        self.quick_actions.pack(side="right")

        self.add_menu_btn = ctk.CTkButton(
            self.quick_actions,
            text="+ Add Menu Item",
            font=ctk.CTkFont(size=14),
            fg_color=PRIMARY_COLOR,
            hover_color=SECONDARY_COLOR,
            height=40,
            corner_radius=8
        )
        self.add_menu_btn.pack(side="left", padx=5)

        self.export_btn = ctk.CTkButton(
            self.quick_actions,
            text="Export Report",
            font=ctk.CTkFont(size=14),
            fg_color=PRIMARY_COLOR,
            hover_color=SECONDARY_COLOR,
            height=40,
            corner_radius=8
        )
        self.export_btn.pack(side="left", padx=5)

        # Stats cards
        self.stats_frame = ctk.CTkFrame(
            self.main_content,
            fg_color="transparent"
        )
        self.stats_frame.pack(fill="x", pady=(0, 20))

        stats = [
            ("Total Revenue", "$15,300", "#e6ffe6", ""),
            ("Active Orders", "25", "#e6f3ff", ""),
            ("Total Users", "300", "#ffe6e6", ""),
            ("Menu Items", "48", "#e6fff9", "")
        ]

        for title, value, color, icon in stats:
            card = ctk.CTkFrame(
                self.stats_frame,
                fg_color=color
            )
            card.pack(side="left", padx=5, fill="x", expand=True)

            ctk.CTkLabel(
                card,
                text=f"{icon} {title}",
                font=ctk.CTkFont(size=14)
            ).pack(pady=(10, 5))

            ctk.CTkLabel(
                card,
                text=value,
                font=ctk.CTkFont(size=24, weight="bold")
            ).pack(pady=(0, 10))

        # Orders Frame
        self.orders_frame = ctk.CTkFrame(
            self.main_content,
            fg_color="transparent"
        )
        self.orders_frame.pack(fill="x", padx=20, pady=10)

        # Header with Recent Orders and View All
        header_frame = ctk.CTkFrame(self.orders_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            header_frame,
            text="Recent Orders",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(side="left")

        view_all_btn = ctk.CTkButton(
            header_frame,
            text="View All Orders",
            font=ctk.CTkFont(size=14),
            fg_color=PRIMARY_COLOR,
            hover_color=SECONDARY_COLOR,
            height=32,
            width=140,
            corner_radius=8
        )
        view_all_btn.pack(side="right")

        # Order Status Tabs
        status_frame = ctk.CTkFrame(self.orders_frame, fg_color="transparent")
        status_frame.pack(fill="x", pady=(0, 20))

        status_counts = self.get_status_counts()
        statuses = [
            ("All Orders", status_counts["All Orders"], "#00B894"),
            ("Pending", status_counts["Pending"], "#FFA502"),
            ("Processing", status_counts["Processing"], "#54A0FF"),
            ("Completed", status_counts["Completed"], "#00B894"),
            ("Cancelled", status_counts["Cancelled"], "#FF4757")
        ]

        for status, count, color in statuses:
            btn = ctk.CTkButton(
                status_frame,
                text=f"{status} ({count})",
                font=ctk.CTkFont(size=14),
                fg_color=color if status == self.current_filter else "transparent",
                text_color="white" if status == self.current_filter else "gray10",
                hover_color=color,
                height=35,
                width=130,
                corner_radius=8,
                command=lambda s=status: self.filter_orders(s)
            )
            btn.pack(side="left", padx=(0, 15))

        # Orders Table
        table_frame = ctk.CTkFrame(self.orders_frame, fg_color="white", corner_radius=15)
        table_frame.pack(fill="both", expand=True)

        # Column widths
        col_widths = {
            "Order ID": 120,
            "Customer": 150,
            "Items": 200,
            "Total": 100,
            "Status": 120,
            "Actions": 150
        }

        # Table Headers
        headers = ["Order ID", "Customer", "Items", "Total", "Status", "Actions"]
        header_frame = ctk.CTkFrame(table_frame, fg_color=PRIMARY_COLOR, height=45, corner_radius=8)
        header_frame.pack(fill="x", padx=2, pady=2)
        header_frame.pack_propagate(False)

        for header in headers:
            header_label = ctk.CTkLabel(
                header_frame,
                text=header,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="white",
                width=col_widths[header]
            )
            header_label.pack(side="left", padx=10)

        # Status colors
        status_colors = {
            "Pending": "#FFA502",
            "Processing": "#54A0FF",
            "Completed": "#00B894",
            "Cancelled": "#FF4757"
        }

        # Create order rows with alternating background
        filtered_orders = self.get_filtered_orders()
        for i, order in enumerate(filtered_orders):
            row_bg = "#F8F9FA" if i % 2 == 0 else "white"
            row_frame = ctk.CTkFrame(table_frame, fg_color=row_bg, height=50)
            row_frame.pack(fill="x", padx=2, pady=1)
            row_frame.pack_propagate(False)

            # Order ID
            ctk.CTkLabel(
                row_frame,
                text=order["id"],
                font=ctk.CTkFont(size=14),
                width=col_widths["Order ID"]
            ).pack(side="left", padx=10)

            # Customer
            ctk.CTkLabel(
                row_frame,
                text=order["customer"],
                font=ctk.CTkFont(size=14),
                width=col_widths["Customer"]
            ).pack(side="left", padx=10)

            # Items
            ctk.CTkLabel(
                row_frame,
                text=order["items"],
                font=ctk.CTkFont(size=14),
                width=col_widths["Items"]
            ).pack(side="left", padx=10)

            # Total
            ctk.CTkLabel(
                row_frame,
                text=order["total"],
                font=ctk.CTkFont(size=14),
                width=col_widths["Total"]
            ).pack(side="left", padx=10)

            # Status with color coding
            status_frame = ctk.CTkFrame(row_frame, fg_color="transparent", width=col_widths["Status"])
            status_frame.pack(side="left", padx=10)
            status_frame.pack_propagate(False)

            status_label = ctk.CTkLabel(
                status_frame,
                text=order["status"],
                font=ctk.CTkFont(size=13),
                fg_color=status_colors[order["status"]],
                text_color="white",
                corner_radius=5,
                width=90,
                height=25
            )
            status_label.place(relx=0.5, rely=0.5, anchor="center")

            # Actions
            actions_frame = ctk.CTkFrame(row_frame, fg_color="transparent", width=col_widths["Actions"])
            actions_frame.pack(side="left", padx=10)
            actions_frame.pack_propagate(False)

            view_btn = ctk.CTkButton(
                actions_frame,
                text="View",
                font=ctk.CTkFont(size=13),
                fg_color=PRIMARY_COLOR,
                hover_color=SECONDARY_COLOR,
                width=60,
                height=28,
                corner_radius=5
            )
            view_btn.place(relx=0.2, rely=0.5, anchor="center")

            # Add edit button only for non-completed orders
            if order["status"] not in ["Completed", "Cancelled"]:
                edit_btn = ctk.CTkButton(
                    actions_frame,
                    text="Edit",
                    font=ctk.CTkFont(size=13),
                    fg_color="#54A0FF",
                    hover_color="#2E86DE",
                    width=60,
                    height=28,
                    corner_radius=5
                )
                edit_btn.place(relx=0.7, rely=0.5, anchor="center")

    def show_orders(self):
        self.controller.show_orders_page()

    def show_menu_management(self):
        self.controller.show_menu_management_page()

    def show_user_management(self):
        self.controller.show_user_management_page()

    def show_reports(self):
        self.controller.show_reports_page()

    def show_settings(self):
        self.controller.show_settings_page()

    def logout(self):
        self.controller.show_login_page()
