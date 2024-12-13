import customtkinter as ctk
from .admin_base_page import AdminBasePage
from .constants import *

class SettingsPage(AdminBasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        # Set active button
        self.set_active_button("Settings")
        
        # Header
        self.header = ctk.CTkFrame(
            self.content_area,
            fg_color=PRIMARY_COLOR,
            height=60,
            corner_radius=10
        )
        self.header.pack(fill="x", padx=0, pady=(0, 20))
        
        # Save button
        self.save_btn = ctk.CTkButton(
            self.header,
            text="Save Changes",
            font=ctk.CTkFont(size=14),
            fg_color=SECONDARY_COLOR,
            hover_color="#2A8572"
        )
        self.save_btn.pack(side="right", padx=20)
        
        # Main content
        self.content = ctk.CTkFrame(self.content_area, fg_color=BG_COLOR)
        self.content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Settings sections
        sections = [
            ("Restaurant Profile", [
                ("Restaurant Name", "SmartBites Restaurant"),
                ("Branch Location", "Jl Daeng Barat"),
                ("Contact Number", "+1234567890"),
                ("Email", "contact@smartbites.com"),
                ("Operating Hours", "9:00 AM - 10:00 PM")
            ]),
            ("Order Settings", [
                ("Auto-accept Orders", True),
                ("Order Preparation Time (mins)", "30"),
                ("Minimum Order Amount", "$10"),
                ("Delivery Radius (km)", "5"),
                ("Maximum Daily Orders", "100")
            ]),
            ("Notification Settings", [
                ("New Order Notifications", True),
                ("Order Status Updates", True),
                ("Customer Reviews", True),
                ("Daily Reports", True),
                ("System Updates", True)
            ]),
            ("Payment Settings", [
                ("Accept Cash", True),
                ("Accept Cards", True),
                ("Accept Digital Wallets", True),
                ("Service Tax (%)", "10"),
                ("Delivery Fee", "$5")
            ])
        ]
        
        for section_title, settings in sections:
            section = ctk.CTkFrame(self.content, fg_color="white")
            section.pack(fill="x", pady=10)
            
            # Section header
            ctk.CTkLabel(
                section,
                text=section_title,
                font=ctk.CTkFont(size=16, weight="bold")
            ).pack(anchor="w", padx=15, pady=10)
            
            # Settings items
            for setting, value in settings:
                item_frame = ctk.CTkFrame(section, fg_color="transparent")
                item_frame.pack(fill="x", padx=15, pady=5)
                
                ctk.CTkLabel(
                    item_frame,
                    text=setting,
                    font=ctk.CTkFont(size=12)
                ).pack(side="left")
                
                if isinstance(value, bool):
                    switch = ctk.CTkSwitch(
                        item_frame,
                        text="",
                        progress_color=PRIMARY_COLOR,
                        button_color=SECONDARY_COLOR
                    )
                    switch.pack(side="right")
                    if value:
                        switch.select()
                else:
                    entry = ctk.CTkEntry(
                        item_frame,
                        width=200,
                        placeholder_text=str(value)
                    )
                    entry.pack(side="right")
                    entry.insert(0, str(value))
        
        # Danger zone
        danger_zone = ctk.CTkFrame(self.content, fg_color="#FFF0F0")
        danger_zone.pack(fill="x", pady=20)
        
        ctk.CTkLabel(
            danger_zone,
            text="Danger Zone",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#DC143C"
        ).pack(anchor="w", padx=15, pady=10)
        
        danger_actions = ctk.CTkFrame(danger_zone, fg_color="transparent")
        danger_actions.pack(fill="x", padx=15, pady=(0, 10))
        
        ctk.CTkButton(
            danger_actions,
            text="Clear All Data",
            font=ctk.CTkFont(size=12),
            fg_color="#DC143C",
            hover_color="#B22222",
            width=120
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            danger_actions,
            text="Reset Settings",
            font=ctk.CTkFont(size=12),
            fg_color="#DC143C",
            hover_color="#B22222",
            width=120
        ).pack(side="left", padx=5)
