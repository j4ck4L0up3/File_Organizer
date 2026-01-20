"""For running all funnels in an integrated fashion."""

from pathlib import Path

from app import file_organizer as fo


def main(desktop_flag: bool, trash_flag: bool):
    my_dirs = [
        "Projects",
        "Hackathons",
        "Documents",
        "Desktop",
        "Fonts",
        "Templates",
        "3D Models",
        "Hacking",
        "Powerhouse_Vault",
        "Obsidian_Plugin_Sandbox",
        "Pictures",
        "Music",
        "Downloads",
        "Arduino",
        "anaconda3",
        "Videos",
        "Backups",
        "Research",
        "College",
    ]
    home_path = Path().home()

    # first create directories if they don't already exist
    fo.create_required_dirs(my_dirs, home_path)

    # run funnels with desktop flag applied,
    # True or False determined in cli.py
    fo.research_dir_funnel(home_path, desktop_flag)
    fo.college_dir_funnel(home_path, desktop_flag)
    fo.hackathon_dir_funnel(home_path, desktop_flag)
    fo.projects_dir_funnel(home_path, desktop_flag)
    fo.backups_dir_funnel(home_path, desktop_flag)
    fo.cleanup_downloads_dir(home_path)
    fo.del_zip_files(home_path, trash_flag)
