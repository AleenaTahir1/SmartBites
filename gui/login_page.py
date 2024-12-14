import os
import re
import customtkinter as ctk
from PIL import Image
from tkinter import font
from .base_page import BasePage
from .constants import *
from database.config import SessionLocal
from database.utils import authenticate_user

class LoginPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        # Check available fonts
        try:
            available_fonts = font.families()
            modern_fonts = ["Segoe UI", "Verdana", "Tahoma", "Century Gothic", "Calibri"]
            
            # Find the first available modern font
            for modern_font in modern_fonts:
                if modern_font in available_fonts:
                    global LOGO_FONT
                    LOGO_FONT = modern_font
                    print(f"Using font: {modern_font}")
                    break
        except Exception as e:
            print(f"Error checking fonts: {e}")
        
        self.configure(fg_color=BG_COLOR)
        
        # Create main container
        self.container = ctk.CTkFrame(
            self,
            fg_color=BG_COLOR,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT
        )
        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        
        # Left side with logo and wave background
        self.left_frame = ctk.CTkFrame(
            self.container,
            fg_color=PRIMARY_COLOR,
            width=WINDOW_WIDTH//2,
            height=WINDOW_HEIGHT
        )
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        self.left_frame.grid_propagate(False)
        
        # Load and display logo
        try:
            logo_path = os.path.join("assets", "images", "myLogo.png")
            self.logo_image = ctk.CTkImage(
                light_image=Image.open(logo_path),
                dark_image=Image.open(logo_path),
                size=(200, 200)  # Changed from 300x300 to 200x200 to match signup page
            )
            self.logo_label = ctk.CTkLabel(
                self.left_frame,
                image=self.logo_image,
                text=""
            )
            self.logo_label.place(relx=0.5, rely=0.35, anchor="center")
            
            # Add app name below logo
            self.app_name = ctk.CTkLabel(
                self.left_frame,
                text="SmartBites",
                font=(LOGO_FONT, 40, "bold"),
                text_color=BG_COLOR
            )
            self.app_name.place(relx=0.5, rely=0.6, anchor="center")
            
            # Add slogan below app name
            self.slogan = ctk.CTkLabel(
                self.left_frame,
                text="Smart Choice, Faster Bites!",
                font=(SLOGAN_FONT, NORMAL_TEXT_SIZE, "bold"),
                text_color=BG_COLOR
            )
            self.slogan.place(relx=0.5, rely=0.7, anchor="center")
            
        except Exception as e:
            print(f"Error loading logo: {e}")
        
        # Right side with login form
        self.right_frame = ctk.CTkFrame(
            self.container,
            fg_color=BG_COLOR,
            width=WINDOW_WIDTH//2,
            height=WINDOW_HEIGHT
        )
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        
        # Login form container
        self.login_container = ctk.CTkFrame(
            self.right_frame,
            fg_color=BG_COLOR,
            width=LOGIN_WIDTH
        )
        self.login_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Welcome text
        self.welcome_label = ctk.CTkLabel(
            self.login_container,
            text="Welcome",
            font=(FONT_FAMILY, HEADING_SIZE, "bold"),
            text_color=TEXT_COLOR
        )
        self.welcome_label.pack(pady=(0, 5))
        
        self.subtitle_label = ctk.CTkLabel(
            self.login_container,
            text="Login in to your account to continue",
            font=(FONT_FAMILY, SUBHEADING_SIZE),
            text_color=NEUTRAL_COLOR
        )
        self.subtitle_label.pack(pady=(0, 20))
        
        # Username input with icon
        self.username_frame = ctk.CTkFrame(
            self.login_container,
            fg_color=INPUT_BG_COLOR,
            corner_radius=CORNER_RADIUS,
            height=INPUT_HEIGHT
        )
        self.username_frame.pack(fill="x", pady=(0, 5))
        self.username_frame.pack_propagate(False)
        
        # Username icon
        self.username_icon = ctk.CTkLabel(
            self.username_frame,
            text="👤",
            font=(FONT_FAMILY, NORMAL_TEXT_SIZE),
            text_color=NEUTRAL_COLOR
        )
        self.username_icon.place(relx=0.02, rely=0.5, anchor="w")
        
        self.username_entry = ctk.CTkEntry(
            self.username_frame,
            placeholder_text="Username",
            placeholder_text_color=PLACEHOLDER_COLOR,
            font=(FONT_FAMILY, NORMAL_TEXT_SIZE),
            fg_color=INPUT_BG_COLOR,
            border_width=0,
            corner_radius=0
        )
        self.username_entry.place(relx=0.3, rely=0.5, relwidth=0.68, anchor="w")
        
        # Password input with icon and show/hide toggle
        self.password_frame = ctk.CTkFrame(
            self.login_container,
            fg_color=INPUT_BG_COLOR,
            corner_radius=CORNER_RADIUS,
            height=INPUT_HEIGHT
        )
        self.password_frame.pack(fill="x", pady=(0, 5))
        self.password_frame.pack_propagate(False)
        
        # Password icon
        self.password_icon = ctk.CTkLabel(
            self.password_frame,
            text="🔑",
            font=(FONT_FAMILY, NORMAL_TEXT_SIZE),
            text_color=NEUTRAL_COLOR
        )
        self.password_icon.place(relx=0.02, rely=0.5, anchor="w")
        
        self.password_entry = ctk.CTkEntry(
            self.password_frame,
            placeholder_text="Password",
            placeholder_text_color=PLACEHOLDER_COLOR,
            font=(FONT_FAMILY, NORMAL_TEXT_SIZE),
            fg_color=INPUT_BG_COLOR,
            border_width=0,
            corner_radius=0,
            show="●"
        )
        self.password_entry.place(relx=0.3, rely=0.5, relwidth=0.58, anchor="w")
        
        # Show/Hide password button
        self.show_password = False
        self.toggle_password_btn = ctk.CTkButton(
            self.password_frame,
            text="👁",
            width=30,
            height=30,
            fg_color="transparent",
            hover_color=NEUTRAL_COLOR,
            text_color=TEXT_COLOR,
            command=self.toggle_password_visibility
        )
        self.toggle_password_btn.place(relx=0.95, rely=0.5, anchor="e")
        
        # Error message label - Right below password field
        self.error_label = ctk.CTkLabel(
            self.login_container,
            text="Password must be at least 6 characters long",
            text_color="red",
            font=(FONT_FAMILY, SMALL_TEXT_SIZE),
            fg_color="transparent"
        )
        self.error_label.pack(pady=(0, 5))
        self.error_label.pack_forget()
        
        # Forgot password link
        self.forgot_password_btn = ctk.CTkButton(
            self.login_container,
            text="Forgot your password?",
            font=(FONT_FAMILY, SMALL_TEXT_SIZE),
            fg_color=BG_COLOR,
            hover_color=INPUT_BG_COLOR,
            text_color=ACCENT_COLOR,
            command=self.forgot_password
        )
        self.forgot_password_btn.pack(anchor="e", pady=(5, 20))
        
        # Login button
        self.login_button = ctk.CTkButton(
            self.login_container,
            text="LOG IN",
            font=(FONT_FAMILY, NORMAL_TEXT_SIZE, "bold"),
            fg_color=PRIMARY_COLOR,
            text_color="#FFFFFF",  
            hover_color=SECONDARY_COLOR,
            height=BUTTON_HEIGHT,
            corner_radius=CORNER_RADIUS,
            command=self.login
        )
        self.login_button.pack(fill="x", pady=(0, 20))  # Reduced top padding
        
        # Sign Up section
        self.signup_label = ctk.CTkLabel(
            self.login_container,
            text="Don't have an account?",
            font=(FONT_FAMILY, SMALL_TEXT_SIZE),
            text_color=TEXT_COLOR
        )
        self.signup_label.pack(pady=(0, 5))

        self.signup_button = ctk.CTkButton(
            self.login_container,
            text="SIGN UP",
            font=(FONT_FAMILY, NORMAL_TEXT_SIZE, "bold"),
            fg_color=PRIMARY_COLOR,
            text_color="#FFFFFF",  
            hover_color=SECONDARY_COLOR,
            command=self.show_signup
        )
        self.signup_button.pack(fill="x", pady=(0, 20))
        
        # Separator line
        self.separator_frame = ctk.CTkFrame(
            self.login_container,
            fg_color=BG_COLOR,
            height=20
        )
        self.separator_frame.pack(fill="x", pady=10)
        
        self.separator_text = ctk.CTkLabel(
            self.separator_frame,
            text="------------------------ or ------------------------",
            font=(FONT_FAMILY, SMALL_TEXT_SIZE),
            text_color=NEUTRAL_COLOR
        )
        self.separator_text.place(relx=0.5, rely=0.5, anchor="center")
        
        # Guest login option
        self.guest_btn = ctk.CTkButton(
            self.login_container,
            text="Continue as Guest",
            font=(FONT_FAMILY, NORMAL_TEXT_SIZE),
            fg_color=INPUT_BG_COLOR,
            hover_color=NEUTRAL_COLOR,
            text_color=TEXT_COLOR,
            height=BUTTON_HEIGHT,
            corner_radius=CORNER_RADIUS,
            command=self.guest_login
        )
        self.guest_btn.pack(fill="x", pady=(10, 0))

    def validate_password(self, password):
        """Validate password meets requirements"""
        if len(password) < 6:
            return False
        return True

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            self.error_label.configure(text="Please enter both username and password", text_color="red")
            self.error_label.pack(pady=(0, 5))
            return
        
        # Get database session
        db = SessionLocal()
        try:
            user = authenticate_user(db, username, password)
            if user:
                self.controller.current_user = user
                self.controller.show_home_page()
            else:
                self.error_label.configure(text="Invalid username or password", text_color="red")
                self.error_label.pack(pady=(0, 5))
        finally:
            db.close()

    def toggle_password_visibility(self):
        self.show_password = not self.show_password
        self.password_entry.configure(show="" if self.show_password else "●")
        self.toggle_password_btn.configure(text="👁" if not self.show_password else "🔒")

    def forgot_password(self):
        self.controller.show_page("ForgotPasswordPage")

    def show_signup(self):
        self.controller.show_page("SignupPage")

    def guest_login(self):
        # TODO: Implement guest login
        print("Guest login clicked")
