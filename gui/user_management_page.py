import customtkinter as ctk
from .admin_base_page import AdminBasePage
from database.config import SessionLocal
from database.models import User, UserRole
from database.utils import create_user
from tkinter import messagebox
import datetime

class UserManagementPage(AdminBasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        # Configure grid
        self.right_panel.grid_columnconfigure(0, weight=1)
        self.right_panel.grid_rowconfigure(0, weight=1)
        
        # Create main content frame
        self.content_frame = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        self.content_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)
        
        # Create top bar with title and add button
        self.top_bar = ctk.CTkFrame(
            self.content_frame,
            fg_color="#059669",
            corner_radius=10
        )
        self.top_bar.grid(row=0, column=0, sticky="ew", padx=10, pady=(0, 20))
        self.top_bar.grid_columnconfigure(1, weight=1)  # For spacing between title and button
        
        # Title with subtitle
        title_frame = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="w", padx=20, pady=15)
        
        ctk.CTkLabel(
            title_frame,
            text="User Management",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="white"
        ).grid(row=0, column=0, sticky="w")
        
        ctk.CTkLabel(
            title_frame,
            text="Manage your cafeteria's users and roles",
            font=ctk.CTkFont(size=14),
            text_color="#e2e8f0"
        ).grid(row=1, column=0, sticky="w", pady=(2, 0))
        
        # Create filters frame with white background
        self.filters_frame = ctk.CTkFrame(
            self.top_bar,
            fg_color="white",
            corner_radius=8,
            height=45  # Fixed height for better appearance
        )
        self.filters_frame.grid(row=0, column=1, sticky="e", padx=20, pady=10)
        self.filters_frame.grid_propagate(False)  # Maintain fixed height
        
        # Role filter
        role_frame = ctk.CTkFrame(self.filters_frame, fg_color="transparent")
        role_frame.pack(side="left", padx=15, pady=5)
        
        ctk.CTkLabel(
            role_frame,
            text="Filter by Role:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#475569"
        ).pack(side="left", padx=(0, 8))
        
        self.role_var = ctk.StringVar(value="All")
        self.role_filter = ctk.CTkComboBox(
            role_frame,
            values=["All"] + [role.value.capitalize() for role in UserRole],
            variable=self.role_var,
            command=self.on_role_change,
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
        self.role_filter.pack(side="left")
        
        # Add User button
        self.add_user_button = ctk.CTkButton(
            self.top_bar,
            text="+ Add New User",
            command=self.show_add_user_dialog,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            fg_color="#ffffff",
            text_color="#059669",
            hover_color="#e2e8f0"
        )
        self.add_user_button.grid(row=0, column=2, sticky="e", padx=20)
        
        # Create users frame with modern styling
        self.users_frame = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="white",
            corner_radius=8,
            width=1200  # Make it wider to show scrollbar
        )
        self.users_frame.grid(row=1, column=0, sticky="nsew", padx=10)
        
        # Configure grid columns for perfect alignment
        self.users_frame.grid_columnconfigure(0, weight=2)  # Username
        self.users_frame.grid_columnconfigure(1, weight=3)  # Email
        self.users_frame.grid_columnconfigure(2, weight=1)  # Role
        self.users_frame.grid_columnconfigure(3, weight=2)  # Created
        self.users_frame.grid_columnconfigure(4, weight=2)  # Actions
        
        # Create headers with consistent styling
        headers = ["Username", "Email", "Role", "Created", "Actions"]
        
        # Create header background
        header_bg = ctk.CTkFrame(self.users_frame, fg_color="#f8fafc", height=40, corner_radius=0)
        header_bg.grid(row=0, column=0, columnspan=5, sticky="ew")
        header_bg.grid_propagate(False)
        
        # Configure header grid weights
        for i in range(5):
            header_bg.grid_columnconfigure(i, weight=1 if i != 1 else 2)  # Email column wider
        
        # Add header labels
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
        
        # Add separator line
        separator = ctk.CTkFrame(self.users_frame, fg_color="#e2e8f0", height=1, corner_radius=0)
        separator.grid(row=1, column=0, columnspan=5, sticky="ew", padx=10)
        
        # Load users
        self.load_users()
    
    def load_users(self, *args):
        """Initial load and refresh of users"""
        self.on_role_change()
    
    def on_role_change(self, choice=None):
        """Handle role filter change with loading animation"""
        # Update loading state
        self.role_filter.configure(state="disabled")
        
        try:
            # Clear existing users (except header and separator)
            for widget in self.users_frame.winfo_children():
                if isinstance(widget, ctk.CTkLabel) or (isinstance(widget, ctk.CTkFrame) and widget not in [self.users_frame.winfo_children()[0], self.users_frame.winfo_children()[1]]):
                    widget.destroy()
            
            # Get users from database
            db = SessionLocal()
            try:
                query = db.query(User).order_by(User.created_at.desc())
                
                # Apply role filter
                role_filter = self.role_var.get()
                if role_filter != "All":
                    query = query.filter(User.role == UserRole[role_filter.upper()])
                
                users = query.all()
                
                # Show "No users found" message if no results
                if not users:
                    no_results_frame = ctk.CTkFrame(self.users_frame, fg_color="white", height=100)
                    no_results_frame.grid(row=2, column=0, columnspan=5, sticky="ew", padx=20, pady=20)
                    no_results_frame.grid_propagate(False)
                    
                    message = f"No users found" if role_filter == "All" else f"No {role_filter.lower()} users found"
                    ctk.CTkLabel(
                        no_results_frame,
                        text=message,
                        font=ctk.CTkFont(size=13),
                        text_color="#64748b"
                    ).place(relx=0.5, rely=0.5, anchor="center")
                    return
                
                # Create content rows
                for idx, user in enumerate(users, 2):
                    row_bg = "#f8fafc" if idx % 2 == 0 else "white"
                    
                    # Username
                    ctk.CTkLabel(
                        self.users_frame,
                        text=user.username,
                        font=ctk.CTkFont(size=13),
                        text_color="#1e293b",
                        anchor="w",
                        fg_color=row_bg,
                        corner_radius=0
                    ).grid(row=idx, column=0, sticky="ew", padx=(20, 15), pady=10)
                    
                    # Email
                    ctk.CTkLabel(
                        self.users_frame,
                        text=user.email,
                        font=ctk.CTkFont(size=13),
                        text_color="#64748b",
                        anchor="w",
                        fg_color=row_bg,
                        corner_radius=0
                    ).grid(row=idx, column=1, sticky="ew", padx=15, pady=10)
                    
                    # Role with badge styling
                    role_frame = ctk.CTkFrame(
                        self.users_frame,
                        fg_color=row_bg,
                        corner_radius=0
                    )
                    role_frame.grid(row=idx, column=2, sticky="ew", padx=15, pady=10)
                    
                    # Different colors for different roles
                    role_colors = {
                        UserRole.CUSTOMER: ("#059669", "#ecfdf5"),  # Green
                        UserRole.STAFF: ("#0284c7", "#e0f2fe"),    # Blue
                        UserRole.ADMIN: ("#7c3aed", "#f3e8ff")     # Purple
                    }
                    role_color, role_bg = role_colors.get(user.role, ("#64748b", "#f1f5f9"))
                    
                    role_badge = ctk.CTkFrame(
                        role_frame,
                        fg_color=role_bg,
                        corner_radius=4
                    )
                    role_badge.pack(expand=True, pady=5)
                    
                    ctk.CTkLabel(
                        role_badge,
                        text=user.role.value.capitalize(),
                        font=ctk.CTkFont(size=13),
                        text_color=role_color,
                        width=80,
                        height=28
                    ).pack(expand=True, padx=10)
                    
                    # Created Date
                    ctk.CTkLabel(
                        self.users_frame,
                        text=user.created_at.strftime("%Y-%m-%d"),
                        font=ctk.CTkFont(size=13),
                        text_color="#1e293b",
                        anchor="center",
                        fg_color=row_bg,
                        corner_radius=0
                    ).grid(row=idx, column=3, sticky="ew", padx=15, pady=10)
                    
                    # Actions
                    actions_frame = ctk.CTkFrame(
                        self.users_frame,
                        fg_color=row_bg,
                        corner_radius=0
                    )
                    actions_frame.grid(row=idx, column=4, sticky="ew", padx=15, pady=10)
                    
                    buttons_frame = ctk.CTkFrame(actions_frame, fg_color="transparent")
                    buttons_frame.pack(expand=True, pady=5)
                    
                    ctk.CTkButton(
                        buttons_frame,
                        text="Edit",
                        command=lambda u=user: self.show_edit_user_dialog(u),
                        font=ctk.CTkFont(size=13),
                        fg_color="#0ea5e9",
                        hover_color="#0284c7",
                        width=60,
                        height=28
                    ).pack(side="left", padx=2)
                    
                    ctk.CTkButton(
                        buttons_frame,
                        text="Delete",
                        command=lambda u=user: self.delete_user(u),
                        font=ctk.CTkFont(size=13),
                        fg_color="#ef4444",
                        hover_color="#dc2626",
                        width=60,
                        height=28
                    ).pack(side="left", padx=2)
            
            finally:
                db.close()
        
        finally:
            # Re-enable the filter
            self.role_filter.configure(state="normal")
    
    def show_add_user_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Add User")
        dialog.geometry("450x600")
        dialog.grab_set()
        
        # Main container with padding
        container = ctk.CTkFrame(dialog, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Title with icon
        title_frame = ctk.CTkFrame(container, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 30))
        
        ctk.CTkLabel(
            title_frame,
            text="👤",  # User icon
            font=ctk.CTkFont(size=32)
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(
            title_frame,
            text="Add New User",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(side="left")
        
        # Form fields with better spacing and styling
        form_frame = ctk.CTkFrame(container, fg_color="transparent")
        form_frame.pack(fill="x", pady=10)
        
        # Username field
        username_var = ctk.StringVar()
        ctk.CTkLabel(
            form_frame,
            text="Username",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#495057"
        ).pack(anchor="w", pady=(0, 5))
        
        username_entry = ctk.CTkEntry(
            form_frame,
            textvariable=username_var,
            height=40,
            placeholder_text="Enter username",
            font=ctk.CTkFont(size=13)
        )
        username_entry.pack(fill="x", pady=(0, 15))
        
        # Email field
        email_var = ctk.StringVar()
        ctk.CTkLabel(
            form_frame,
            text="Email",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#495057"
        ).pack(anchor="w", pady=(0, 5))
        
        email_entry = ctk.CTkEntry(
            form_frame,
            textvariable=email_var,
            height=40,
            placeholder_text="Enter email address",
            font=ctk.CTkFont(size=13)
        )
        email_entry.pack(fill="x", pady=(0, 15))
        
        # Password field
        password_var = ctk.StringVar()
        ctk.CTkLabel(
            form_frame,
            text="Password",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#495057"
        ).pack(anchor="w", pady=(0, 5))
        
        password_entry = ctk.CTkEntry(
            form_frame,
            textvariable=password_var,
            height=40,
            placeholder_text="Enter password",
            show="•",
            font=ctk.CTkFont(size=13)
        )
        password_entry.pack(fill="x", pady=(0, 15))
        
        # Role selection
        role_var = ctk.StringVar()
        ctk.CTkLabel(
            form_frame,
            text="Role",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#495057"
        ).pack(anchor="w", pady=(0, 5))
        
        roles = ["Customer", "Staff", "Admin"]
        role_combobox = ctk.CTkComboBox(
            form_frame,
            values=roles,
            variable=role_var,
            height=40,
            font=ctk.CTkFont(size=13),
            dropdown_font=ctk.CTkFont(size=13)
        )
        role_combobox.pack(fill="x", pady=(0, 30))
        role_combobox.set("Customer")  # Default role
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.pack(fill="x")
        
        # Cancel button
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            command=dialog.destroy,
            fg_color="#6c757d",
            hover_color="#5a6268",
            height=40,
            font=ctk.CTkFont(size=14),
            width=120
        )
        cancel_btn.pack(side="left", padx=(0, 10))
        
        # Save button
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="Save User",
            command=lambda: save_user(),
            fg_color="#059669",  # Match sidebar green
            hover_color="#047857",  # Darker shade for hover
            height=40,
            font=ctk.CTkFont(size=14),
            width=120
        )
        save_btn.pack(side="left")
        
        def save_user():
            try:
                # Validate inputs
                username = username_var.get().strip()
                email = email_var.get().strip()
                password = password_var.get().strip()
                role = role_var.get().strip()
                
                if not all([username, email, password, role]):
                    messagebox.showerror(
                        "Required Fields",
                        "Please fill in all required fields",
                        parent=dialog
                    )
                    return
                
                # Create new user
                db = SessionLocal()
                try:
                    # Check if username or email already exists
                    existing_user = db.query(User).filter(
                        (User.username == username) | (User.email == email)
                    ).first()
                    
                    if existing_user:
                        messagebox.showerror(
                            "Duplicate User",
                            "Username or email already exists",
                            parent=dialog
                        )
                        return
                    
                    new_user = create_user(
                        db=db,
                        username=username,
                        email=email,
                        password=password,
                        role=UserRole[role.upper()]
                    )
                    
                    messagebox.showinfo(
                        "Success",
                        "User added successfully!",
                        parent=dialog
                    )
                    dialog.destroy()
                    self.load_users()
                finally:
                    db.close()
                    
            except Exception as e:
                messagebox.showerror(
                    "Error",
                    str(e),
                    parent=dialog
                )
    
    def show_edit_user_dialog(self, user):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Edit User")
        dialog.geometry("450x600")
        dialog.grab_set()
        
        # Main container with padding
        container = ctk.CTkFrame(dialog, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Title with icon
        title_frame = ctk.CTkFrame(container, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 30))
        
        ctk.CTkLabel(
            title_frame,
            text="✏️",  # Edit icon
            font=ctk.CTkFont(size=32)
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(
            title_frame,
            text=f"Edit User: {user.username}",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(side="left")
        
        # Form fields
        form_frame = ctk.CTkFrame(container, fg_color="transparent")
        form_frame.pack(fill="x", pady=10)
        
        # Email field
        email_var = ctk.StringVar(value=user.email)
        ctk.CTkLabel(
            form_frame,
            text="Email",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#495057"
        ).pack(anchor="w", pady=(0, 5))
        
        email_entry = ctk.CTkEntry(
            form_frame,
            textvariable=email_var,
            height=40,
            placeholder_text="Enter email address",
            font=ctk.CTkFont(size=13)
        )
        email_entry.pack(fill="x", pady=(0, 15))
        
        # Password field (optional)
        password_var = ctk.StringVar()
        ctk.CTkLabel(
            form_frame,
            text="New Password (optional)",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#495057"
        ).pack(anchor="w", pady=(0, 5))
        
        password_entry = ctk.CTkEntry(
            form_frame,
            textvariable=password_var,
            height=40,
            placeholder_text="Leave blank to keep current password",
            show="•",
            font=ctk.CTkFont(size=13)
        )
        password_entry.pack(fill="x", pady=(0, 15))
        
        # Role selection
        role_var = ctk.StringVar(value=user.role.name.capitalize())
        ctk.CTkLabel(
            form_frame,
            text="Role",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#495057"
        ).pack(anchor="w", pady=(0, 5))
        
        roles = ["Customer", "Staff", "Admin"]
        role_combobox = ctk.CTkComboBox(
            form_frame,
            values=roles,
            variable=role_var,
            height=40,
            font=ctk.CTkFont(size=13),
            dropdown_font=ctk.CTkFont(size=13),
            state="readonly" if user.role == UserRole.ADMIN else "normal"
        )
        role_combobox.pack(fill="x", pady=(0, 30))
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.pack(fill="x")
        
        # Cancel button
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            command=dialog.destroy,
            fg_color="#6c757d",
            hover_color="#5a6268",
            height=40,
            font=ctk.CTkFont(size=14),
            width=120
        )
        cancel_btn.pack(side="left", padx=(0, 10))
        
        # Save button
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="Save Changes",
            command=lambda: save_changes(),
            fg_color="#059669",  # Match sidebar green
            hover_color="#047857",  # Darker shade for hover
            height=40,
            font=ctk.CTkFont(size=14),
            width=120
        )
        save_btn.pack(side="left")
        
        def save_changes():
            try:
                # Validate inputs
                email = email_var.get().strip()
                password = password_var.get().strip()
                role = role_var.get().strip()
                
                if not email:
                    messagebox.showerror(
                        "Required Fields",
                        "Email is required",
                        parent=dialog
                    )
                    return
                
                db = SessionLocal()
                try:
                    # Check if email already exists (excluding current user)
                    existing_user = db.query(User).filter(
                        (User.email == email) & (User.id != user.id)
                    ).first()
                    
                    if existing_user:
                        messagebox.showerror(
                            "Duplicate Email",
                            "Email already exists",
                            parent=dialog
                        )
                        return
                    
                    # Update user
                    user_to_update = db.query(User).get(user.id)
                    if user_to_update:
                        user_to_update.email = email
                        if password:
                            user_to_update.set_password(password)
                        if user_to_update.role != UserRole.ADMIN:
                            user_to_update.role = UserRole[role.upper()]
                        
                        db.commit()
                        messagebox.showinfo(
                            "Success",
                            "User updated successfully!",
                            parent=dialog
                        )
                        dialog.destroy()
                        self.load_users()
                finally:
                    db.close()
                    
            except Exception as e:
                messagebox.showerror(
                    "Error",
                    str(e),
                    parent=dialog
                )
    
    def delete_user(self, user):
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete user {user.username}?"):
            db = SessionLocal()
            try:
                db_user = db.query(User).filter(User.id == user.id).first()
                if db_user:
                    if db_user.role == UserRole.ADMIN:
                        messagebox.showerror("Error", "Cannot delete admin users")
                        return
                    
                    db.delete(db_user)
                    db.commit()
                    messagebox.showinfo("Success", "User deleted successfully!")
                    self.load_users()  # Refresh the list
            finally:
                db.close()
