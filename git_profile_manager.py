#!/usr/bin/env python3
"""
Git Profile Manager - A GUI tool to manage and switch between multiple Git configurations
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import json
import os
from pathlib import Path


class GitProfileManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Git Profile Manager")
        self.root.geometry("700x500")
        self.root.resizable(False, False)

        # Configuration file path
        self.config_file = Path.home() / ".git_profile_manager.json"
        self.profiles = self.load_profiles()
        self.current_git_config = self.get_current_git_config()

        self.setup_ui()
        self.refresh_profiles_list()

    def load_profiles(self):
        """Load saved profiles from config file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading profiles: {e}")
                return []
        return []

    def save_profiles(self):
        """Save profiles to config file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.profiles, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save profiles: {e}")

    def get_current_git_config(self):
        """Get current Git configuration"""
        try:
            name = subprocess.check_output(['git', 'config', 'user.name'],
                                         stderr=subprocess.DEVNULL).decode().strip()
            email = subprocess.check_output(['git', 'config', 'user.email'],
                                          stderr=subprocess.DEVNULL).decode().strip()
            return {'name': name, 'email': email}
        except subprocess.CalledProcessError:
            return {'name': 'Not configured', 'email': 'Not configured'}

    def set_git_config(self, name, email, scope='local'):
        """Set Git configuration"""
        try:
            scope_flag = '--global' if scope == 'global' else '--local'
            subprocess.run(['git', 'config', scope_flag, 'user.name', name], check=True)
            subprocess.run(['git', 'config', scope_flag, 'user.email', email], check=True)
            return True
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to set Git config: {e}")
            return False

    def setup_ui(self):
        """Setup the user interface"""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Current Configuration Section
        current_frame = ttk.LabelFrame(main_frame, text="Current Git Configuration", padding="10")
        current_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Label(current_frame, text="Name:", font=('Arial', 9, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=2)
        self.current_name_label = ttk.Label(current_frame, text=self.current_git_config['name'],
                                           foreground='blue')
        self.current_name_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=2)

        ttk.Label(current_frame, text="Email:", font=('Arial', 9, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=2)
        self.current_email_label = ttk.Label(current_frame, text=self.current_git_config['email'],
                                            foreground='blue')
        self.current_email_label.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=2)

        ttk.Button(current_frame, text="Refresh", command=self.refresh_current_config).grid(
            row=0, column=2, rowspan=2, padx=(20, 0))

        # Saved Profiles Section
        profiles_frame = ttk.LabelFrame(main_frame, text="Saved Profiles", padding="10")
        profiles_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))

        # Profiles listbox with scrollbar
        list_frame = ttk.Frame(profiles_frame)
        list_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.profiles_listbox = tk.Listbox(list_frame, height=8, yscrollcommand=scrollbar.set,
                                          font=('Courier', 9))
        self.profiles_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.profiles_listbox.yview)

        # Buttons for profile management
        btn_frame = ttk.Frame(profiles_frame)
        btn_frame.grid(row=1, column=0, pady=(10, 0))

        ttk.Button(btn_frame, text="Apply Selected (Local)",
                  command=lambda: self.apply_profile('local')).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Apply Selected (Global)",
                  command=lambda: self.apply_profile('global')).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Delete Selected",
                  command=self.delete_profile).pack(side=tk.LEFT, padx=2)

        # Add New Profile Section
        add_frame = ttk.LabelFrame(main_frame, text="Add New Profile", padding="10")
        add_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Label(add_frame, text="Profile Name:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.profile_name_entry = ttk.Entry(add_frame, width=30)
        self.profile_name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0), pady=2)

        ttk.Label(add_frame, text="Git Name:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.git_name_entry = ttk.Entry(add_frame, width=30)
        self.git_name_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 0), pady=2)

        ttk.Label(add_frame, text="Git Email:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.git_email_entry = ttk.Entry(add_frame, width=30)
        self.git_email_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(5, 0), pady=2)

        btn_add_frame = ttk.Frame(add_frame)
        btn_add_frame.grid(row=3, column=0, columnspan=2, pady=(10, 0))

        ttk.Button(btn_add_frame, text="Add Profile", command=self.add_profile).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_add_frame, text="Use Current Config",
                  command=self.populate_current_config).pack(side=tk.LEFT, padx=2)

        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        profiles_frame.columnconfigure(0, weight=1)
        profiles_frame.rowconfigure(0, weight=1)
        add_frame.columnconfigure(1, weight=1)

    def refresh_current_config(self):
        """Refresh the current Git configuration display"""
        self.current_git_config = self.get_current_git_config()
        self.current_name_label.config(text=self.current_git_config['name'])
        self.current_email_label.config(text=self.current_git_config['email'])

    def refresh_profiles_list(self):
        """Refresh the profiles listbox"""
        self.profiles_listbox.delete(0, tk.END)
        for profile in self.profiles:
            display_text = f"{profile['profile_name']:20} | {profile['name']:20} | {profile['email']}"
            self.profiles_listbox.insert(tk.END, display_text)

    def populate_current_config(self):
        """Populate the form with current Git configuration"""
        self.git_name_entry.delete(0, tk.END)
        self.git_name_entry.insert(0, self.current_git_config['name'])

        self.git_email_entry.delete(0, tk.END)
        self.git_email_entry.insert(0, self.current_git_config['email'])

        # Auto-generate profile name
        if self.current_git_config['name'] != 'Not configured':
            self.profile_name_entry.delete(0, tk.END)
            self.profile_name_entry.insert(0, self.current_git_config['name'])

    def add_profile(self):
        """Add a new profile"""
        profile_name = self.profile_name_entry.get().strip()
        git_name = self.git_name_entry.get().strip()
        git_email = self.git_email_entry.get().strip()

        if not profile_name or not git_name or not git_email:
            messagebox.showwarning("Warning", "All fields are required!")
            return

        # Check if profile already exists
        for profile in self.profiles:
            if profile['profile_name'] == profile_name:
                if not messagebox.askyesno("Confirm",
                    f"Profile '{profile_name}' already exists. Overwrite?"):
                    return
                self.profiles.remove(profile)
                break

        # Add new profile
        self.profiles.append({
            'profile_name': profile_name,
            'name': git_name,
            'email': git_email
        })

        self.save_profiles()
        self.refresh_profiles_list()

        # Clear the form
        self.profile_name_entry.delete(0, tk.END)
        self.git_name_entry.delete(0, tk.END)
        self.git_email_entry.delete(0, tk.END)

        messagebox.showinfo("Success", f"Profile '{profile_name}' added successfully!")

    def backup_current_profile(self):
        """Backup current Git configuration as a profile if not already saved"""
        current = self.get_current_git_config()

        # Skip if not configured
        if current['name'] == 'Not configured' or current['email'] == 'Not configured':
            return False

        # Check if this profile already exists
        for profile in self.profiles:
            if profile['name'] == current['name'] and profile['email'] == current['email']:
                return False  # Already saved, no need to backup

        # Generate a backup profile name
        base_name = f"{current['name']}_backup"
        backup_name = base_name
        counter = 1

        # Ensure unique profile name
        while any(p['profile_name'] == backup_name for p in self.profiles):
            backup_name = f"{base_name}_{counter}"
            counter += 1

        # Add backup profile
        self.profiles.append({
            'profile_name': backup_name,
            'name': current['name'],
            'email': current['email']
        })

        self.save_profiles()
        return True

    def apply_profile(self, scope):
        """Apply the selected profile with auto-backup of current config"""
        selection = self.profiles_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a profile to apply!")
            return

        profile = self.profiles[selection[0]]

        # Get current config before applying new one
        current = self.get_current_git_config()

        # Check if current config is different from the one being applied
        if (current['name'] != profile['name'] or current['email'] != profile['email']):
            # Backup current profile if it's not already saved
            was_backed_up = self.backup_current_profile()
        else:
            was_backed_up = False

        # Apply the new profile
        if self.set_git_config(profile['name'], profile['email'], scope):
            self.refresh_current_config()
            self.refresh_profiles_list()  # Refresh to show backup if added
            scope_text = "repository" if scope == "local" else "globally"

            backup_msg = "\n\nPrevious configuration was automatically backed up." if was_backed_up else ""
            messagebox.showinfo("Success",
                f"Profile '{profile['profile_name']}' applied {scope_text}!{backup_msg}")

    def delete_profile(self):
        """Delete the selected profile"""
        selection = self.profiles_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a profile to delete!")
            return

        profile = self.profiles[selection[0]]

        if messagebox.askyesno("Confirm",
            f"Are you sure you want to delete profile '{profile['profile_name']}'?"):
            self.profiles.pop(selection[0])
            self.save_profiles()
            self.refresh_profiles_list()
            messagebox.showinfo("Success", "Profile deleted successfully!")


def main():
    root = tk.Tk()
    app = GitProfileManager(root)
    root.mainloop()


if __name__ == "__main__":
    main()
