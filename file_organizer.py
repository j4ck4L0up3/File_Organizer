"""Organize Files into the Appropriate Locations"""

import os
import shutil
from pathlib import Path
from typing import Optional

from .logger import get_debug_logger
from .special_exceptions import EmptyDirectory

with open("./debug.log", "wt", encoding="utf-8") as debug_log_file:
    debug_logger = get_debug_logger(debug_log_file)


def get_non_hidden_dirs(directory: Optional[Path] = None) -> list:
    """get list of non-hidden directories"""

    if directory is None:
        return []

    approved_items = [
        item for item in os.listdir(directory) if not item.startswith(".")
    ]
    approved_dirs = [
        item for item in approved_items if os.path.isdir(Path(directory, item))
    ]
    debug_logger.debug("Approved Directories: %s", approved_dirs)
    return approved_dirs


def get_non_hidden_files(directory: Optional[Path] = None) -> list:
    """get list of non-hidden files"""

    if directory is None:
        return []

    approved_items = [
        item for item in os.listdir(directory) if not item.startswith(".")
    ]
    approved_files = [
        file for file in approved_items if os.path.isfile(Path(directory, file))
    ]
    debug_logger.debug("Approved Files: %s", approved_files)
    return approved_files


def create_required_dirs(dirs: list, home: Path):
    """create all required directories if they do not already exist"""

    try:
        for directory in dirs:
            if Path.exists(home / directory):
                debug_logger.info("Directory %s already exists", directory)
                continue

            os.makedirs(home / directory)
            debug_logger.debug("%s has been added!", directory)

    except FileExistsError as fee:
        debug_logger.error(
            "FileExistsError occurred with checking in create_required_dirs: %s", fee
        )

    except OSError as ose:
        debug_logger.error("OSError in create_required_dirs: %s", ose)

    except Exception as e:
        debug_logger.error("Error in create_required_dirs: %s", e)


# TODO: add cleanup Desktop, asks if you want to include desktop in cleanup
# returns flag for funnels to check
# if not clean_desktop and directory == 'Desktop', then continue


def research_dir_funnel(home: Path):
    """move directories to Research directory
    if they start with 'Learn', 'Study', or 'Test'
    """

    try:
        approved_home_dirs = get_non_hidden_dirs(home)
        if approved_home_dirs == []:
            raise EmptyDirectory(debug_logger, home, research_dir_funnel.__name__)

        for directory in approved_home_dirs:
            if directory == "Research":
                continue

            directory_path = home / directory
            approved_sub_dirs = get_non_hidden_dirs(directory_path)
            if approved_sub_dirs == []:
                debug_logger.info("No subdirectories in %s", directory)
                continue

            for item in approved_sub_dirs:
                has_git_file = Path.exists(home / directory / item / ".git")
                is_research = (
                    item.startswith("Learn")
                    or item.startswith("Study")
                    or item.startswith("Test")
                )
                is_research = is_research and has_git_file
                if not is_research:
                    continue

                source_path = home / directory / item
                destination_path = home / "Research"
                debug_logger.info("Source path in research_dir_funnel: %s", source_path)
                debug_logger.info(
                    "Destination path in research_dir_funnel: %s", destination_path
                )
                # FIXME: test before moving anything
                # moved_dir_path = shutil.move(source_path, destination_path)
                # debug_logger.info(f'Directory was move to {moved_dir_path}')

    except EmptyDirectory as ed:
        ed.log_empty_dir_memo()

    except FileExistsError as fee:
        debug_logger.error("FileExistsError in research_dir_funnel: %s", fee)

    except OSError as ose:
        debug_logger.error("OSError in research_dir_funnel: %s", ose)

    except Exception as e:
        debug_logger.error("Error in research_dir_funnel: %s", e)

    debug_logger.info("Function completed: research_dir_funnel")


def college_dir_funnel(home: Path):
    """move directories to College directory
    if they start with 'CS'
    """

    try:
        approved_home_dirs = get_non_hidden_dirs(home)
        if approved_home_dirs == []:
            raise EmptyDirectory(debug_logger, home, college_dir_funnel.__name__)

        for directory in approved_home_dirs:
            if directory == "College":
                continue

            directory_path = home / directory
            approved_sub_dirs = get_non_hidden_dirs(directory_path)
            if approved_sub_dirs == []:
                debug_logger.info("No subdirectories in %s", directory)
                continue

            for item in approved_sub_dirs:
                is_college = item.startswith("CS")
                if not is_college:
                    continue

                source_path = home / directory / item
                destination_path = home / "College"
                debug_logger.info("Source path in college_dir_funnel: %s", source_path)
                debug_logger.info(
                    "Destination path in college_dir_funnel: %s", destination_path
                )
                # FIXME: test before moving anything
                # moved_dir_path = shutil.move(source_path, destination_path)
                # debug_logger.info(f'Directory was move to {moved_dir_path}')

    except EmptyDirectory as ed:
        ed.log_empty_dir_memo()

    except FileExistsError as fee:
        debug_logger.error("FileExistsError in college_dir_funnel: %s", fee)

    except OSError as ose:
        debug_logger.error("OSError in college_dir_funnel: %s", ose)

    except Exception as e:
        debug_logger.error("Error in college_dir_funnel: %s", e)

    debug_logger.info("Function completed: college_dir_funnel")


def hackathon_dir_funnel(home: Path):
    """move directories to Hackathon directory
    if they start with 'Hackathon'
    """

    try:
        approved_home_dirs = get_non_hidden_dirs(home)
        if approved_home_dirs == []:
            raise EmptyDirectory(debug_logger, home, hackathon_dir_funnel.__name__)

        for directory in approved_home_dirs:
            if directory == "Hackathon":
                continue

            directory_path = home / directory
            approved_sub_dirs = get_non_hidden_dirs(directory_path)
            if approved_sub_dirs == []:
                debug_logger.info("No subdirectories in %s", directory)
                continue

            for item in approved_sub_dirs:
                has_git_file = Path.exists(home / directory / item / ".git")
                is_hackathon = item.startswith("Hackathon") and has_git_file
                if not is_hackathon:
                    continue

                source_path = home / directory / item
                destination_path = home / "Hackathon"
                debug_logger.info(
                    "Source path in hackathon_dir_funnel: %s", source_path
                )
                debug_logger.info(
                    "Destination path in hackathon_dir_funnel: %s", destination_path
                )
                # FIXME: test before moving anything
                # moved_dir_path = shutil.move(source_path, destination_path)
                # debug_logger.info(f'Directory was move to {moved_dir_path}')

    except EmptyDirectory as ed:
        ed.log_empty_dir_memo()

    except FileExistsError as fee:
        debug_logger.error("FileExistsError in hackathon_dir_funnel: %s", fee)

    except OSError as ose:
        debug_logger.error("OSError in hackthon_dir_funnel: %s", ose)

    except Exception as e:
        debug_logger.error("Error in hackathon_dir_funnel: %s", e)

    debug_logger.info("Function completed: hackathon_dir_funnel")


def projects_dir_funnel(home: Path):
    """move directories to Projects
    if they contain a .git file
    and not already in Research
    """

    try:
        approved_home_dirs = get_non_hidden_dirs(home)
        if approved_home_dirs == []:
            raise EmptyDirectory(debug_logger, home, projects_dir_funnel.__name__)

        for directory in approved_home_dirs:
            if directory == "Projects":
                continue
            if directory == "Research":
                continue

            directory_path = home / directory
            approved_sub_dirs = get_non_hidden_dirs(directory_path)
            if approved_sub_dirs == []:
                debug_logger.info("No subdirectories in %s", directory)
                continue

            for item in approved_sub_dirs:
                has_git_file = Path.exists(home / directory / item / ".git")
                if not has_git_file:
                    continue

                source_path = home / directory / item
                destination_path = home / "Projects"
                debug_logger.info("Source path in projects_dir_funnel: %s", source_path)
                debug_logger.info(
                    "Destination path in projects_dir_funnel: %s", destination_path
                )
                # FIXME: test before moving anything
                # moved_dir_path = shutil.move(source_path, destination_path)
                # debug_logger.info(f'Directory was move to {moved_dir_path}')

    except EmptyDirectory as ed:
        ed.log_empty_dir_memo()

    except FileExistsError as fee:
        debug_logger.error("FileExistsError in projects_dir_funnel: %s", fee)

    except OSError as ose:
        debug_logger.error("OSError in projects_dir_funnel: %s", ose)

    except Exception as e:
        debug_logger.error("Error in projects_dir_funnel: %s", e)

    debug_logger.info("Function completed: projects_dir_funnel")


def backups_dir_funnel(home: Path):
    """move files to Backups
    if they contain 'backup' in the filename
    """

    try:
        approved_home_dirs = get_non_hidden_dirs(home)
        if approved_home_dirs == []:
            raise EmptyDirectory(debug_logger, home, backups_dir_funnel.__name__)

        for directory in approved_home_dirs:
            directory_path = home / directory
            approved_files = get_non_hidden_files(directory_path)
            backup_files = [file for file in approved_files if "backup" in file]
            debug_logger.debug("Backup files to be moved: %s", backup_files)

            if backup_files == []:
                debug_logger.info("No backup files in %s", directory)
                continue

            for file in backup_files:
                source_path = home / directory / file
                destination_path = home / "Backups"
                debug_logger.info("Source path in backups_dir_funnel: %s", source_path)
                debug_logger.info(
                    "Destination path in backups_dir_funnel: %s", destination_path
                )
                # FIXME: test before moving
                # move files to Backups
                # moved_dir_path = shutil.move(source_path, destination_path)

    except EmptyDirectory as ed:
        ed.log_empty_dir_memo()

    except FileExistsError as fee:
        debug_logger.error("FileExistsError in backups_dir_funnel: %s", fee)

    except OSError as ose:
        debug_logger.error("OSError in backups_dir_funnel: %s", ose)

    except Exception as e:
        debug_logger.error("Error in backups_dir_funnel: %s", e)

    debug_logger.info("Function completed: backups_dir_funnel")


def cleanup_downloads_dir(home: Path):
    """clean up Downloads directory by moving files
    based on their file extension to other directories
    """

    try:
        # funnel remaining files into Documents, Pictures, Music, Videos
        downloads_path = home / "Downloads"
        downloads_files = get_non_hidden_files(downloads_path)
        funnel_dir_ext_map = {
            "Documents": [".pdf", ".doc", ".docx", ".txt"],
            "Pictures": [".png", ".jpg", ".jpeg"],
            "Music": [".wav", ".mp3", ".mp4", ".ogg"],
            "Videos": [".mov", ".avi", ".wmv", ".flv", ".avchd"],
        }

        for file in downloads_files:
            file_ext = Path(file).suffix
            for directory, ext_list in funnel_dir_ext_map.items():
                if file_ext in ext_list:
                    # FIXME: move to dir after testing
                    source_path = home / "Downloads" / file
                    destination_path = home / directory
                    debug_logger.info(
                        "Source path in cleanup_downloads_dir: %s", source_path
                    )
                    debug_logger.info(
                        "Destination path in cleanup_downloads_dir: %s",
                        destination_path,
                    )

                    break

    except FileExistsError as fee:
        debug_logger.error("FileExistsError in cleanup_downloads_dir: %s", fee)

    except OSError as ose:
        debug_logger.error("OSError in cleanup_downloads_dir: %s", ose)

    except Exception as e:
        debug_logger.error("Error in cleanup_downloads_dir: %s", e)

    debug_logger.info("Function completed: cleanup_downloads_dir")


# TODO: check if user wants compressed files in downloads deleted
def del_zip_files():
    """TODO: add docstring"""
    pass


if __name__ == "__main__":
    my_dirs = [
        "Projects",
        "Hackathons",
        "Documents",
        "Desktop",
        "Fonts",
        "Templates",
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

    # initial run test
    test_path = Path.home() / "Test_FO"

    create_required_dirs(my_dirs, test_path)

    research_dir_funnel(test_path)
    college_dir_funnel(test_path)
    hackathon_dir_funnel(test_path)
    projects_dir_funnel(test_path)
    backups_dir_funnel(test_path)
    cleanup_downloads_dir(test_path)

    # home_path = Path.home()
    # debug_logger.info('Home path created: %s', home_path)

    #  create required dirs
    # create_required_dirs(my_dirs, home_path)

    # directory funnels
    # research_dir_funnel(home_path)
    # college_dir_funnel(home_path)
    # hackathon_dir_funnel(home_path)
    # projects_dir_funnel(home_path)
    # backups_dir_funnel(home_path)
    # cleanup_downloads_dir(home_path)

    # close debug log file
    debug_log_file.close()
