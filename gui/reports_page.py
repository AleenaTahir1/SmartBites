import customtkinter as ctk
from .admin_base_page import AdminBasePage
from .constants import *
from database.config import SessionLocal
from database.models import Order, MenuItem, User, OrderItem, OrderStatus
from sqlalchemy import func, desc, extract
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
import logging
from datetime import datetime, timedelta
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from PIL import Image
import os
import csv
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle

class ReportsPage(AdminBasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        # Configure grid
        self.right_panel.grid_columnconfigure(0, weight=1)
        self.right_panel.grid_rowconfigure(0, weight=1)
        
        # Create main content frame with scrollable
        self.main_frame = ctk.CTkScrollableFrame(
            self.right_panel,
            fg_color="transparent"
        )
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Create top bar with title and export button
        self.top_bar = ctk.CTkFrame(
            self.main_frame,
            fg_color="#059669",
            corner_radius=10
        )
        self.top_bar.grid(row=0, column=0, sticky="ew", padx=10, pady=(0, 20))
        self.top_bar.grid_columnconfigure(1, weight=1)
        
        # Title with subtitle
        title_frame = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="w", padx=20, pady=15)
        
        ctk.CTkLabel(
            title_frame,
            text="Reports & Analytics",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="white"
        ).grid(row=0, column=0, sticky="w")
        
        ctk.CTkLabel(
            title_frame,
            text="View your restaurant's performance metrics",
            font=ctk.CTkFont(size=14),
            text_color="#e2e8f0"
        ).grid(row=1, column=0, sticky="w", pady=(2, 0))
        
        # Time period selector
        self.period_frame = ctk.CTkFrame(self.top_bar, fg_color="white", corner_radius=8)
        self.period_frame.grid(row=0, column=1, sticky="e", padx=20, pady=15)
        
        ctk.CTkLabel(
            self.period_frame,
            text="Time Period:",
            font=ctk.CTkFont(size=13),
            text_color="#475569"
        ).pack(side="left", padx=(10, 8))
        
        self.period_var = ctk.StringVar(value="Last 7 Days")
        self.period_menu = ctk.CTkComboBox(
            self.period_frame,
            values=["Today", "Last 7 Days", "Last 30 Days", "This Month", "This Year"],
            variable=self.period_var,
            command=self.update_reports,
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
        self.period_menu.pack(side="left", padx=10)
        
        # Export button
        self.export_btn = ctk.CTkButton(
            self.top_bar,
            text="Export Report",
            command=self.export_report,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            fg_color="#ffffff",
            text_color="#059669",
            hover_color="#e2e8f0"
        )
        self.export_btn.grid(row=0, column=2, sticky="e", padx=20)
        
        # Create metrics frame
        self.metrics_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.metrics_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 20))
        
        for i in range(4):
            self.metrics_frame.grid_columnconfigure(i, weight=1)
        
        # Create charts frame
        self.charts_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.charts_frame.grid(row=2, column=0, sticky="nsew", padx=10)
        self.charts_frame.grid_columnconfigure(0, weight=1)
        self.charts_frame.grid_columnconfigure(1, weight=1)
        
        # Create additional charts frame
        self.additional_charts_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.additional_charts_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=(20, 0))
        self.additional_charts_frame.grid_columnconfigure(0, weight=1)
        self.additional_charts_frame.grid_columnconfigure(1, weight=1)
        
        # Create insights frame
        self.insights_frame = ctk.CTkFrame(self.main_frame, fg_color="white", corner_radius=10)
        self.insights_frame.grid(row=4, column=0, sticky="nsew", padx=10, pady=(20, 0))
        self.insights_frame.grid_columnconfigure(0, weight=1)

        # Add insights title
        ctk.CTkLabel(
            self.insights_frame,
            text="Key Insights & Analysis",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#1e293b"
        ).pack(anchor="w", padx=20, pady=(20, 15))

        # Create text widget for insights
        self.insights_text = ctk.CTkTextbox(
            self.insights_frame,
            height=200,
            font=ctk.CTkFont(size=14),
            text_color="#475569",
            fg_color="white"
        )
        self.insights_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Load initial data
        self.update_reports()
    
    def get_date_range(self):
        today = datetime.now()
        period = self.period_var.get()
        
        if period == "Today":
            start_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == "Last 7 Days":
            start_date = today - timedelta(days=7)
        elif period == "Last 30 Days":
            start_date = today - timedelta(days=30)
        elif period == "This Month":
            start_date = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        elif period == "This Year":
            start_date = today.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            start_date = today - timedelta(days=7)  # Default to Last 7 Days if not recognized
        
        end_date = today  # End date is today
        return start_date, end_date
    
    def update_metrics(self):
        # Clear existing metrics
        for widget in self.metrics_frame.winfo_children():
            widget.destroy()
        
        db = SessionLocal()
        try:
            start_date, end_date = self.get_date_range()
            
            # Get total revenue
            total_revenue = db.query(func.sum(Order.total_amount)).filter(
                Order.created_at.between(start_date, end_date),
                Order.status != OrderStatus.CANCELLED
            ).scalar() or 0
            
            # Get total orders
            total_orders = db.query(func.count(Order.id)).filter(
                Order.created_at.between(start_date, end_date),
                Order.status != OrderStatus.CANCELLED
            ).scalar() or 0
            
            # Get average order value
            avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
            
            # Get active users (users who placed orders)
            active_users = db.query(func.count(func.distinct(Order.customer_id))).filter(
                Order.created_at.between(start_date, end_date),
                Order.status != OrderStatus.CANCELLED
            ).scalar() or 0
            
            # Get previous period metrics for comparison
            period_delta = end_date - start_date
            prev_start = start_date - period_delta
            prev_end = start_date
            
            prev_revenue = db.query(func.sum(Order.total_amount)).filter(
                Order.created_at.between(prev_start, prev_end),
                Order.status != OrderStatus.CANCELLED
            ).scalar() or 0
            
            # Calculate growth
            revenue_growth = ((total_revenue - prev_revenue) / prev_revenue * 100) if prev_revenue > 0 else 0
            
            # Create metric cards
            metrics = [
                ("Total Revenue", f"Rs. {total_revenue:,.2f}", f"{revenue_growth:+.1f}%", "#e6ffe6"),
                ("Total Orders", str(total_orders), "", "#e6f3ff"),
                ("Average Order", f"Rs. {avg_order_value:,.2f}", "", "#ffe6e6"),
                ("Active Users", str(active_users), "", "#e6fff9")
            ]
            
            for i, (title, value, change, color) in enumerate(metrics):
                card = ctk.CTkFrame(self.metrics_frame, fg_color=color, corner_radius=10)
                card.grid(row=0, column=i, sticky="ew", padx=5)
                
                ctk.CTkLabel(
                    card,
                    text=title,
                    font=ctk.CTkFont(size=14),
                    text_color="#1e293b"
                ).pack(pady=(15, 5))
                
                ctk.CTkLabel(
                    card,
                    text=value,
                    font=ctk.CTkFont(size=24, weight="bold"),
                    text_color="#1e293b"
                ).pack(pady=(0, 5))
                
                if change:
                    ctk.CTkLabel(
                        card,
                        text=change,
                        font=ctk.CTkFont(size=12),
                        text_color="#059669" if float(change[:-1]) >= 0 else "#ef4444"
                    ).pack(pady=(0, 15))
                else:
                    ctk.CTkFrame(card, height=15, fg_color="transparent").pack()
        
        finally:
            db.close()
    
    def update_charts(self):
        # Clear existing charts
        for widget in self.charts_frame.winfo_children():
            widget.destroy()
        for widget in self.additional_charts_frame.winfo_children():
            widget.destroy()
        
        db = SessionLocal()
        try:
            start_date, end_date = self.get_date_range()
            
            # Create revenue trend chart
            revenue_frame = ctk.CTkFrame(self.charts_frame, fg_color="white", corner_radius=10)
            revenue_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
            
            revenue_fig, revenue_ax = plt.subplots(figsize=(6, 4))
            revenue_fig.patch.set_facecolor("#ffffff")
            
            # Get daily revenue data
            daily_revenue = db.query(
                func.date(Order.created_at).label('date'),
                func.sum(Order.total_amount).label('revenue')
            ).filter(
                Order.created_at.between(start_date, end_date),
                Order.status != OrderStatus.CANCELLED
            ).group_by(func.date(Order.created_at)).all()
            
            dates = [r.date for r in daily_revenue]
            revenues = [float(r.revenue) for r in daily_revenue]
            
            revenue_ax.plot(dates, revenues, marker='o', color="#059669", linewidth=2)
            revenue_ax.set_title("Revenue Trend", pad=20, fontsize=12, fontweight='bold')
            revenue_ax.tick_params(axis='x', rotation=45)
            revenue_ax.grid(True, linestyle='--', alpha=0.7)
            revenue_ax.set_ylabel("Revenue (Rs.)")
            
            # Embed revenue chart
            revenue_canvas = FigureCanvasTkAgg(revenue_fig, master=revenue_frame)
            revenue_canvas.draw()
            revenue_canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
            
            # Create top selling items chart
            items_frame = ctk.CTkFrame(self.charts_frame, fg_color="white", corner_radius=10)
            items_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
            
            items_fig, items_ax = plt.subplots(figsize=(6, 4))
            items_fig.patch.set_facecolor("#ffffff")
            
            # Get top selling items
            top_items = db.query(
                MenuItem.name,
                func.sum(OrderItem.quantity).label('total_quantity')
            ).join(OrderItem).join(Order).filter(
                Order.created_at.between(start_date, end_date),
                Order.status != OrderStatus.CANCELLED
            ).group_by(MenuItem.name).order_by(desc('total_quantity')).limit(5).all()
            
            item_names = [item.name for item in top_items]
            quantities = [int(item.total_quantity) for item in top_items]
            
            colors = ['#059669', '#0ea5e9', '#f59e0b', '#ef4444', '#8b5cf6']
            items_ax.pie(quantities, labels=item_names, colors=colors, autopct='%1.1f%%')
            items_ax.set_title("Top Selling Items", pad=20, fontsize=12, fontweight='bold')
            
            # Embed items chart
            items_canvas = FigureCanvasTkAgg(items_fig, master=items_frame)
            items_canvas.draw()
            items_canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
            
            # Create order status distribution chart
            status_frame = ctk.CTkFrame(self.additional_charts_frame, fg_color="white", corner_radius=10)
            status_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
            
            status_fig, status_ax = plt.subplots(figsize=(6, 4))
            status_fig.patch.set_facecolor("#ffffff")
            
            # Get order status distribution
            status_dist = db.query(
                Order.status,
                func.count(Order.id).label('count')
            ).filter(
                Order.created_at.between(start_date, end_date)
            ).group_by(Order.status).all()
            
            status_names = [s.status.value for s in status_dist]
            status_counts = [s.count for s in status_dist]
            
            status_colors = {
                'pending': '#f59e0b',
                'processing': '#0ea5e9',
                'completed': '#059669',
                'cancelled': '#ef4444'
            }
            colors = [status_colors[status] for status in status_names]
            
            status_ax.bar(status_names, status_counts, color=colors)
            status_ax.set_title("Order Status Distribution", pad=20, fontsize=12, fontweight='bold')
            status_ax.tick_params(axis='x', rotation=45)
            status_ax.set_ylabel("Number of Orders")
            
            # Embed status chart
            status_canvas = FigureCanvasTkAgg(status_fig, master=status_frame)
            status_canvas.draw()
            status_canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
            
            # Create peak hours chart
            hours_frame = ctk.CTkFrame(self.additional_charts_frame, fg_color="white", corner_radius=10)
            hours_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
            
            hours_fig, hours_ax = plt.subplots(figsize=(6, 4))
            hours_fig.patch.set_facecolor("#ffffff")
            
            # Get orders by hour
            hours_dist = db.query(
                extract('hour', Order.created_at).label('hour'),
                func.count(Order.id).label('count')
            ).filter(
                Order.created_at.between(start_date, end_date),
                Order.status != OrderStatus.CANCELLED
            ).group_by('hour').order_by('hour').all()
            
            hours = [h.hour for h in hours_dist]
            counts = [h.count for h in hours_dist]
            
            hours_ax.plot(hours, counts, marker='o', color="#059669", linewidth=2)
            hours_ax.set_title("Peak Hours Analysis", pad=20, fontsize=12, fontweight='bold')
            hours_ax.set_xlabel("Hour of Day")
            hours_ax.set_ylabel("Number of Orders")
            hours_ax.grid(True, linestyle='--', alpha=0.7)
            hours_ax.set_xticks(range(0, 24, 2))
            
            # Embed hours chart
            hours_canvas = FigureCanvasTkAgg(hours_fig, master=hours_frame)
            hours_canvas.draw()
            hours_canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
            
        finally:
            db.close()
            plt.close('all')
    
    def update_insights(self):
        db = SessionLocal()
        try:
            start_date, end_date = self.get_date_range()
            
            # Get total revenue and growth
            total_revenue = db.query(func.sum(Order.total_amount)).filter(
                Order.created_at.between(start_date, end_date),
                Order.status != OrderStatus.CANCELLED
            ).scalar() or 0
            
            period_delta = end_date - start_date
            prev_start = start_date - period_delta
            prev_end = start_date
            
            prev_revenue = db.query(func.sum(Order.total_amount)).filter(
                Order.created_at.between(prev_start, prev_end),
                Order.status != OrderStatus.CANCELLED
            ).scalar() or 0
            
            revenue_growth = ((total_revenue - prev_revenue) / prev_revenue * 100) if prev_revenue > 0 else 0
            
            # Get busiest hour
            busiest_hour = db.query(
                extract('hour', Order.created_at).label('hour'),
                func.count(Order.id).label('count')
            ).filter(
                Order.created_at.between(start_date, end_date),
                Order.status != OrderStatus.CANCELLED
            ).group_by('hour').order_by(desc('count')).first()
            
            if busiest_hour is None:
                logging.warning('No busiest hour data available')
                formatted_hour = '• Busiest Hour: Not Available'
                peak_period = 'Not Available'
            else:
                try:
                    hour = int(busiest_hour.hour)
                    formatted_hour = f'• Busiest Hour: {hour:02d}:00 - {(hour+1) % 24:02d}:00'
                    peak_period = 'Evening' if 17 <= hour <= 22 else 'Afternoon' if 12 <= hour <= 16 else 'Morning'
                except (ValueError, AttributeError) as e:
                    logging.error('Formatting error for busiest_hour: %s, Error: %s', busiest_hour, e)
                    formatted_hour = '• Busiest Hour: Not Available'
                    peak_period = 'Not Available'
            
            # Get top selling item
            top_item = db.query(
                MenuItem.name,
                func.sum(OrderItem.quantity).label('total_quantity'),
                func.sum(MenuItem.price * OrderItem.quantity).label('total_revenue')
            ).join(OrderItem).join(Order).filter(
                Order.created_at.between(start_date, end_date),
                Order.status != OrderStatus.CANCELLED
            ).group_by(MenuItem.name).order_by(desc('total_quantity')).first()
            
            # Get completion rate
            total_orders = db.query(func.count(Order.id)).filter(
                Order.created_at.between(start_date, end_date)
            ).scalar() or 0
            
            completed_orders = db.query(func.count(Order.id)).filter(
                Order.created_at.between(start_date, end_date),
                Order.status == OrderStatus.COMPLETED
            ).scalar() or 0
            
            completion_rate = (completed_orders / total_orders * 100) if total_orders > 0 else 0
            
            # Format insights text
            period_name = self.period_var.get().lower()
            insights = f"""📊 Performance Summary for {self.period_var.get()}

💰 Revenue Analysis
• Total Revenue: Rs. {total_revenue:,.2f}
• Growth Rate: {revenue_growth:+.1f}% compared to previous period
• {f'Revenue is showing a positive trend with {abs(revenue_growth):.1f}% growth' if revenue_growth > 0 else f'Revenue has decreased by {abs(revenue_growth):.1f}% - may need attention'}

📈 Operations Metrics
• Order Completion Rate: {completion_rate:.1f}%
{formatted_hour}
• Peak Business Period: {peak_period}

🏆 Top Performer
• Most Popular Item: {top_item.name}
• Units Sold: {int(top_item.total_quantity)}
• Revenue Generated: Rs. {float(top_item.total_revenue):,.2f}

💡 Recommendations
• {f'Consider running promotions during off-peak hours to increase sales' if completion_rate > 80 else f'Focus on improving order completion rate which is below target'}
• {f'Expand inventory for {top_item.name} to meet high demand' if top_item.total_quantity > 50 else f'Consider promoting other menu items to diversify sales'}
• {f'Maintain current growth strategies' if revenue_growth > 10 else f'Review pricing and marketing strategies to boost revenue'}
"""
            
            # Update insights text
            self.insights_text.delete("0.0", "end")
            self.insights_text.insert("0.0", insights)
            
        finally:
            db.close()

    def get_report_data(self):
        db = SessionLocal()
        try:
            start_date, end_date = self.get_date_range()
            
            # Get total revenue
            total_revenue = db.query(func.sum(Order.total_amount)).filter(
                Order.created_at.between(start_date, end_date),
                Order.status != OrderStatus.CANCELLED
            ).scalar() or 0
            
            # Get total orders
            total_orders = db.query(func.count(Order.id)).filter(
                Order.created_at.between(start_date, end_date),
                Order.status != OrderStatus.CANCELLED
            ).scalar() or 0
            
            # Get average order value
            avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
            
            # Get active users (users who placed orders)
            active_users = db.query(func.count(func.distinct(Order.customer_id))).filter(
                Order.created_at.between(start_date, end_date),
                Order.status != OrderStatus.CANCELLED
            ).scalar() or 0
            
            # Get previous period metrics for comparison
            period_delta = end_date - start_date
            prev_start = start_date - period_delta
            prev_end = start_date
            
            prev_revenue = db.query(func.sum(Order.total_amount)).filter(
                Order.created_at.between(prev_start, prev_end),
                Order.status != OrderStatus.CANCELLED
            ).scalar() or 0
            
            # Calculate growth
            revenue_growth = ((total_revenue - prev_revenue) / prev_revenue * 100) if prev_revenue > 0 else 0
            
            # Create metric data
            metrics = [
                ("Total Revenue", f"Rs. {total_revenue:,.2f}", f"{revenue_growth:+.1f}%"),
                ("Total Orders", str(total_orders), ""),
                ("Average Order", f"Rs. {avg_order_value:,.2f}", ""),
                ("Active Users", str(active_users), "")
            ]
            
            return metrics
        
        finally:
            db.close()

    def export_report(self):
        from tkinter import filedialog
        from tkinter import messagebox
        from reportlab.lib import colors
        from reportlab.lib.units import inch
        from reportlab.platypus import Table, TableStyle
        from datetime import datetime

        # Gather data for the report
        report_data = self.get_report_data()

        # Gather analytics data
        db = SessionLocal()
        try:
            start_date, end_date = self.get_date_range()
            
            # Get peak hours
            peak_hours_data = db.query(
                extract('hour', Order.created_at).label('hour'),
                func.count(Order.id).label('count')
            ).filter(
                Order.created_at.between(start_date, end_date),
                Order.status != OrderStatus.CANCELLED
            ).group_by('hour').order_by(desc('count')).first()
            
            if peak_hours_data:
                hour = int(peak_hours_data.hour)
                peak_hours = f"{hour:02d}:00 - {(hour+1) % 24:02d}:00"
            else:
                peak_hours = "Not Available"
            
            # Get popular items
            popular_items_data = db.query(
                MenuItem.name,
                func.sum(OrderItem.quantity).label('total_quantity')
            ).select_from(MenuItem).join(
                OrderItem, MenuItem.id == OrderItem.menu_item_id
            ).join(
                Order, OrderItem.order_id == Order.id
            ).filter(
                Order.created_at.between(start_date, end_date),
                Order.status != OrderStatus.CANCELLED
            ).group_by(MenuItem.name).order_by(desc('total_quantity')).limit(2).all()
            
            popular_items = ", ".join([f"{item.name} ({int(item.total_quantity)} orders)" 
                                     for item in popular_items_data]) if popular_items_data else "Not Available"
            
        finally:
            db.close()

        # Open file dialog to choose save location
        file_path = filedialog.asksaveasfilename(defaultextension='.pdf',
                                               filetypes=[('PDF files', '*.pdf'), ('All files', '*.*')])
        if not file_path:
            return  # User canceled the save dialog

        try:
            # Create PDF with better styling
            c = canvas.Canvas(file_path, pagesize=letter)
            width, height = letter

            # Add a light gray background header
            c.setFillColor(colors.lightgrey)
            c.rect(0, height - 120, width, 120, fill=True)
            
            # Header with logo placeholder
            c.setFillColor(colors.black)
            c.setFont("Helvetica-Bold", 24)
            c.drawString(inch, height - 40, "SmartBites - Admin End")
            
            # Report title with current date and time
            current_datetime = datetime.now()
            formatted_date = current_datetime.strftime("%Y-%m-%d")
            formatted_time = current_datetime.strftime("%I:%M %p")
            c.setFont("Helvetica", 14)
            c.drawString(inch, height - 60, f"Daily Order Report - {formatted_date}")
            c.drawString(inch + 4*inch, height - 60, f"Generated at: {formatted_time}")
            c.setFont("Helvetica", 12)
            c.drawString(inch, height - 80, "University Cafeteria")
            c.drawString(inch, height - 100, "Generated By: SmartBites Admin Panel")

            # Add decorative line
            c.setStrokeColor(colors.blue)
            c.setLineWidth(2)
            c.line(inch, height - 130, width - inch, height - 130)

            # Analytics Insights Section
            y = height - 180
            c.setFont("Helvetica-Bold", 16)
            c.drawString(inch, y, "Analytics Insights")
            
            c.setFont("Helvetica", 12)
            y -= 25
            c.drawString(inch, y, f"Peak Order Hours: {peak_hours}")
            y -= 20
            c.drawString(inch, y, f"Most Popular Items: {popular_items}")
            
            # Order Breakdown
            y -= 40
            c.setFont("Helvetica-Bold", 16)
            c.drawString(inch, y, "Order Breakdown")
            y -= 30

            # Create the order table
            data = [['Order ID', 'User ID', 'Items', 'Time', 'Amount (PKR)']]
            
            # Get order data
            orders = db.query(
                Order.id,
                Order.customer_id,
                Order.created_at,
                Order.total_amount
            ).filter(
                Order.created_at.between(start_date, end_date),
                Order.status != OrderStatus.CANCELLED
            ).order_by(desc(Order.created_at)).all()

            # Add order data rows
            for order in orders:
                # Get items for this order
                items_query = db.query(
                    MenuItem.name,
                    OrderItem.quantity
                ).join(
                    OrderItem, MenuItem.id == OrderItem.menu_item_id
                ).filter(
                    OrderItem.order_id == order.id
                ).all()
                
                # Format items string
                items_str = ", ".join([f"{item.name} x{item.quantity}" for item in items_query])
                
                data.append([
                    str(order.id),
                    str(order.customer_id),
                    items_str,
                    order.created_at.strftime('%I:%M %p'),  # 12-hour format with AM/PM
                    f"{float(order.total_amount):.2f}"
                ])

            # Create table with adjusted widths
            table = Table(data, colWidths=[0.7*inch, 0.7*inch, 4*inch, 1*inch, 1*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('WORDWRAP', (2, 1), (2, -1), True),  # Enable word wrap for items column
            ]))

            # Calculate table height based on number of rows
            row_height = 0.4 * inch  # Adjust this value to control row height
            table_height = row_height * len(data)
            
            # Position table with more space from top
            table.wrapOn(c, width, height)
            table.drawOn(c, inch, height - 180 - table_height)

            # Draw Summary Section with proper spacing
            summary_y = height - 200 - table_height  # Position summary below table
            c.setFont("Helvetica-Bold", 14)
            c.drawString(inch, summary_y, "Summary Section")
            
            c.setFont("Helvetica", 12)
            summary_y -= 25
            c.drawString(inch, summary_y, f"Total Orders Processed: {len(orders)}")
            summary_y -= 20
            total_revenue = sum(float(order.total_amount) for order in orders)
            c.drawString(inch, summary_y, f"Total Revenue: Rs. {total_revenue:.2f}")
            summary_y -= 20
            
            # Count unique users
            unique_users = len(set(order.customer_id for order in orders))
            c.drawString(inch, summary_y, f"Active Users: {unique_users}")

            # Footer with proper spacing
            c.setFont("Helvetica", 8)
            c.drawString(inch, inch, f"Report generated on {formatted_date} at {formatted_time}")
            c.drawString(width - 2*inch, inch, f"Page 1 of 1")
            c.save()
            messagebox.showinfo('Success', 'Report exported successfully!')
        except Exception as e:
            messagebox.showerror('Error', f'Failed to export report: {str(e)}')

    def update_reports(self, *args):
        self.update_metrics()
        self.update_charts()
        self.update_insights()
