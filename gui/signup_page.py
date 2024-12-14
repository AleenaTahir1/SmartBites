import re
import os
import customtkinter as ctk
from PIL import Image
from .base_page import BasePage
from .constants import *
from database.config import SessionLocal
from database.utils import create_user
from database.models import UserRole
from tkinter import messagebox

class SignupPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.configure(fg_color=BG_COLOR)
        
        # Create main container with two columns
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Left column for logo (1/3 width)
        self.left_frame = ctk.CTkFrame(self.main_container, fg_color=PRIMARY_COLOR)
        self.left_frame.pack(side="left", fill="both", expand=True)
        
        # Load and display logo
        try:
            logo_path = os.path.join("assets", "images", "myLogo.png")
            self.logo_image = ctk.CTkImage(
                light_image=Image.open(logo_path),
                dark_image=Image.open(logo_path),
                size=(200, 200)
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
            
            # Add description below app name
            self.description = ctk.CTkLabel(
                self.left_frame,
                text="Smart Choice, Faster Bites!",
                font=(SLOGAN_FONT, NORMAL_TEXT_SIZE, "bold"),
                text_color=BG_COLOR
            )
            self.description.place(relx=0.5, rely=0.7, anchor="center")
            
        except Exception as e:
            print(f"Error loading logo: {e}")
        
        # Right column for signup form
        self.right_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.right_frame.pack(side="left", fill="both", expand=True, padx=20)
        
        # Create Account Label
        self.create_account_label = ctk.CTkLabel(
            self.right_frame,
            text="Create Account",
            font=(FONT_FAMILY, HEADING_SIZE, "bold"),
            text_color=TEXT_COLOR
        )
        self.create_account_label.place(relx=0.5, rely=0.15, anchor="center")

        # Create Account Subtitle Label
        self.create_account_subtitle_label = ctk.CTkLabel(
            self.right_frame,
            text="Quickly to get started",
            font=(FONT_FAMILY, NORMAL_TEXT_SIZE),
            text_color=NEUTRAL_COLOR
        )
        self.create_account_subtitle_label.place(relx=0.5, rely=0.2, anchor="center")
        
        # Full Name Entry Frame
        self.name_frame = ctk.CTkFrame(
            self.right_frame,
            fg_color=INPUT_BG_COLOR,
            corner_radius=CORNER_RADIUS,
            height=INPUT_HEIGHT
        )
        self.name_frame.place(relx=0.5, rely=0.3, anchor="center")
        self.name_frame.configure(width=300)
        self.name_frame.pack_propagate(False)

        # Name icon
        self.name_icon = ctk.CTkLabel(
            self.name_frame,
            text="👤",
            font=(FONT_FAMILY, NORMAL_TEXT_SIZE),
            text_color=NEUTRAL_COLOR
        )
        self.name_icon.place(relx=0.02, rely=0.5, anchor="w")

        # Name entry
        self.fullname_entry = ctk.CTkEntry(
            self.name_frame,
            placeholder_text="Full Name",
            placeholder_text_color=PLACEHOLDER_COLOR,
            font=(FONT_FAMILY, NORMAL_TEXT_SIZE),
            fg_color=INPUT_BG_COLOR,
            border_width=0,
            corner_radius=0
        )
        self.fullname_entry.place(relx=0.3, rely=0.5, relwidth=0.68, anchor="w")

        # Email Entry Frame
        self.email_frame = ctk.CTkFrame(
            self.right_frame,
            fg_color=INPUT_BG_COLOR,
            corner_radius=CORNER_RADIUS,
            height=INPUT_HEIGHT
        )
        self.email_frame.place(relx=0.5, rely=0.4, anchor="center")
        self.email_frame.configure(width=300)
        self.email_frame.pack_propagate(False)

        # Email icon
        self.email_icon = ctk.CTkLabel(
            self.email_frame,
            text="✉",
            font=(FONT_FAMILY, NORMAL_TEXT_SIZE),
            text_color=NEUTRAL_COLOR
        )
        self.email_icon.place(relx=0.02, rely=0.5, anchor="w")

        # Email entry
        self.email_entry = ctk.CTkEntry(
            self.email_frame,
            placeholder_text="Email",
            placeholder_text_color=PLACEHOLDER_COLOR,
            font=(FONT_FAMILY, NORMAL_TEXT_SIZE),
            fg_color=INPUT_BG_COLOR,
            border_width=0,
            corner_radius=0
        )
        self.email_entry.place(relx=0.3, rely=0.5, relwidth=0.68, anchor="w")
        self.email_entry.bind('<KeyRelease>', self.validate_email_live)

        # Email validation label
        self.email_validation_label = ctk.CTkLabel(
            self.right_frame,
            text="",
            font=(FONT_FAMILY, SMALL_TEXT_SIZE),
            text_color=ERROR_COLOR
        )
        self.email_validation_label.place(relx=0.5, rely=0.45, anchor="center")

        # Password Entry Frame
        self.password_frame = ctk.CTkFrame(
            self.right_frame,
            fg_color=INPUT_BG_COLOR,
            corner_radius=CORNER_RADIUS,
            height=INPUT_HEIGHT
        )
        self.password_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.password_frame.configure(width=300)
        self.password_frame.pack_propagate(False)

        # Password icon
        self.password_icon = ctk.CTkLabel(
            self.password_frame,
            text="🔑",
            font=(FONT_FAMILY, NORMAL_TEXT_SIZE),
            text_color=NEUTRAL_COLOR
        )
        self.password_icon.place(relx=0.02, rely=0.5, anchor="w")

        # Password entry
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

        # Confirm Password Frame
        self.confirm_password_frame = ctk.CTkFrame(
            self.right_frame,
            fg_color=INPUT_BG_COLOR,
            corner_radius=CORNER_RADIUS,
            height=INPUT_HEIGHT
        )
        self.confirm_password_frame.place(relx=0.5, rely=0.6, anchor="center")
        self.confirm_password_frame.configure(width=300)
        self.confirm_password_frame.pack_propagate(False)

        # Confirm Password icon
        self.confirm_password_icon = ctk.CTkLabel(
            self.confirm_password_frame,
            text="🔑",
            font=(FONT_FAMILY, NORMAL_TEXT_SIZE),
            text_color=NEUTRAL_COLOR
        )
        self.confirm_password_icon.place(relx=0.02, rely=0.5, anchor="w")

        # Confirm Password entry
        self.confirm_password_entry = ctk.CTkEntry(
            self.confirm_password_frame,
            placeholder_text="Confirm Password",
            placeholder_text_color=PLACEHOLDER_COLOR,
            font=(FONT_FAMILY, NORMAL_TEXT_SIZE),
            fg_color=INPUT_BG_COLOR,
            border_width=0,
            corner_radius=0,
            show="●"
        )
        self.confirm_password_entry.place(relx=0.3, rely=0.5, relwidth=0.58, anchor="w")

        # Show/Hide confirm password button
        self.toggle_confirm_password_btn = ctk.CTkButton(
            self.confirm_password_frame,
            text="👁",
            width=30,
            height=30,
            fg_color="transparent",
            hover_color=NEUTRAL_COLOR,
            text_color=TEXT_COLOR,
            command=self.toggle_confirm_password_visibility
        )
        self.toggle_confirm_password_btn.place(relx=0.95, rely=0.5, anchor="e")

        # Add password visibility flags
        self.show_password = False
        self.show_confirm_password = False

        # Error message label
        self.error_label = ctk.CTkLabel(
            self.right_frame,
            text="",
            text_color=ERROR_COLOR,
            font=(FONT_FAMILY, SMALL_TEXT_SIZE)
        )
        self.error_label.place(relx=0.5, rely=0.72, anchor="center")
        self.error_label.place_forget()

        # Register Button
        self.signup_button = ctk.CTkButton(
            self.right_frame,
            text="Register",
            command=self.signup,
            width=200,
            height=BUTTON_HEIGHT,
            corner_radius=CORNER_RADIUS,
            fg_color=PRIMARY_COLOR,
            text_color="white",
            hover_color=SECONDARY_COLOR,
            font=(FONT_FAMILY, NORMAL_TEXT_SIZE, "bold")
        )
        self.signup_button.place(relx=0.5, rely=0.78, anchor="center")

        # "Already have an account?" text
        self.login_label = ctk.CTkLabel(
            self.right_frame,
            text="Already have an account?",
            font=(FONT_FAMILY, NORMAL_TEXT_SIZE),
            text_color=TEXT_COLOR
        )
        self.login_label.place(relx=0.5, rely=0.84, anchor="center")

        # Login Link
        self.login_link = ctk.CTkButton(
            self.right_frame,
            text="Log in",
            command=self.show_login,
            width=100,
            height=BUTTON_HEIGHT,
            corner_radius=CORNER_RADIUS,
            fg_color="white",
            text_color=ACCENT_COLOR,
            hover_color="#E5E5E5",
            font=(FONT_FAMILY, NORMAL_TEXT_SIZE, "bold")
        )
        self.login_link.place(relx=0.5, rely=0.9, anchor="center")
    
    def signup(self):
        username = self.fullname_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not username or not email or not password or not confirm_password:
            self.error_label.configure(text="All fields are required")
            self.error_label.place(relx=0.5, rely=0.72, anchor="center")
            return

        # Password length validation
        if not self.validate_password(password):
            self.error_label.configure(text="Password must be at least 6 characters long")
            self.error_label.place(relx=0.5, rely=0.72, anchor="center")
            self.password_frame.configure(border_width=2, border_color=ERROR_COLOR)
            return

        if password != confirm_password:
            self.error_label.configure(text="Passwords do not match")
            self.error_label.place(relx=0.5, rely=0.72, anchor="center")
            self.confirm_password_frame.configure(border_width=2, border_color=ERROR_COLOR)
            return

        # Clear error states
        self.error_label.place_forget()
        self.password_frame.configure(border_width=0)
        self.confirm_password_frame.configure(border_width=0)

        # Create new user in database
        try:
            db = SessionLocal()
            create_user(db, username, email, password, UserRole.CUSTOMER)
            db.close()
            messagebox.showinfo("Success", "Account created successfully! Please login.")
            self.controller.show_page("LoginPage")
        except Exception as e:
            self.error_label.configure(text="Error creating account. Please try again.")
            self.error_label.place(relx=0.5, rely=0.72, anchor="center")
            print(f"Error creating user: {e}")
    
    def validate_password(self, password):
        """Validate password meets requirements"""
        if len(password) < 6:
            return False
        return True

    def show_login(self):
        self.controller.show_page("LoginPage")

    def validate_email_live(self, event):
        email = self.email_entry.get()
        if email:
            if not self.validate_email(email):
                self.email_validation_label.configure(text="Please enter a valid email address")
                self.email_frame.configure(border_width=2, border_color=ERROR_COLOR)
                return False
            else:
                self.email_validation_label.configure(text="")
                self.email_frame.configure(border_width=0)
                return True
        else:
            self.email_validation_label.configure(text="")
            self.email_frame.configure(border_width=0)
            return False

    def validate_email(self, email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    def toggle_password_visibility(self):
        self.show_password = not self.show_password
        self.password_entry.configure(show="" if self.show_password else "●")
        self.toggle_password_btn.configure(text="👁" if not self.show_password else "🔒")

    def toggle_confirm_password_visibility(self):
        self.show_confirm_password = not self.show_confirm_password
        self.confirm_password_entry.configure(show="" if self.show_confirm_password else "●")
        self.toggle_confirm_password_btn.configure(text="👁" if not self.show_confirm_password else "🔒")
