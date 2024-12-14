import customtkinter as ctk
from .base_page import BasePage
from .constants import *
import re
import os
from PIL import Image
from database.config import SessionLocal
from database.utils import get_user_by_email, update_user_password
from tkinter import messagebox
import random
import string

class ForgotPasswordPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.configure(fg_color=PRIMARY_COLOR)  # Set background to emerald green
        
        # Initialize password visibility states
        self.show_password = False
        self.show_confirm_password = False
        
        # Logo container at top
        self.logo_container = ctk.CTkFrame(
            self,
            fg_color="transparent",
            height=100
        )
        self.logo_container.pack(fill="x", pady=(20, 0))
        
        # Load and display logo
        try:
            logo_path = os.path.join("assets", "images", "myLogo.png")
            self.logo_image = ctk.CTkImage(
                light_image=Image.open(logo_path),
                dark_image=Image.open(logo_path),
                size=(45, 45)
            )
            self.logo_label = ctk.CTkLabel(
                self.logo_container,
                image=self.logo_image,
                text=""
            )
            self.logo_label.place(relx=0.05, rely=0.5, anchor="w")
            
            # Add app name next to logo
            self.app_name = ctk.CTkLabel(
                self.logo_container,
                text="SmartBites",
                font=(LOGO_FONT, 25, "bold"),
                text_color=WHITE_COLOR
            )
            self.app_name.place(relx=0.09, rely=0.5, anchor="w")
            
        except Exception as e:
            print(f"Error loading logo: {e}")
        
        # White center container
        self.center_container = ctk.CTkFrame(
            self,
            fg_color=WHITE_COLOR,
            corner_radius=15,
            width=500,
            height=450
        )
        self.center_container.pack(expand=True, pady=(20, 40))
        self.center_container.pack_propagate(False)
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.center_container,
            text="Forgot Password",
            font=(FONT_FAMILY, HEADING_SIZE, "bold"),
            text_color=TEXT_COLOR
        )
        self.title_label.pack(pady=(60, 10))
        
        # Description
        self.description_label = ctk.CTkLabel(
            self.center_container,
            text="Enter the email associated to your account and\nwe will send you password reset instructions.",
            font=(FONT_FAMILY, NORMAL_TEXT_SIZE),
            text_color=NEUTRAL_COLOR,
            justify="center",
            wraplength=400
        )
        self.description_label.pack(pady=(0, 40))
        
        # Email Entry Frame
        self.email_frame = ctk.CTkFrame(
            self.center_container,
            fg_color=INPUT_BG_COLOR,
            corner_radius=CORNER_RADIUS,
            height=INPUT_HEIGHT
        )
        self.email_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.email_frame.configure(width=250)
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
        
        # Error Label
        self.error_label = ctk.CTkLabel(
            self.center_container,
            text="",
            text_color=ERROR_COLOR,
            font=(FONT_FAMILY, SMALL_TEXT_SIZE)
        )
        self.error_label.place(relx=0.5, rely=0.57, anchor="center")
        
        # Send Code Button
        self.send_code_btn = ctk.CTkButton(
            self.center_container,
            text="Continue",
            command=self.send_reset_code,
            width=250,
            height=BUTTON_HEIGHT,
            corner_radius=CORNER_RADIUS,
            fg_color=PRIMARY_COLOR,
            text_color=WHITE_COLOR,
            hover_color="#0056b3",
            font=(FONT_FAMILY, NORMAL_TEXT_SIZE, "bold")
        )
        self.send_code_btn.place(relx=0.5, rely=0.65, anchor="center")
        
        # Back to Login Button
        self.back_btn = ctk.CTkButton(
            self.center_container,
            text="Back to Login",
            command=self.back_to_login,
            width=200,
            height=BUTTON_HEIGHT,
            corner_radius=CORNER_RADIUS,
            fg_color="transparent",
            text_color=ACCENT_COLOR,
            hover_color="#F0F0F0",
            font=(FONT_FAMILY, NORMAL_TEXT_SIZE)
        )
        self.back_btn.place(relx=0.5, rely=0.8, anchor="center")
        
        # Create verification code page (initially hidden)
        self.verification_container = ctk.CTkFrame(
            self,
            fg_color=WHITE_COLOR,
            corner_radius=15,
            width=500,
            height=450
        )
        self.verification_container.pack_propagate(False)  # Added to prevent size changes
        
        # Verification page title
        self.verification_title = ctk.CTkLabel(
            self.verification_container,
            text="Enter Security Code",
            font=(FONT_FAMILY, HEADING_SIZE, "bold"),
            text_color=TEXT_COLOR
        )
        self.verification_title.place(relx=0.5, rely=0.15, anchor="center")  # Changed to place
        
        # Verification description
        self.verification_desc = ctk.CTkLabel(
            self.verification_container,
            text="We have sent a security code to your email.\nPlease enter it below to continue.",
            font=(FONT_FAMILY, NORMAL_TEXT_SIZE),
            text_color=NEUTRAL_COLOR,
            justify="center",
            wraplength=400
        )
        self.verification_desc.place(relx=0.5, rely=0.25, anchor="center")  # Changed to place
        
        # Code Entry Frame
        self.code_frame = ctk.CTkFrame(
            self.verification_container,
            fg_color=INPUT_BG_COLOR,
            corner_radius=CORNER_RADIUS,
            height=INPUT_HEIGHT
        )
        self.code_frame.place(relx=0.5, rely=0.4, anchor="center")
        self.code_frame.configure(width=250)
        self.code_frame.pack_propagate(False)
        
        # Code icon
        self.code_icon = ctk.CTkLabel(
            self.code_frame,
            text="🔑",
            font=(FONT_FAMILY, NORMAL_TEXT_SIZE),
            text_color=NEUTRAL_COLOR
        )
        self.code_icon.place(relx=0.02, rely=0.5, anchor="w")
        
        # Code entry
        self.code_entry = ctk.CTkEntry(
            self.code_frame,
            placeholder_text="Enter Security Code",
            font=(FONT_FAMILY, NORMAL_TEXT_SIZE),
            fg_color="transparent",
            placeholder_text_color=PLACEHOLDER_COLOR,
            border_width=0
        )
        self.code_entry.place(relx=0.3, rely=0.5, relwidth=0.68, anchor="w")
        
        # New Password Frame
        self.new_password_frame = ctk.CTkFrame(
            self.verification_container,
            fg_color=INPUT_BG_COLOR,
            corner_radius=CORNER_RADIUS,
            height=INPUT_HEIGHT
        )
        self.new_password_frame.place(relx=0.5, rely=0.53, anchor="center")
        self.new_password_frame.configure(width=250)
        self.new_password_frame.pack_propagate(False)
        
        # New Password icon
        self.new_password_icon = ctk.CTkLabel(
            self.new_password_frame,
            text="🔒",
            font=(FONT_FAMILY, NORMAL_TEXT_SIZE),
            text_color=NEUTRAL_COLOR
        )
        self.new_password_icon.place(relx=0.02, rely=0.5, anchor="w")
        
        # New Password entry
        self.new_password_entry = ctk.CTkEntry(
            self.new_password_frame,
            placeholder_text="Enter New Password",
            font=(FONT_FAMILY, NORMAL_TEXT_SIZE),
            fg_color="transparent",
            placeholder_text_color=PLACEHOLDER_COLOR,
            border_width=0,
            show="•"
        )
        self.new_password_entry.place(relx=0.3, rely=0.5, relwidth=0.68, anchor="w")
        
        # Show/Hide new password button
        self.toggle_new_password_btn = ctk.CTkButton(
            self.new_password_frame,
            text="👁",
            width=30,
            height=30,
            fg_color="transparent",
            hover_color=NEUTRAL_COLOR,
            text_color=TEXT_COLOR,
            command=self.toggle_new_password_visibility
        )
        self.toggle_new_password_btn.place(relx=0.95, rely=0.5, anchor="e")

        # Confirm Password Frame
        self.confirm_password_frame = ctk.CTkFrame(
            self.verification_container,
            fg_color=INPUT_BG_COLOR,
            corner_radius=CORNER_RADIUS,
            height=INPUT_HEIGHT
        )
        self.confirm_password_frame.place(relx=0.5, rely=0.66, anchor="center")
        self.confirm_password_frame.configure(width=250)
        self.confirm_password_frame.pack_propagate(False)
        
        # Confirm Password icon
        self.confirm_password_icon = ctk.CTkLabel(
            self.confirm_password_frame,
            text="🔒",
            font=(FONT_FAMILY, NORMAL_TEXT_SIZE),
            text_color=NEUTRAL_COLOR
        )
        self.confirm_password_icon.place(relx=0.02, rely=0.5, anchor="w")
        
        # Confirm Password entry
        self.confirm_password_entry = ctk.CTkEntry(
            self.confirm_password_frame,
            placeholder_text="Confirm Password",
            font=(FONT_FAMILY, NORMAL_TEXT_SIZE),
            fg_color="transparent",
            placeholder_text_color=PLACEHOLDER_COLOR,
            border_width=0,
            show="•"
        )
        self.confirm_password_entry.place(relx=0.3, rely=0.5, relwidth=0.68, anchor="w")
        
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
        
        # Password validation error label
        self.password_error_label = ctk.CTkLabel(
            self.verification_container,
            text="",
            text_color=ERROR_COLOR,
            font=(FONT_FAMILY, SMALL_TEXT_SIZE)
        )
        self.password_error_label.place(relx=0.5, rely=0.74, anchor="center")
        self.password_error_label.place_forget()  # Initially hidden
        
        # Reset Password Button
        self.reset_password_btn = ctk.CTkButton(
            self.verification_container,
            text="Reset Password",
            width=250,
            height=BUTTON_HEIGHT,
            corner_radius=CORNER_RADIUS,
            fg_color=PRIMARY_COLOR,
            text_color=WHITE_COLOR,
            hover_color="#006B3E",  # Darker shade of PRIMARY_COLOR
            font=(FONT_FAMILY, NORMAL_TEXT_SIZE, "bold"),
            command=self.reset_password  # Make sure this is correct
        )
        self.reset_password_btn.place(relx=0.5, rely=0.8, anchor="center")
        
        # Success message label (initially hidden)
        self.success_label = ctk.CTkLabel(
            self.verification_container,
            text="Password successfully reset!",
            font=(FONT_FAMILY, 20, "bold"),
            text_color=ACCENT_COLOR
        )
        self.success_label.place_forget()

    def reset_page_state(self):
        """Reset the page to its initial state"""
        # Hide verification container if visible
        self.verification_container.pack_forget()
        
        # Show initial container
        self.center_container.pack(expand=True, pady=(20, 40))
        
        # Clear all fields
        self.email_entry.delete(0, 'end')
        if hasattr(self, 'code_entry'):
            self.code_entry.delete(0, 'end')
        if hasattr(self, 'new_password_entry'):
            self.new_password_entry.delete(0, 'end')
        if hasattr(self, 'confirm_password_entry'):
            self.confirm_password_entry.delete(0, 'end')
        
        # Reset any error states
        self.email_frame.configure(border_width=0)
        if hasattr(self, 'error_label'):
            self.error_label.configure(text="")
        
        # Reset button states
        self.reset_password_btn.configure(state="normal")
        
        # Hide success message if visible
        if hasattr(self, 'success_label'):
            self.success_label.place_forget()

    def tkraise(self):
        """Override tkraise to reset page state when shown"""
        self.reset_page_state()
        super().tkraise()

    def validate_email_live(self, event):
        email = self.email_entry.get()
        if email:
            if not self.validate_email(email):
                self.error_label.configure(text="Please enter a valid email address")
                self.email_frame.configure(border_width=2, border_color=ERROR_COLOR)
                return False
            else:
                self.error_label.configure(text="")
                self.email_frame.configure(border_width=0)
                return True
        else:
            self.error_label.configure(text="")
            self.email_frame.configure(border_width=0)
            return False
    
    def validate_email(self, email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None
    
    def validate_password(self, password):
        """Validate password meets requirements"""
        if len(password) < 6:
            return False
        return True

    def send_reset_code(self):
        email = self.email_entry.get()
        
        if not email:
            self.error_label.configure(text="Please enter your email address")
            self.error_label.place(relx=0.5, rely=0.57, anchor="center")
            return
        
        if not self.validate_email(email):
            self.error_label.configure(text="Please enter a valid email address")
            self.error_label.place(relx=0.5, rely=0.57, anchor="center")
            return
        
        # Check if email exists in database
        db = SessionLocal()
        user = get_user_by_email(db, email)
        db.close()
        
        if not user:
            self.error_label.configure(text="No account found with this email address")
            self.error_label.place(relx=0.5, rely=0.57, anchor="center")
            return
        
        # Generate a random 6-digit code
        self.reset_code = ''.join(random.choices(string.digits, k=6))
        self.user_id = user.id
        
        # In a real application, you would send this code via email
        # For demo purposes, we'll show it in a message box
        messagebox.showinfo("Reset Code", f"Your reset code is: {self.reset_code}\n\nIn a real application, this would be sent to your email.")
        
        # Hide the email entry container and show verification container
        self.center_container.pack_forget()
        self.verification_container.pack(expand=True, pady=(20, 40))
        
    def reset_password(self):
        entered_code = self.code_entry.get()
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        if not entered_code or not new_password or not confirm_password:
            self.password_error_label.configure(text="All fields are required")
            self.password_error_label.place(relx=0.5, rely=0.74, anchor="center")
            return
        
        if not hasattr(self, 'reset_code') or entered_code != self.reset_code:
            self.password_error_label.configure(text="Invalid reset code")
            self.password_error_label.place(relx=0.5, rely=0.74, anchor="center")
            return
        
        if not self.validate_password(new_password):
            self.password_error_label.configure(text="Password must be at least 6 characters long")
            self.password_error_label.place(relx=0.5, rely=0.74, anchor="center")
            return
        
        if new_password != confirm_password:
            self.password_error_label.configure(text="Passwords do not match")
            self.password_error_label.place(relx=0.5, rely=0.74, anchor="center")
            return
        
        try:
            # Update password in database
            db = SessionLocal()
            update_user_password(db, self.user_id, new_password)
            db.close()
            
            # Show success message
            messagebox.showinfo("Success", "Password has been reset successfully!")
            
            # Return to login page
            self.controller.show_page("LoginPage")
            
        except Exception as e:
            self.password_error_label.configure(text="Error resetting password. Please try again.")
            self.password_error_label.place(relx=0.5, rely=0.74, anchor="center")
            print(f"Error resetting password: {e}")
    
    def go_to_login_direct(self):
        print("Going directly to login")
        # Hide success message
        self.success_label.place_forget()
        
        # Re-enable the reset button
        self.reset_password_btn.configure(state="normal")
        
        # Clear all fields
        self.code_entry.delete(0, 'end')
        self.new_password_entry.delete(0, 'end')
        self.confirm_password_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
        
        # Reset containers to initial state
        self.verification_container.pack_forget()
        self.center_container.pack_forget()
        
        # Go directly to login page using the correct method
        self.controller.show_page("LoginPage")
    
    def back_to_login_clicked(self):
        print("Going back to login")
        # Hide success message
        self.success_label.place_forget()
        
        # Re-enable the reset button
        self.reset_password_btn.configure(state="normal")
        
        # Hide verification container and show email container
        self.verification_container.pack_forget()
        self.center_container.pack(expand=True, pady=(20, 40))
        
        # Clear all fields on the verification page
        self.code_entry.delete(0, 'end')
        self.new_password_entry.delete(0, 'end')
        self.confirm_password_entry.delete(0, 'end')
        
        # Clear all fields on the email page
        self.email_entry.delete(0, 'end')
        
        # Go back to login page
        self.controller.show_page("LoginPage")
    
    def toggle_new_password_visibility(self):
        self.show_password = not self.show_password
        self.new_password_entry.configure(show="" if self.show_password else "•")
        self.toggle_new_password_btn.configure(text="👁" if not self.show_password else "🔒")
    
    def toggle_confirm_password_visibility(self):
        self.show_confirm_password = not self.show_confirm_password
        self.confirm_password_entry.configure(show="" if self.show_confirm_password else "•")
        self.toggle_confirm_password_btn.configure(text="👁" if not self.show_confirm_password else "🔒")
    
    def back_to_login(self):
        self.controller.show_page("LoginPage")
