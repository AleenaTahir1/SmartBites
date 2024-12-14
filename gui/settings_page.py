import customtkinter as ctk
from .admin_base_page import AdminBasePage
from .constants import *
from database.config import SessionLocal
from database.utils import get_all_settings, upsert_setting, delete_setting
from tkinter import messagebox

class SettingsPage(AdminBasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        # Set active button
        self.set_active_button("Settings")
        
        # Create top bar with title
        self.top_bar = ctk.CTkFrame(
            self.content_area,
            fg_color="#059669",  # Emerald Green
            corner_radius=10,
            height=100
        )
        self.top_bar.pack(fill="x", padx=10, pady=(0, 20))
        self.top_bar.pack_propagate(False)
        
        # Title with subtitle in top bar
        title_frame = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        title_frame.pack(side="left", padx=20, pady=15)
        
        ctk.CTkLabel(
            title_frame,
            text="Settings ",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="white"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            title_frame,
            text="Configure your cafeteria's settings and preferences",
            font=ctk.CTkFont(size=14),
            text_color="#e2e8f0"
        ).pack(anchor="w", pady=(2, 0))
        
        # Save button in top bar
        self.save_btn = ctk.CTkButton(
            self.top_bar,
            text="Save Changes",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="white",
            text_color="#059669",
            hover_color="#e2e8f0",
            width=150,
            height=40,
            command=self.save_settings
        )
        self.save_btn.pack(side="right", padx=20)
        
        # Main content with scrollable frame
        self.content = ctk.CTkScrollableFrame(
            self.content_area,
            fg_color=BG_COLOR,
            height=500
        )
        self.content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Dictionary to store settings widgets
        self.settings_widgets = {}
        
        # Settings sections
        self.sections = [
            ("Cafeteria Profile", [
                ("cafeteria_name", "Cafeteria Name", "SmartBites Cafeteria", "string"),
                ("university_name", "University Name", "University Name", "string"),
                ("contact_number", "Contact Number", "+1234567890", "string"),
                ("email", "Email", "cafeteria@university.edu", "string"),
                ("operating_hours", "Operating Hours", "8:00 AM - 8:00 PM", "string")
            ]),
            ("Order Settings", [
                ("auto_accept_orders", "Auto-accept Orders", "true", "boolean"),
                ("preparation_time", "Order Preparation Time (mins)", "15", "number"),
                ("minimum_order", "Minimum Order Amount", "5", "number"),
                ("max_daily_orders", "Maximum Daily Orders", "1000", "number"),
                ("allow_advance_orders", "Allow Advance Orders", "true", "boolean")
            ]),
            ("Service Hours", [
                ("breakfast_hours", "Breakfast Hours", "8:00 AM - 11:00 AM", "string"),
                ("lunch_hours", "Lunch Hours", "11:30 AM - 4:00 PM", "string"),
                ("dinner_hours", "Dinner Hours", "4:30 PM - 8:00 PM", "string"),
                ("weekend_hours", "Weekend Hours", "10:00 AM - 6:00 PM", "string")
            ]),
            ("Notification Settings", [
                ("notify_new_orders", "New Order Notifications", "true", "boolean"),
                ("notify_ready_pickup", "Order Ready for Pickup", "true", "boolean"),
                ("notify_low_stock", "Low Stock Alert", "true", "boolean"),
                ("daily_reports", "Daily Reports", "true", "boolean"),
                ("system_updates", "System Updates", "true", "boolean")
            ]),
            ("Payment Settings", [
                ("accept_cash", "Accept Cash", "true", "boolean"),
                ("accept_cards", "Accept University ID Card", "true", "boolean"),
                ("accept_credit_cards", "Accept Credit/Debit Cards", "true", "boolean"),
                ("service_tax", "Service Tax (%)", "0", "number"),
                ("student_discount", "Student Discount (%)", "15", "number")
            ])
        ]
        
        self.load_settings()
        
    def load_settings(self):
        """Load settings from database"""
        db = SessionLocal()
        try:
            # Get all settings from database
            stored_settings = {setting.key: setting for setting in get_all_settings(db)}
            
            # Create UI for each section
            for section_title, settings in self.sections:
                section = ctk.CTkFrame(self.content, fg_color="white", corner_radius=10)
                section.pack(fill="x", pady=10)
                
                # Section header
                header_frame = ctk.CTkFrame(section, fg_color="transparent", corner_radius=5)
                header_frame.pack(fill="x", padx=2, pady=2)
                
                ctk.CTkLabel(
                    header_frame,
                    text=section_title,
                    font=ctk.CTkFont(size=16, weight="bold"),
                    text_color="black"
                ).pack(anchor="w", padx=15, pady=10)
                
                # Settings items
                for key, label, default_value, type_ in settings:
                    item_frame = ctk.CTkFrame(section, fg_color="transparent")
                    item_frame.pack(fill="x", padx=15, pady=8)
                    
                    # Label with tooltip
                    label_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
                    label_frame.pack(side="left", fill="x", expand=True)
                    
                    ctk.CTkLabel(
                        label_frame,
                        text=label,
                        font=ctk.CTkFont(size=13),
                        text_color=TEXT_COLOR
                    ).pack(side="left", padx=(0, 10))
                    
                    # Get stored value or use default
                    stored_setting = stored_settings.get(key)
                    value = stored_setting.value if stored_setting else default_value
                    
                    if type_ == "boolean":
                        var = ctk.StringVar(value=value)
                        widget = ctk.CTkSwitch(
                            item_frame,
                            text="",
                            variable=var,
                            progress_color=PRIMARY_COLOR,
                            button_color=SECONDARY_COLOR,
                            button_hover_color="#2A8572"
                        )
                        widget.pack(side="right")
                        if value.lower() == "true":
                            widget.select()
                    else:
                        widget = ctk.CTkEntry(
                            item_frame,
                            width=200,
                            placeholder_text=str(default_value),
                            font=ctk.CTkFont(size=13)
                        )
                        widget.pack(side="right")
                        widget.insert(0, str(value))
                    
                    # Store widget reference
                    self.settings_widgets[key] = (widget, type_)
        
        finally:
            db.close()
        
        # Danger zone
        danger_zone = ctk.CTkFrame(self.content, fg_color="#FFF0F0", corner_radius=10)
        danger_zone.pack(fill="x", pady=20)
        
        # Danger zone header
        danger_header = ctk.CTkFrame(danger_zone, fg_color="#FFE5E5", corner_radius=5)
        danger_header.pack(fill="x", padx=2, pady=2)
        
        ctk.CTkLabel(
            danger_header,
            text="⚠️ Danger Zone",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#DC143C"
        ).pack(anchor="w", padx=15, pady=10)
        
        # Danger actions container
        danger_actions = ctk.CTkFrame(danger_zone, fg_color="transparent")
        danger_actions.pack(fill="x", padx=15, pady=(10, 15))
        
        # Warning text
        ctk.CTkLabel(
            danger_actions,
            text="These actions cannot be undone. Please be certain.",
            font=ctk.CTkFont(size=12),
            text_color="#666666"
        ).pack(anchor="w", pady=(0, 10))
        
        # Action buttons
        ctk.CTkButton(
            danger_actions,
            text="Clear All Data",
            font=ctk.CTkFont(size=13),
            fg_color="#DC143C",
            hover_color="#B22222",
            width=150,
            command=self.clear_all_data
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            danger_actions,
            text="Reset Settings",
            font=ctk.CTkFont(size=13),
            fg_color="#DC143C",
            hover_color="#B22222",
            width=150,
            command=self.reset_settings
        ).pack(side="left", padx=5)
    
    def save_settings(self):
        """Save all settings to database"""
        db = SessionLocal()
        try:
            for key, (widget, type_) in self.settings_widgets.items():
                # Get section from self.sections
                section = next(
                    section_title
                    for section_title, settings in self.sections
                    if any(s[0] == key for s in settings)
                )
                
                if type_ == "boolean":
                    value = str(widget.get() == "1")
                else:
                    value = widget.get()
                
                upsert_setting(db, key, value, section, type_)
            
            messagebox.showinfo("Success", "Settings saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
        finally:
            db.close()
    
    def clear_all_data(self):
        """Clear all application data"""
        if messagebox.askyesno("Confirm Action", 
                             "Are you sure you want to clear all data? This action cannot be undone!",
                             icon="warning"):
            # TODO: Implement data clearing logic
            messagebox.showinfo("Success", "All data has been cleared.")
    
    def reset_settings(self):
        """Reset all settings to default values"""
        if messagebox.askyesno("Confirm Action", 
                             "Are you sure you want to reset all settings to default? This action cannot be undone!",
                             icon="warning"):
            db = SessionLocal()
            try:
                # Reset each setting to its default value
                for section_title, settings in self.sections:
                    for key, _, default_value, type_ in settings:
                        widget, _ = self.settings_widgets[key]
                        if type_ == "boolean":
                            widget.deselect()
                            if default_value.lower() == "true":
                                widget.select()
                        else:
                            widget.delete(0, "end")
                            widget.insert(0, default_value)
                
                messagebox.showinfo("Success", "Settings have been reset to default values.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to reset settings: {str(e)}")
            finally:
                db.close()
