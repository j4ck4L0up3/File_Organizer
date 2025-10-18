"""Organize Files into the Appropriate Locations"""

import logging
import os
import shutil
import subprocess
import sys
from pathlib import Path

from app.special_exceptions import EmptyDirectory

# uncomment logger for debugging
# logger = logging.getLogger("Debug Logger")

logger = logging.getLogger("Prod Logger")


def get_non_hidden_dirs(directory: Path | None = None) -> list[str]:
    """get list of non-hidden directories"""

    if directory is None:
        return []

    approved_items = [
        item for item in os.listdir(directory) if not item.startswith(".")
    ]
    approved_dirs = [item for item in approved_items if Path(directory, item).is_dir()]
    logger.debug("Approved Directories in %s: %s", directory, approved_dirs)
    actual_dirs = subprocess.run(
        ["ls", directory], capture_output=True, text=True, check=True
    )
    logger.debug("Actual Directories in %s: %s", directory, actual_dirs.stdout)
    return approved_dirs


def get_non_hidden_files(directory: Path | None = None) -> list[str]:
    """get list of non-hidden files"""

    if directory is None:
        return []

    approved_items = [
        item for item in os.listdir(directory) if not item.startswith(".")
    ]
    approved_files = [
        file for file in approved_items if Path(directory, file).is_file()
    ]
    logger.debug("Approved Files: %s", approved_files)
    return approved_files


def create_required_dirs(dirs: list, home: Path):
    """
    create all required directories if they do not already exist
    """

    try:
        for directory in dirs:
            if Path.exists(home / directory):
                logger.info("Directory %s already exists", directory)
                continue

            os.makedirs(home / directory)
            logger.debug("%s has been added!", directory)

    except FileExistsError as fee:
        logger.error(
            "FileExistsError occurred with checking in create_required_dirs: %s", fee
        )
        raise

    except OSError as ose:
        logger.error("OSError in create_required_dirs: %s", ose)
        raise


def research_dir_funnel(home: Path, desktop_flag: bool = False):
    """
    move directories to Research directory
    if they start with 'Learn', 'Study', or 'Test'
    """

    try:
        approved_home_dirs = get_non_hidden_dirs(home)
        if approved_home_dirs == [] or len(approved_home_dirs) == 0:
            raise EmptyDirectory(home, research_dir_funnel.__name__)

        for directory in approved_home_dirs:
            if directory == "Research":
                continue

            if not desktop_flag and directory == "Desktop":
                continue

            directory_path = home / directory
            approved_sub_dirs = get_non_hidden_dirs(directory_path)
            if approved_sub_dirs == []:
                logger.debug("No subdirectories in %s", directory)
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

                if not (destination_path / item).exists():
                    logger.debug("Source path in research_dir_funnel: %s", source_path)
                    logger.debug(
                        "Destination path in research_dir_funnel: %s", destination_path
                    )
                    moved_dir_path = shutil.move(source_path, destination_path)
                    logger.info(
                        "Directory %s was moved to %s", source_path, moved_dir_path
                    )

                else:
                    raise FileExistsError(
                        f"Cannot move {item} into {destination_path} because it already exists"
                    )

    except EmptyDirectory as ed:
        logger.error("EmptyDirectory in research_dir_funnel: %s", ed)
        raise

    except FileExistsError as fee:
        logger.error("FileExistsError in research_dir_funnel: %s", fee)
        raise

    logger.debug("Function completed: research_dir_funnel")
    logger.info("Research directory organized!")


def college_dir_funnel(home: Path, desktop_flag: bool = False):
    """
    move directories to College directory
    if they start with 'CS'
    """

    try:
        approved_home_dirs = get_non_hidden_dirs(home)
        if approved_home_dirs == []:
            raise EmptyDirectory(home, college_dir_funnel.__name__)

        for directory in approved_home_dirs:
            if directory == "College":
                continue

            if (not desktop_flag) and directory == "Desktop":
                continue

            directory_path = home / directory
            approved_sub_dirs = get_non_hidden_dirs(directory_path)
            if approved_sub_dirs == []:
                logger.debug("No subdirectories in %s", directory)
                continue

            for item in approved_sub_dirs:
                is_college = item.startswith("CS")
                if not is_college:
                    continue

                source_path = home / directory / item
                destination_path = home / "College"
                if not (destination_path / item).exists():
                    logger.debug("Source path in college_dir_funnel: %s", source_path)
                    logger.debug(
                        "Destination path in college_dir_funnel: %s", destination_path
                    )
                    moved_dir_path = shutil.move(source_path, destination_path)
                    logger.info(
                        "Directory %s was move to %s", source_path, moved_dir_path
                    )
                else:
                    raise FileExistsError(
                        f"Cannot move {item} into {destination_path} because it already exists"
                    )

    except EmptyDirectory as ed:
        logger.error("EmptyDirectory in college_dir_funnel: %s", ed)
        raise

    except FileExistsError as fee:
        logger.error("FileExistsError in college_dir_funnel: %s", fee)
        raise

    logger.debug("Function completed: college_dir_funnel")
    logger.info("College directory organized!")


def hackathon_dir_funnel(home: Path, desktop_flag: bool = False):
    """
    move directories to Hackathons directory
    if they start with 'Hackathon'
    """

    try:
        approved_home_dirs = get_non_hidden_dirs(home)
        if approved_home_dirs == []:
            raise EmptyDirectory(home, hackathon_dir_funnel.__name__)

        for directory in approved_home_dirs:
            if directory == "Hackathons":
                continue

            if not desktop_flag and directory == "Desktop":
                continue

            directory_path = home / directory
            approved_sub_dirs = get_non_hidden_dirs(directory_path)
            if approved_sub_dirs == []:
                logger.debug("No subdirectories in %s", directory)
                continue

            for item in approved_sub_dirs:
                has_git_file = Path.exists(home / directory / item / ".git")
                is_hackathon = item.startswith("Hackathon")
                is_hackathon = is_hackathon and has_git_file
                if not is_hackathon:
                    continue

                source_path = home / directory / item
                destination_path = home / "Hackathons"

                if not (destination_path / item).exists():
                    logger.debug("Source path in hackathon_dir_funnel: %s", source_path)
                    logger.debug(
                        "Destination path in hackathon_dir_funnel: %s", destination_path
                    )
                    moved_dir_path = shutil.move(source_path, destination_path)
                    logger.info(
                        "Directory %s was move to %s", source_path, moved_dir_path
                    )
                else:
                    raise FileExistsError(
                        f"Cannot move {item} into {destination_path} because it already exists"
                    )

    except EmptyDirectory as ed:
        logger.error("EmptyDirectory in hackathon_dir_funnel: %s", ed)
        raise

    except FileExistsError as fee:
        logger.error("FileExistsError in hackathon_dir_funnel: %s", fee)
        raise

    logger.debug("Function completed: hackathon_dir_funnel")
    logger.info("Hackathon directory organized!")


def projects_dir_funnel(home: Path, desktop_flag: bool = False):
    """
    move directories to Projects
    if they contain a .git file
    and not already in Research
    """

    try:
        approved_home_dirs = get_non_hidden_dirs(home)
        if approved_home_dirs == []:
            raise EmptyDirectory(home, projects_dir_funnel.__name__)

        for directory in approved_home_dirs:
            if directory == "Projects":
                continue

            if directory == "Research":
                continue

            if not desktop_flag and directory == "Desktop":
                continue

            directory_path = home / directory
            approved_sub_dirs = get_non_hidden_dirs(directory_path)
            if approved_sub_dirs == []:
                logger.debug("No subdirectories in %s", directory)
                continue

            for item in approved_sub_dirs:
                has_git_file = Path.exists(home / directory / item / ".git")
                if not has_git_file:
                    continue

                source_path = home / directory / item
                destination_path = home / "Projects"
                if not (destination_path / item).exists():
                    logger.debug("Source path in projects_dir_funnel: %s", source_path)
                    logger.debug(
                        "Destination path in projects_dir_funnel: %s", destination_path
                    )
                    moved_dir_path = shutil.move(source_path, destination_path)
                    logger.info(
                        "Directory %s was moved to %s", source_path, moved_dir_path
                    )
                else:
                    raise FileExistsError(
                        f"Cannot move {item} into {destination_path} because it already exists"
                    )

    except EmptyDirectory as ed:
        logger.error("EmptyDirectory in projects_dir_funnel: %s", ed)
        raise

    except FileExistsError as fee:
        logger.error("FileExistsError in projects_dir_funnel: %s", fee)
        raise

    logger.debug("Function completed: projects_dir_funnel")
    logger.info("Projects directory organized!")


def backups_dir_funnel(home: Path, desktop_flag: bool = False):
    """
    move files to Backups
    if they contain 'key', 'backup', or 'recovery' in the filename
    """

    try:
        approved_home_dirs = get_non_hidden_dirs(home)
        if approved_home_dirs == []:
            raise EmptyDirectory(home, backups_dir_funnel.__name__)

        for directory in approved_home_dirs:
            if (not desktop_flag) and directory == "Desktop":
                continue

            if directory == "Backups":
                continue

            directory_path = home / directory
            approved_files = get_non_hidden_files(directory_path)
            backup_files = [
                file
                for file in approved_files
                if "backup" in file or "recovery" in file or "key" in file
            ]
            logger.info("Backup files to be moved: %s", backup_files)

            if backup_files == []:
                logger.debug("No backup files in %s", directory)
                continue

            for file in backup_files:
                source_path = home / directory / file
                destination_path = home / "Backups"
                logger.debug("Source path in backups_dir_funnel: %s", source_path)
                logger.debug(
                    "Destination path in backups_dir_funnel: %s", destination_path
                )
                shutil.move(source_path, destination_path)
                logger.info("File %s moved to %s", source_path, destination_path)
                logger.debug(
                    f"Current Backups directory: {get_non_hidden_files(destination_path)}"
                )

    except EmptyDirectory as ed:
        logger.error("EmptyDirectory in backups_dir_funnel: %s", ed)
        raise

    except FileExistsError as fee:
        logger.error("FileExistsError in backups_dir_funnel: %s", fee)
        raise

    except OSError as ose:
        logger.error("OSError in backups_dir_funnel: %s", ose)
        raise

    logger.debug("Function completed: backups_dir_funnel")
    logger.info("Backups directory organized!")


def cleanup_downloads_dir(home: Path):
    """
    clean up Downloads directory by moving files
    based on their file extension to other directories
    """

    try:
        # funnel remaining files into Documents, Pictures, Music, Videos
        downloads_path = home / "Downloads"
        downloads_files = get_non_hidden_files(downloads_path)
        if downloads_files == []:
            raise EmptyDirectory(downloads_path, cleanup_downloads_dir.__name__)

        funnel_dir_ext_map = {
            "Documents": [".pdf", ".doc", ".docx", ".txt"],
            "Pictures": [".png", ".jpg", ".jpeg", ".svg"],
            "Music": [".wav", ".mp3", ".mp4", ".ogg"],
            "Videos": [".mov", ".avi", ".wmv", ".flv", ".avchd"],
        }

        for file in downloads_files:
            file_ext = Path(file).suffix
            for directory, ext_list in funnel_dir_ext_map.items():
                if file_ext in ext_list:
                    source_path = home / "Downloads" / file
                    destination_path = home / directory
                    logger.debug(
                        "Source path in cleanup_downloads_dir: %s", source_path
                    )
                    logger.debug(
                        "Destination path in cleanup_downloads_dir: %s",
                        destination_path,
                    )
                    shutil.move(source_path, destination_path)
                    logger.info("File %s moved to %s", source_path, destination_path)

                    break

    except EmptyDirectory as ed:
        logger.error("EmptyDirectory in cleanup_downloads_dir: %s", ed)
        raise

    except FileExistsError as fee:
        logger.error("FileExistsError in cleanup_downloads_dir: %s", fee)
        raise

    except OSError as ose:
        logger.error("OSError in cleanup_downloads_dir: %s", ose)
        raise

    logger.debug("Function completed: cleanup_downloads_dir")
    logger.info("Downloads directory cleaned up!")


def del_zip_files(home: Path, del_flag: bool = False):
    """
    if delete flag is True, delete the zip files in Downloads
    """

    if del_flag:
        try:
            downloads_path = home / "Downloads"
            downloads_files = get_non_hidden_files(downloads_path)
            if downloads_files == []:
                raise EmptyDirectory(downloads_path, del_zip_files.__name__)

            def is_zip_file(file):
                if ".zip" in file:
                    return True
                if ".deb" in file:
                    return True
                if ".tar.gz" in file:
                    return True
                if ".tar.bz2" in file:
                    return True
                if ".tar.xz" in file:
                    return True
                return False

            zip_files = list(filter(is_zip_file, downloads_files))
            is_sure = input(
                f"Are you sure you want to delete these zip files? (y/n)\n{zip_files}"
            )

            if is_sure in ("y", "Y"):
                for file in zip_files:
                    os.remove(downloads_path / file)
                    logger.info("File: %s removed", file)

            else:
                sys.exit(1)

        except EmptyDirectory as ed:
            logger.error("Empty directory in del_zip_files: %s", ed)
            raise

        except OSError as oe:
            logger.error("Deletion Issue, OSError: %s", oe)
            raise

        logger.info("Compressed files deleted!")
