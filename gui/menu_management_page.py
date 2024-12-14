import customtkinter as ctk
from .admin_base_page import AdminBasePage
from database.config import SessionLocal
from database.models import MenuItem
from tkinter import messagebox, filedialog
from PIL import Image
import os

class MenuManagementPage(AdminBasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        # Configure grid
        self.right_panel.grid_columnconfigure(0, weight=1)
        self.right_panel.grid_rowconfigure(0, weight=1)
        
        # Create main content frame
        self.content_frame = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        self.content_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)  # Row 1 for menu items frame
        
        # Create top bar with title and add button
        self.top_bar = ctk.CTkFrame(self.content_frame, fg_color="#059669", corner_radius=10)
        self.top_bar.grid(row=0, column=0, sticky="ew", padx=10, pady=(0, 20))
        self.top_bar.grid_columnconfigure(1, weight=1)  # For spacing between title and button
        
        # Title with subtitle
        title_frame = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="w", padx=20, pady=15)
        
        ctk.CTkLabel(
            title_frame,
            text="Menu Management",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="white"
        ).grid(row=0, column=0, sticky="w")
        
        ctk.CTkLabel(
            title_frame,
            text="Manage your cafeteria's menu items",
            font=ctk.CTkFont(size=14),
            text_color="#e2e8f0"
        ).grid(row=1, column=0, sticky="w", pady=(2, 0))
        
        self.add_item_button = ctk.CTkButton(
            self.top_bar,
            text="+ Add New Item",
            command=self.show_add_item_dialog,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            fg_color="#ffffff",
            text_color="#059669",
            hover_color="#e2e8f0"
        )
        self.add_item_button.grid(row=0, column=1, sticky="e", padx=20)
        
        # Create menu items frame with white background and rounded corners
        self.menu_items_frame = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="white",
            corner_radius=8,
            width=1200  # Make it wider to show scrollbar
        )
        self.menu_items_frame.grid(row=1, column=0, sticky="nsew", padx=10)
        
        # Configure grid columns for perfect alignment
        self.menu_items_frame.grid_columnconfigure(0, weight=2)  # Name
        self.menu_items_frame.grid_columnconfigure(1, weight=3)  # Description
        self.menu_items_frame.grid_columnconfigure(2, weight=1)  # Price
        self.menu_items_frame.grid_columnconfigure(3, weight=1)  # Category
        self.menu_items_frame.grid_columnconfigure(4, weight=1)  # Available
        self.menu_items_frame.grid_columnconfigure(5, weight=2)  # Actions
        
        # Create headers with consistent styling
        headers = ["Name", "Description", "Price", "Category", "Available", "Actions"]
        header_bg = ctk.CTkFrame(self.menu_items_frame, fg_color="#f1f5f9", height=40, corner_radius=0)
        header_bg.grid(row=0, column=0, columnspan=6, sticky="ew")
        header_bg.grid_propagate(False)
        
        for col, header in enumerate(headers):
            label = ctk.CTkLabel(
                header_bg,
                text=header,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#1e293b",
                fg_color="transparent",
                anchor="w" if col < 2 else "center",
                corner_radius=0
            )
            label.grid(row=0, column=col, sticky="ew", padx=(20 if col == 0 else 15, 15), pady=10)
        
        # Configure header grid weights
        for i in range(6):
            header_bg.grid_columnconfigure(i, weight=1)
        
        # Add separator line
        separator = ctk.CTkFrame(self.menu_items_frame, fg_color="#e2e8f0", height=1, corner_radius=0)
        separator.grid(row=1, column=0, columnspan=6, sticky="ew", padx=10)
        
        # Load menu items
        self.load_menu_items()
    
    def load_menu_items(self):
        # Clear existing menu items (except header)
        for widget in self.menu_items_frame.winfo_children():
            if not isinstance(widget, ctk.CTkFrame):  # Preserve header and separator
                widget.destroy()
        
        # Get menu items from database
        db = SessionLocal()
        try:
            menu_items = db.query(MenuItem).order_by(MenuItem.name).all()
            
            for idx, item in enumerate(menu_items, 2):
                # Name
                ctk.CTkLabel(
                    self.menu_items_frame,
                    text=item.name,
                    font=ctk.CTkFont(size=13),
                    text_color="#1e293b",
                    anchor="w",
                    fg_color="#f8fafc" if idx % 2 == 0 else "white",
                    corner_radius=0
                ).grid(row=idx, column=0, sticky="ew", padx=(20, 10), pady=10)
                
                # Description
                ctk.CTkLabel(
                    self.menu_items_frame,
                    text=item.description[:50] + "..." if len(item.description) > 50 else item.description,
                    font=ctk.CTkFont(size=13),
                    text_color="#64748b",
                    anchor="w",
                    fg_color="#f8fafc" if idx % 2 == 0 else "white",
                    corner_radius=0
                ).grid(row=idx, column=1, sticky="ew", padx=10, pady=10)
                
                # Price
                ctk.CTkLabel(
                    self.menu_items_frame,
                    text=f"Rs. {item.price:,.0f}",
                    font=ctk.CTkFont(size=13),
                    text_color="#1e293b",
                    anchor="center",
                    fg_color="#f8fafc" if idx % 2 == 0 else "white",
                    corner_radius=0
                ).grid(row=idx, column=2, sticky="ew", padx=10, pady=10)
                
                # Category
                category_frame = ctk.CTkFrame(
                    self.menu_items_frame,
                    fg_color="#f8fafc" if idx % 2 == 0 else "white",
                    corner_radius=0
                )
                category_frame.grid(row=idx, column=3, sticky="ew", padx=10, pady=10)
                
                ctk.CTkLabel(
                    category_frame,
                    text=item.category,
                    font=ctk.CTkFont(size=13),
                    fg_color="white",
                    text_color="#475569",
                    corner_radius=0,
                    height=28
                ).pack(expand=True, pady=5)
                
                # Available
                switch_frame = ctk.CTkFrame(
                    self.menu_items_frame,
                    fg_color="#f8fafc" if idx % 2 == 0 else "white",
                    corner_radius=0
                )
                switch_frame.grid(row=idx, column=4, sticky="ew", padx=10, pady=10)
                
                switch_var = ctk.BooleanVar(value=bool(item.available))
                switch = ctk.CTkSwitch(
                    switch_frame,
                    text="",
                    variable=switch_var,
                    command=lambda i=item, v=switch_var: self.toggle_availability(i, v),
                    width=40,
                    height=20,
                    progress_color="#059669",
                    button_color="#ffffff",
                    button_hover_color="#f1f5f9"
                )
                switch.pack(expand=True, pady=5)
                
                # Actions
                actions_frame = ctk.CTkFrame(
                    self.menu_items_frame,
                    fg_color="#f8fafc" if idx % 2 == 0 else "white",
                    corner_radius=0
                )
                actions_frame.grid(row=idx, column=5, sticky="ew", padx=10, pady=10)
                
                buttons_frame = ctk.CTkFrame(actions_frame, fg_color="transparent")
                buttons_frame.pack(expand=True, pady=5)
                
                ctk.CTkButton(
                    buttons_frame,
                    text="Edit",
                    command=lambda i=item: self.show_edit_item_dialog(i),
                    font=ctk.CTkFont(size=13),
                    fg_color="#0ea5e9",
                    hover_color="#0284c7",
                    width=60,
                    height=28
                ).pack(side="left", padx=2)
                
                ctk.CTkButton(
                    buttons_frame,
                    text="Delete",
                    command=lambda i=item: self.delete_item(i),
                    font=ctk.CTkFont(size=13),
                    fg_color="#ef4444",
                    hover_color="#dc2626",
                    width=60,
                    height=28
                ).pack(side="left", padx=2)
        
        finally:
            db.close()
    
    def toggle_availability(self, item, var):
        db = SessionLocal()
        try:
            db_item = db.query(MenuItem).filter(MenuItem.id == item.id).first()
            if db_item:
                db_item.available = var.get()
                db.commit()
                messagebox.showinfo("Success", f"{item.name} {'enabled' if var.get() else 'disabled'} successfully!")
        finally:
            db.close()
    
    def show_add_item_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Add Menu Item")
        dialog.geometry("500x600")
        dialog.grab_set()  # Make the dialog modal
        
        dialog.grid_columnconfigure(1, weight=1)
        
        # Create form fields
        ctk.CTkLabel(
            dialog,
            text="Add New Menu Item",
            font=ctk.CTkFont(size=20, weight="bold")
        ).grid(row=0, column=0, columnspan=2, pady=20)
        
        # Name
        ctk.CTkLabel(dialog, text="Name:").grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")
        name_var = ctk.StringVar()
        name_entry = ctk.CTkEntry(dialog, textvariable=name_var)
        name_entry.grid(row=1, column=1, padx=10, pady=(10, 0), sticky="ew")
        
        # Description
        ctk.CTkLabel(dialog, text="Description:").grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")
        description_var = ctk.StringVar()
        description_entry = ctk.CTkEntry(dialog, textvariable=description_var)
        description_entry.grid(row=2, column=1, padx=10, pady=(10, 0), sticky="ew")
        
        # Price
        ctk.CTkLabel(dialog, text="Price:").grid(row=3, column=0, padx=10, pady=(10, 0), sticky="w")
        price_var = ctk.StringVar()
        price_entry = ctk.CTkEntry(dialog, textvariable=price_var)
        price_entry.grid(row=3, column=1, padx=10, pady=(10, 0), sticky="ew")
        
        # Category
        ctk.CTkLabel(dialog, text="Category:").grid(row=4, column=0, padx=10, pady=(10, 0), sticky="w")
        category_var = ctk.StringVar()
        categories = ["Main Course", "Appetizer", "Dessert", "Beverage"]
        category_combobox = ctk.CTkComboBox(dialog, values=categories, variable=category_var)
        category_combobox.grid(row=4, column=1, padx=10, pady=(10, 0), sticky="ew")
        
        # Available
        available_var = ctk.BooleanVar(value=True)
        available_switch = ctk.CTkSwitch(dialog, text="Available", variable=available_var)
        available_switch.grid(row=5, column=0, columnspan=2, padx=10, pady=(10, 0))
        
        def save_item():
            try:
                # Validate inputs
                name = name_var.get().strip()
                description = description_var.get().strip()
                price = price_var.get().strip()
                category = category_var.get().strip()
                
                if not all([name, description, price, category]):
                    messagebox.showerror("Error", "Please fill in all fields")
                    return
                
                try:
                    price = float(price)
                except ValueError:
                    messagebox.showerror("Error", "Price must be a number")
                    return
                
                # Create new menu item
                db = SessionLocal()
                try:
                    new_item = MenuItem(
                        name=name,
                        description=description,
                        price=price,
                        category=category,
                        available=1 if available_var.get() else 0
                    )
                    db.add(new_item)
                    db.commit()
                    
                    messagebox.showinfo("Success", "Menu item added successfully!")
                    dialog.destroy()
                    self.load_menu_items()  # Refresh the list
                finally:
                    db.close()
                    
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        # Add save button
        save_btn = ctk.CTkButton(dialog, text="Save", command=save_item)
        save_btn.grid(row=6, column=0, columnspan=2, padx=10, pady=20)
    
    def show_edit_item_dialog(self, item):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Edit Menu Item")
        dialog.geometry("500x600")
        dialog.grab_set()  # Make the dialog modal
        
        dialog.grid_columnconfigure(1, weight=1)
        
        # Create form fields
        ctk.CTkLabel(
            dialog,
            text="Edit Menu Item",
            font=ctk.CTkFont(size=20, weight="bold")
        ).grid(row=0, column=0, columnspan=2, pady=20)
        
        # Name
        ctk.CTkLabel(dialog, text="Name:").grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")
        name_var = ctk.StringVar(value=item.name)
        name_entry = ctk.CTkEntry(dialog, textvariable=name_var)
        name_entry.grid(row=1, column=1, padx=10, pady=(10, 0), sticky="ew")
        
        # Description
        ctk.CTkLabel(dialog, text="Description:").grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")
        description_var = ctk.StringVar(value=item.description)
        description_entry = ctk.CTkEntry(dialog, textvariable=description_var)
        description_entry.grid(row=2, column=1, padx=10, pady=(10, 0), sticky="ew")
        
        # Price
        ctk.CTkLabel(dialog, text="Price:").grid(row=3, column=0, padx=10, pady=(10, 0), sticky="w")
        price_var = ctk.StringVar(value=str(item.price))
        price_entry = ctk.CTkEntry(dialog, textvariable=price_var)
        price_entry.grid(row=3, column=1, padx=10, pady=(10, 0), sticky="ew")
        
        # Category
        ctk.CTkLabel(dialog, text="Category:").grid(row=4, column=0, padx=10, pady=(10, 0), sticky="w")
        category_var = ctk.StringVar(value=item.category)
        categories = ["Main Course", "Appetizer", "Dessert", "Beverage"]
        category_combobox = ctk.CTkComboBox(dialog, values=categories, variable=category_var)
        category_combobox.grid(row=4, column=1, padx=10, pady=(10, 0), sticky="ew")
        
        # Available
        available_var = ctk.BooleanVar(value=item.available)
        available_switch = ctk.CTkSwitch(dialog, text="Available", variable=available_var)
        available_switch.grid(row=5, column=0, columnspan=2, padx=10, pady=(10, 0))
        
        def save_changes():
            try:
                # Validate inputs
                name = name_var.get().strip()
                description = description_var.get().strip()
                price = price_var.get().strip()
                category = category_var.get().strip()
                
                if not all([name, description, price, category]):
                    messagebox.showerror("Error", "Please fill in all fields")
                    return
                
                try:
                    price = float(price)
                except ValueError:
                    messagebox.showerror("Error", "Price must be a number")
                    return
                
                # Update menu item
                db = SessionLocal()
                try:
                    db_item = db.query(MenuItem).filter(MenuItem.id == item.id).first()
                    if db_item:
                        db_item.name = name
                        db_item.description = description
                        db_item.price = price
                        db_item.category = category
                        db_item.available = 1 if available_var.get() else 0
                        
                        db.commit()
                        
                        messagebox.showinfo("Success", "Menu item updated successfully!")
                        dialog.destroy()
                        self.load_menu_items()  # Refresh the list
                finally:
                    db.close()
                    
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        # Add save button
        save_btn = ctk.CTkButton(dialog, text="Save Changes", command=save_changes)
        save_btn.grid(row=6, column=0, columnspan=2, padx=10, pady=20)
    
    def delete_item(self, item):
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {item.name}?"):
            db = SessionLocal()
            try:
                db_item = db.query(MenuItem).filter(MenuItem.id == item.id).first()
                if db_item:
                    db.delete(db_item)
                    db.commit()
                    messagebox.showinfo("Success", "Menu item deleted successfully!")
                    self.load_menu_items()  # Refresh the list
            finally:
                db.close()
