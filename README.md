# Git Profile Manager

A simple Python GUI tool to manage and switch between multiple Git user configurations easily.

## Features

- **View Current Git Configuration**: See your current Git user.name and user.email at a glance
- **Save Multiple Profiles**: Store unlimited Git profiles locally
- **Quick Profile Switching**: Apply any saved profile with one click
- **Auto-Backup**: When switching profiles, your current configuration is automatically backed up if not already saved
- **Local or Global Scope**: Choose to apply profile to current repository only or globally
- **Profile Management**: Add, update, and delete profiles easily
- **Auto-populate**: Quickly save your current Git config as a new profile

## Requirements

- Python 3.6 or higher
- tkinter (usually comes pre-installed with Python)
- Git installed and accessible from command line

## Installation

1. Clone or download this repository
2. No additional dependencies needed (uses only Python standard library)

## Usage

### Running the Tool

```bash
cd /path/to/git-profile-manager
python git_profile_manager.py
```

Or on Windows, you can simply double-click `git_profile_manager.py`

### How to Use

1. **View Current Configuration**
   - The top section shows your current Git user configuration
   - Click "Refresh" to update if you've made changes outside the tool

2. **Add Your First Profile**
   - Click "Use Current Config" to auto-fill your current Git settings
   - Or manually enter:
     - Profile Name (e.g., "Work", "Personal")
     - Git Name (e.g., "john.doe")
     - Git Email (e.g., "john.doe@company.com")
   - Click "Add Profile"

3. **Switch Profiles**
   - Select a profile from the list
   - Click "Apply Selected (Local)" to apply to current repository only
   - Click "Apply Selected (Global)" to apply system-wide
   - **Note**: Your current Git config is automatically backed up before switching (if not already saved)

4. **Delete Profiles**
   - Select a profile from the list
   - Click "Delete Selected"

## Example: Setting Up Work and Personal Profiles

### Add Work Profile
```
Profile Name: Work
Git Name: john.doe
Git Email: john.doe@company.com
```

### Add Personal Profile
```
Profile Name: Personal
Git Name: johndoe
Git Email: johndoe@example.com
```

Now you can switch between them anytime with just one click!

## Data Storage

Profiles are saved in: `~/.git_profile_manager.json` (or `C:\Users\YourUsername\.git_profile_manager.json` on Windows)

This file stores all your saved profiles and persists between sessions.

## Tips

- **Auto-Backup Feature**:
  - When you switch profiles, your current Git configuration is automatically backed up
  - The backup is saved with a name like "username_backup" or "username_backup_1"
  - If the configuration is already saved in your profiles, no duplicate backup is created
  - This ensures you never lose your previous Git identity

- **Local vs Global**:
  - **Local**: Applies Git config to the current working directory's Git repository
    - You must run the tool from within a Git repository folder (or navigate there first in your terminal)
    - Example: `cd /path/to/your/git/project` then run the tool
    - The tool finds the `.git` folder in your current directory and updates that specific repository's config
    - If you run the tool from a non-Git folder and click "Apply Local", it will fail
  - **Global**: Applies Git config system-wide (updates `~/.gitconfig`)
    - Works from anywhere, regardless of current directory
    - Becomes your default Git identity for all repositories that don't have local config

- **Eclipse EGit Integration**: After applying a profile locally to a repository, Eclipse EGit will automatically use those credentials for that specific repository

- **Multiple Work Repositories**: Set your work profile as "Local" in each work repository, so they always use work credentials regardless of your global config

## Troubleshooting

**Tool doesn't run:**
- Make sure Python 3.6+ is installed: `python --version`
- Check if Git is accessible: `git --version`

**Changes not reflecting in Eclipse:**
- Try refreshing the Eclipse project (F5)
- Restart Eclipse if needed

**Profile not applied (Local scope):**
- Make sure you navigated to a Git repository folder before running the tool
- Example: Open terminal, run `cd C:\path\to\your\git\project`, then run the tool
- Check if you have write permissions to the `.git/config` file
- The tool applies config to wherever you ran it from, not where the tool is located

## License

Free to use and modify as needed.
