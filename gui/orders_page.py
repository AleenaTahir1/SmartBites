import customtkinter as ctk
from .admin_base_page import AdminBasePage
from database.config import SessionLocal
from database.models import Order, OrderItem, MenuItem, OrderStatus
from tkinter import messagebox
from datetime import datetime

class OrdersPage(AdminBasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        # Configure grid
        self.right_panel.grid_columnconfigure(0, weight=1)
        self.right_panel.grid_rowconfigure(0, weight=1)
        
        # Create main content frame
        self.content_frame = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        self.content_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(2, weight=1)  # Row 2 for orders frame
        
        # Create top bar with title
        self.top_bar = ctk.CTkFrame(
            self.content_frame,
            fg_color="#059669",  # Green background
            corner_radius=10
        )
        self.top_bar.grid(row=0, column=0, sticky="ew", padx=10, pady=(0, 20))
        self.top_bar.grid_columnconfigure(1, weight=1)  # For spacing between title and filters
        
        # Title with subtitle
        title_frame = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="w", padx=20, pady=15)
        
        ctk.CTkLabel(
            title_frame,
            text="Orders Management",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="white"
        ).grid(row=0, column=0, sticky="w")
        
        ctk.CTkLabel(
            title_frame,
            text="Manage your cafeteria's orders",
            font=ctk.CTkFont(size=14),
            text_color="#e2e8f0"
        ).grid(row=1, column=0, sticky="w", pady=(2, 0))
        
        # Create filters frame with white background
        self.filters_frame = ctk.CTkFrame(
            self.top_bar,
            fg_color="white",
            corner_radius=8
        )
        self.filters_frame.grid(row=0, column=1, sticky="e", padx=20, pady=15)
        
        # Status filter
        status_frame = ctk.CTkFrame(self.filters_frame, fg_color="transparent")
        status_frame.pack(side="left", padx=10)
        
        ctk.CTkLabel(
            status_frame,
            text="Filter by Status:",
            font=ctk.CTkFont(size=13),
            text_color="#475569"  # Slate color for better contrast
        ).pack(side="left", padx=(0, 8))
        
        self.status_var = ctk.StringVar(value="All")
        self.status_filter = ctk.CTkComboBox(
            status_frame,
            values=["All"] + [status.value for status in OrderStatus],
            variable=self.status_var,
            command=self.load_orders,
            width=140,
            height=32,
            fg_color="white",
            border_color="#e2e8f0",
            button_color="#059669",
            button_hover_color="#047857",
            dropdown_hover_color="#f1f5f9",
            dropdown_fg_color="white",
            dropdown_text_color="#1e293b",
            text_color="#1e293b",
            font=ctk.CTkFont(size=13)
        )
        self.status_filter.pack(side="left")
        
        # Separator
        separator = ctk.CTkFrame(
            self.filters_frame,
            fg_color="#e2e8f0",
            width=1,
            height=25
        )
        separator.pack(side="left", padx=15, pady=5)
        
        # Date filter
        date_frame = ctk.CTkFrame(self.filters_frame, fg_color="transparent")
        date_frame.pack(side="left", padx=10)
        
        ctk.CTkLabel(
            date_frame,
            text="Date Range:",
            font=ctk.CTkFont(size=13),
            text_color="#475569"  # Slate color for better contrast
        ).pack(side="left", padx=(0, 8))
        
        self.date_var = ctk.StringVar(value="All Time")
        self.date_filter = ctk.CTkComboBox(
            date_frame,
            values=["All Time", "Today", "Last 7 Days", "Last 30 Days"],
            variable=self.date_var,
            command=self.load_orders,
            width=140,
            height=32,
            fg_color="white",
            border_color="#e2e8f0",
            button_color="#059669",
            button_hover_color="#047857",
            dropdown_hover_color="#f1f5f9",
            dropdown_fg_color="white",
            dropdown_text_color="#1e293b",
            text_color="#1e293b",
            font=ctk.CTkFont(size=13)
        )
        self.date_filter.pack(side="left")
        
        # Create orders frame with white background
        self.orders_frame = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="white",  # Set white background
            corner_radius=8
        )
        self.orders_frame.grid(row=2, column=0, sticky="nsew", padx=10)
        self.orders_frame.grid_columnconfigure(0, weight=1)
        self.orders_frame.grid_columnconfigure(1, weight=2)
        self.orders_frame.grid_columnconfigure(2, weight=2)
        self.orders_frame.grid_columnconfigure(3, weight=1)
        self.orders_frame.grid_columnconfigure(4, weight=1)
        self.orders_frame.grid_columnconfigure(5, weight=2)
        self.orders_frame.grid_columnconfigure(6, weight=2)
        
        # Stats frame at the bottom
        self.stats_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        self.stats_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=(10, 5))
        
        # Load initial orders
        self.load_orders()
    
    def load_orders(self, *args):
        # Clear existing orders
        for widget in self.orders_frame.winfo_children():
            widget.destroy()
        
        # Create headers with consistent styling
        headers = ["Order ID", "Customer", "Items", "Total", "Status", "Date", "Actions"]
        header_bg = ctk.CTkFrame(self.orders_frame, fg_color="#f1f5f9", height=40, corner_radius=0)
        header_bg.grid(row=0, column=0, columnspan=7, sticky="ew")
        header_bg.grid_propagate(False)
        
        for col, header in enumerate(headers):
            label = ctk.CTkLabel(
                header_bg,
                text=header,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#1e293b",
                fg_color="transparent",
                anchor="w" if col in [0, 1, 2] else "center",
                corner_radius=0
            )
            label.grid(row=0, column=col, sticky="ew", padx=(20 if col == 0 else 15, 15), pady=10)
        
        # Configure header grid weights
        for i in range(7):
            header_bg.grid_columnconfigure(i, weight=1)
        
        # Add separator line
        separator = ctk.CTkFrame(self.orders_frame, fg_color="#e2e8f0", height=1, corner_radius=0)
        separator.grid(row=1, column=0, columnspan=7, sticky="ew", padx=10)

        # Get orders from database
        db = SessionLocal()
        try:
            query = db.query(Order).order_by(Order.created_at.desc())
            
            # Apply status filter
            status_filter = self.status_var.get()
            if status_filter != "All":
                query = query.filter(Order.status == OrderStatus[status_filter.upper()])
            
            # Apply date filter
            date_filter = self.date_var.get()
            if date_filter != "All Time":
                today = datetime.now()
                if date_filter == "Today":
                    query = query.filter(Order.created_at >= today.replace(hour=0, minute=0, second=0))
                elif date_filter == "Last 7 Days":
                    query = query.filter(Order.created_at >= today.replace(day=today.day-7))
                elif date_filter == "Last 30 Days":
                    query = query.filter(Order.created_at >= today.replace(day=today.day-30))
            
            orders = query.all()
            
            # Display orders with consistent alignment
            for row, order in enumerate(orders, start=2):
                # Order ID
                ctk.CTkLabel(
                    self.orders_frame,
                    text=f"#{order.id}",
                    anchor="w",
                    font=ctk.CTkFont(size=13)
                ).grid(row=row, column=0, sticky="w", padx=10, pady=5)

                # Customer
                ctk.CTkLabel(
                    self.orders_frame,
                    text=order.customer.username,
                    anchor="w",
                    font=ctk.CTkFont(size=13)
                ).grid(row=row, column=1, sticky="w", padx=10, pady=5)

                # Items
                ctk.CTkLabel(
                    self.orders_frame,
                    text=f"{len(order.items)} items",
                    anchor="w",
                    font=ctk.CTkFont(size=13)
                ).grid(row=row, column=2, sticky="w", padx=10, pady=5)

                # Total
                ctk.CTkLabel(
                    self.orders_frame,
                    text=f"Rs. {order.total_amount:.2f}",
                    anchor="center",
                    font=ctk.CTkFont(size=13)
                ).grid(row=row, column=3, sticky="ew", padx=10, pady=5)

                # Status
                status_colors = {
                    OrderStatus.PENDING: ("#FFA502", "#FFF3E0", "Pending"),
                    OrderStatus.PROCESSING: ("#54A0FF", "#E3F2FD", "Processing"),
                    OrderStatus.COMPLETED: ("#4CAF50", "#E8F5E9", "Completed"),
                    OrderStatus.CANCELLED: ("#FF5252", "#FFEBEE", "Cancelled")
                }
                
                status_color, bg_color, status_text = status_colors[order.status]
                status_frame = ctk.CTkFrame(
                    self.orders_frame,
                    fg_color=bg_color,
                    corner_radius=4,
                    height=25
                )
                status_frame.grid(row=row, column=4, sticky="ew", padx=10, pady=5)
                status_frame.grid_propagate(False)
                
                ctk.CTkLabel(
                    status_frame,
                    text=status_text,
                    text_color=status_color,
                    font=ctk.CTkFont(size=13),
                    anchor="center"
                ).grid(row=0, column=0, sticky="nsew", padx=5)
                status_frame.grid_columnconfigure(0, weight=1)

                # Date
                ctk.CTkLabel(
                    self.orders_frame,
                    text=order.created_at.strftime("%Y-%m-%d %H:%M"),
                    anchor="center",
                    font=ctk.CTkFont(size=13)
                ).grid(row=row, column=5, sticky="ew", padx=10, pady=5)

                # Actions
                if order.status == OrderStatus.PENDING:
                    action_btn = ctk.CTkButton(
                        self.orders_frame,
                        text="Mark processing",
                        command=lambda o=order: self.update_order_status(o, OrderStatus.PROCESSING),
                        fg_color="#059669",
                        hover_color="#047857",
                        height=30,
                        font=ctk.CTkFont(size=13)
                    )
                elif order.status == OrderStatus.PROCESSING:
                    action_btn = ctk.CTkButton(
                        self.orders_frame,
                        text="Mark complete",
                        command=lambda o=order: self.update_order_status(o, OrderStatus.COMPLETED),
                        fg_color="#059669",
                        hover_color="#047857",
                        height=30,
                        font=ctk.CTkFont(size=13)
                    )
                else:
                    action_btn = None

                if action_btn:
                    action_btn.grid(row=row, column=6, sticky="ew", padx=10, pady=5)
            
            # Update stats
            total_orders = len(orders)
            total_revenue = sum(order.total_amount for order in orders)
            avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
            
            # Clear and update stats frame
            for widget in self.stats_frame.winfo_children():
                widget.destroy()
            
            stats = [
                (f"Total Orders: {total_orders}", "#3b82f6"),  # Blue
                (f"Total Revenue: Rs. {total_revenue:.2f}", "#3b82f6"),
                (f"Average Order: Rs. {avg_order_value:.2f}", "#3b82f6")
            ]
            
            for i, (text, fg_color) in enumerate(stats):
                stat_frame = ctk.CTkFrame(
                    self.stats_frame,
                    fg_color=fg_color,
                    corner_radius=6,
                    height=35
                )
                stat_frame.pack(side="left", padx=5, pady=5, expand=True, fill="x")
                stat_frame.pack_propagate(False)
                
                stat_label = ctk.CTkLabel(
                    stat_frame,
                    text=text,
                    font=ctk.CTkFont(size=13, weight="bold"),
                    text_color="white",
                    anchor="center"
                )
                stat_label.pack(expand=True, pady=2)
                
        finally:
            db.close()
    
    def show_order_details(self, order):
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"Order #{order.id} Details")
        dialog.geometry("600x500")
        dialog.grab_set()  # Make the dialog modal
        
        # Title
        ctk.CTkLabel(
            dialog,
            text=f"Order #{order.id} Details",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)
        
        # Customer info
        customer_frame = ctk.CTkFrame(dialog)
        customer_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            customer_frame,
            text="Customer Information",
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        ctk.CTkLabel(
            customer_frame,
            text=f"Username: {order.customer.username}"
        ).pack(anchor="w", padx=10, pady=2)
        
        ctk.CTkLabel(
            customer_frame,
            text=f"Email: {order.customer.email}"
        ).pack(anchor="w", padx=10, pady=2)
        
        # Order info
        order_info_frame = ctk.CTkFrame(dialog)
        order_info_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            order_info_frame,
            text="Order Information",
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        ctk.CTkLabel(
            order_info_frame,
            text=f"Status: {order.status.value}"
        ).pack(anchor="w", padx=10, pady=2)
        
        ctk.CTkLabel(
            order_info_frame,
            text=f"Date: {order.created_at.strftime('%Y-%m-%d %H:%M')}"
        ).pack(anchor="w", padx=10, pady=2)
        
        # Items
        items_frame = ctk.CTkFrame(dialog)
        items_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(
            items_frame,
            text="Order Items",
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        # Create scrollable frame for items
        items_list = ctk.CTkScrollableFrame(items_frame)
        items_list.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Headers
        headers_frame = ctk.CTkFrame(items_list, fg_color="transparent")
        headers_frame.pack(fill="x", pady=5)
        
        headers = ["Item", "Quantity", "Price", "Total"]
        for header in headers:
            ctk.CTkLabel(
                headers_frame,
                text=header,
                font=ctk.CTkFont(weight="bold")
            ).pack(side="left", expand=True)
        
        # Items
        for item in order.items:
            item_frame = ctk.CTkFrame(items_list, fg_color="transparent")
            item_frame.pack(fill="x", pady=2)
            
            ctk.CTkLabel(
                item_frame,
                text=item.menu_item.name
            ).pack(side="left", expand=True)
            
            ctk.CTkLabel(
                item_frame,
                text=str(item.quantity)
            ).pack(side="left", expand=True)
            
            ctk.CTkLabel(
                item_frame,
                text=f"Rs. {item.menu_item.price:.2f}"
            ).pack(side="left", expand=True)
            
            ctk.CTkLabel(
                item_frame,
                text=f"Rs. {(item.quantity * item.menu_item.price):.2f}"
            ).pack(side="left", expand=True)
        
        # Total
        total_frame = ctk.CTkFrame(dialog)
        total_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            total_frame,
            text=f"Total Amount: Rs. {order.total_amount:.2f}",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="e", padx=10)
    
    def update_order_status(self, order, new_status):
        if new_status == OrderStatus.CANCELLED:
            if not messagebox.askyesno("Confirm Cancel", f"Are you sure you want to cancel Order #{order.id}?"):
                return
        
        db = SessionLocal()
        try:
            db_order = db.query(Order).filter(Order.id == order.id).first()
            if db_order:
                db_order.status = new_status
                db.commit()
                messagebox.showinfo("Success", f"Order #{order.id} {new_status.value.lower()} successfully!")
                self.load_orders()  # Refresh the list
        finally:
            db.close()
