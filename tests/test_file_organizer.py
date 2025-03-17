#!/usr/bin/python3

"""Tests for file_organizer"""

from pathlib import Path
from random import randint

import pytest

import app.file_organizer as fo
from app.special_exceptions import EmptyDirectory


@pytest.fixture()
def setup_tmp_path(tmp_path):
    root_dirs = [
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

    other_dirs = [
        "CS_1250",
        "CSM_Assignments",
        "Hackathon_Wrong1",
        "Hackathon_Wrong2",
        "Random_Dir",
        "Random_Dir2",
        "Learn_Wrong1",
        "Study_Wrong2",
        "Test_Wrong3",
        "teehee-key.txt",
        "backup-recovery.pdf",
    ]

    hackathon_dirs = [
        "Hackathon_Velocity",
        "Hackathon_Yeti",
        "key1.txt",
    ]

    research_dirs = [
        "Learn_Go",
        "Test_Selenium",
        "Study_Javascript",
        "recovery1.txt",
    ]

    project_dirs = [
        "Terminal_Search",
        "OneStopQR",
        "ElectricGuitar",
        "Integer_Game",
        "backup1.txt",
    ]

    desktop_dirs = [
        "project1",
        "project2",
        "recovery-key.txt",
        "backup.txt",
        "backup-recovery-key.txt",
    ]

    for directory in root_dirs:
        (tmp_path / directory).mkdir()

    for other in other_dirs:
        i = randint(0, len(root_dirs) - 1)
        (tmp_path / root_dirs[i] / other).mkdir()

    for git_dir in project_dirs + research_dirs + hackathon_dirs:
        i = randint(0, len(root_dirs) - 1)
        (tmp_path / root_dirs[i] / git_dir).mkdir()
        (tmp_path / root_dirs[i] / git_dir / ".git").touch()

    for desk_dir in desktop_dirs:
        (tmp_path / "Desktop" / desk_dir).mkdir()
        (tmp_path / "Desktop" / desk_dir / ".git").touch()

    rand_downloads_files = [
        "randfile1.txt",
        "randfile2.pdf",
        "randfile3.doc",
        "randfile4.png",
        "randfile5.jpg",
        "randfile6.mov",
        "randfile7.wav",
        "randfile8.avi",
        "randfile9.ogg",
        "randfile10.docx",
        "randfile11.jpeg",
        "randfile12.mp3",
        "randfile13.mp4",
        "randfile14.zip",
        "randfile15.tar.gz",
        "randfile16.deb",
        "randfile17.tar.bz2",
        "randfile18_backup.txt",
    ]

    for file in rand_downloads_files:
        (tmp_path / "Downloads" / file).touch()

    return tmp_path


# get_non_hidden_dirs tests
def test_get_non_hidden_dirs_with_none():
    assert fo.get_non_hidden_dirs(None) == []


def test_get_non_hidden_dirs_with_no_hidden_dirs(tmp_path):
    (tmp_path / "dir1").mkdir()
    (tmp_path / "dir2").mkdir()

    expected_dirs = ["dir1", "dir2"]
    assert sorted(fo.get_non_hidden_dirs(tmp_path)) == sorted(expected_dirs)


def test_get_non_hidden_dirs_with_hidden_dirs(tmp_path):
    (tmp_path / "dir1").mkdir()
    (tmp_path / ".hidden_dir1").mkdir()
    (tmp_path / "dir2").mkdir()

    expected_dirs = ["dir1", "dir2"]
    assert sorted(fo.get_non_hidden_dirs(tmp_path)) == sorted(expected_dirs)


def test_get_non_hidden_dirs_with_only_hidden_dirs(tmp_path):
    (tmp_path / ".hidden_dir1").mkdir()
    (tmp_path / ".hidden_dir2").mkdir()

    assert fo.get_non_hidden_dirs(tmp_path) == []


def test_get_non_hidden_dirs_with_mixed_files_dirs(tmp_path):
    (tmp_path / "dir1").mkdir()
    (tmp_path / ".hidden_dir1").mkdir()
    (tmp_path / "file.txt").touch()
    (tmp_path / ".hidden_file.txt").touch()
    (tmp_path / "file.pdf").touch()
    (tmp_path / "dir2").mkdir()

    expected_dirs = ["dir1", "dir2"]
    assert sorted(fo.get_non_hidden_dirs(tmp_path)) == sorted(expected_dirs)


# get_non_hidden_files tests
def get_non_hidden_files_with_None():
    assert fo.get_non_hidden_files(None) == []


def get_non_hidden_files_with_no_hidden_files(tmp_path):
    (tmp_path / "file.txt").touch()
    (tmp_path / "words.docx").touch()

    expected_files = ["file.txt", "words.docx"]
    assert sorted(fo.get_non_hidden_files(tmp_path)) == sorted(expected_files)


def get_non_hidden_files_with_hidden_files(tmp_path):
    (tmp_path / "file.txt").touch()
    (tmp_path / ".hidden1.txt").touch()
    (tmp_path / "document.pdf").touch()
    (tmp_path / ".b.sh").touch()

    expected_files = ["file.txt", "document.pdf"]
    assert sorted(fo.get_non_hidden_files(tmp_path)) == sorted(expected_files)


def get_non_hidden_files_with_only_hidden_files(tmp_path):
    (tmp_path / ".hidden1.txt").touch()
    (tmp_path / ".bin.sh").touch()

    assert fo.get_non_hidden_files(tmp_path) == []


def get_non_hidden_files_with_mixed_dirs_files(tmp_path):
    (tmp_path / ".hidden1.txt").touch()
    (tmp_path / ".bin").mkdir()
    (tmp_path / "dir1").mkdir()
    (tmp_path / "a.sh").touch()
    (tmp_path / "file.txt").touch()

    expected_files = ["a.sh", "file.txt"]
    assert sorted(fo.get_non_hidden_files(tmp_path)) == sorted(expected_files)


# create_require_dirs tests
def test_create_require_dirs_creates_dirs(tmp_path):
    dirs_list = ["dir1", "dir2"]
    fo.create_required_dirs(dirs_list, tmp_path)

    for directory in dirs_list:
        assert (tmp_path / directory).exists


def test_create_require_dirs_skips_existing(tmp_path):
    dirs_list = ["dir1", "dir2", "dir3"]
    for directory in dirs_list:
        (tmp_path / directory).mkdir()

    fo.create_required_dirs(dirs_list, tmp_path)
    for directory in dirs_list:
        assert (tmp_path / directory).exists


def test_create_require_dirs_empty_list(tmp_path):
    fo.create_required_dirs([], tmp_path)

    actual_directories = [d for d in tmp_path.iterdir() if d.isdir()]
    assert actual_directories == []


# research_dir_funnel tests
def test_research_dir_funnel_empty_home(tmp_path, monkeypatch):
    monkeypatch.setattr("app.file_organizer.get_non_hidden_dirs", lambda x: [])

    with pytest.raises(EmptyDirectory):
        fo.research_dir_funnel(tmp_path)


def test_research_dir_funnel_with_desktop(tmp_path):
    expected_dirs = [
        "Learn_Go",
        "Test_Selenium",
        "Study_Javascript",
    ]
    desktop_flag = True

    home = tmp_path
    fo.research_dir_funnel(home, desktop_flag)

    for exp_dir in expected_dirs:
        assert (home / "Research" / exp_dir).exists()


def test_research_dir_funnel_existing_dirs_with_desktop(tmp_path):
    home = tmp_path
    existing_dirs = [
        "Learn_Go",
        "Test_Selenium",
        "Study_Javascript",
    ]
    desktop_flag = True

    for ex_dir in existing_dirs:
        if not (home / "Research" / ex_dir).exists():
            (home / "Research" / ex_dir).mkdir()

    with pytest.raises(FileExistsError):
        fo.research_dir_funnel(home, desktop_flag)


def test_research_dir_funnel_without_desktop(tmp_path):
    home = tmp_path
    desktop = home / "Desktop"
    excluded_dirs = []
    expected_dirs = [
        "Learn_Go",
        "Test_Selenium",
        "Study_Javascript",
    ]

    for item in desktop.iterdir():
        excluded_dirs.append(str(item.stem))

    expected_dirs = list(set(expected_dirs) - set(excluded_dirs))

    fo.research_dir_funnel(home)
    for exp_dir in expected_dirs:
        assert (home / "Research" / exp_dir).exists()


def test_research_dir_funnel_existing_dirs_without_desktop(tmp_path):
    home = tmp_path
    desktop = home / "Desktop"
    excluded_dirs = []
    existing_dirs = [
        "Learn_Go",
        "Test_Selenium",
        "Study_Javascript",
    ]
    desktop_flag = True

    for ex_dir in existing_dirs:
        if not (home / "Research" / ex_dir).exists():
            (home / "Research" / ex_dir).mkdir()

    for item in desktop.iterdir():
        excluded_dirs.append(str(item.stem))

    remaining_dirs = list(set(existing_dirs) - set(excluded_dirs))
    if remaining_dirs:
        with pytest.raises(FileExistsError):
            fo.research_dir_funnel(home, desktop_flag)


# college_dir_funnel tests
def test_college_dir_funnel_empty_home(tmp_path, monkeypatch):
    monkeypatch.setattr("app.file_organizer.get_non_hidden_dirs", lambda x: [])

    with pytest.raises(EmptyDirectory):
        fo.college_dir_funnel(tmp_path)


def test_college_dir_funnel_with_desktop(tmp_path):
    home = tmp_path
    expected_dirs = [
        "CS_1250",
        "CSM_Assignments",
    ]
    desktop_flag = True

    fo.college_dir_funnel(home, desktop_flag)

    for exp_dir in expected_dirs:
        assert (home / "College" / exp_dir).exists()


def test_college_dir_funnel_existing_dirs_with_desktop(tmp_path):
    home = tmp_path
    existing_dirs = [
        "CS_1250",
        "CSM_Assignments",
    ]
    desktop_flag = True

    for ex_dir in existing_dirs:
        if not (home / "College" / ex_dir).exists():
            (home / "College" / ex_dir).mkdir()

    with pytest.raises(FileExistsError):
        fo.college_dir_funnel(home, desktop_flag)


def test_college_dir_funnel_without_desktop(tmp_path):
    home = tmp_path
    desktop = home / "Desktop"
    excluded_dirs = []
    expected_dirs = [
        "CS_1250",
        "CSM_Assignments",
    ]

    for item in desktop.iterdir():
        excluded_dirs.append(str(item.stem))

    fo.college_dir_funnel(home)

    expected_dirs = list(set(expected_dirs) - set(excluded_dirs))
    for exp_dir in expected_dirs:
        assert (home / "College" / exp_dir).exists()


def test_college_dir_funnel_existing_dirs_without_desktop(tmp_path):
    home = tmp_path
    desktop = home / "Desktop"
    excluded_dirs = []
    existing_dirs = [
        "CS_1250",
        "CSM_Assignments",
    ]

    for ex_dir in existing_dirs:
        if not (home / "College" / ex_dir).exists():
            (home / "College" / ex_dir).mkdir()

    for item in desktop.iterdir():
        excluded_dirs.append(str(item.stem))

    remaining_dirs = list(set(existing_dirs) - set(excluded_dirs))
    if remaining_dirs:
        with pytest.raises(FileExistsError):
            fo.college_dir_funnel(home)


# hackathon_dir_funnel tests
def test_hackathon_dir_funnel_empty_home(tmp_path, monkeypatch):
    monkeypatch.setattr("app.file_organizer.get_non_hidden_dirs", lambda x: [])

    with pytest.raises(EmptyDirectory):
        fo.hackathon_dir_funnel(tmp_path)


def test_hackathon_dir_funnel_with_desktop(tmp_path):
    home = tmp_path
    expected_dirs = [
        "Hackathon_Velocity",
        "Hackathon_Yeti",
    ]
    desktop_flag = True

    fo.hackathon_dir_funnel(home, desktop_flag)

    for exp_dir in expected_dirs:
        assert (home / "Hackathons" / exp_dir).exists()


def test_hackathon_dir_funnel_existing_dirs_with_desktop(tmp_path):
    home = tmp_path
    existing_dirs = [
        "Hackathon_Velocity",
        "Hackathon_Yeti",
    ]
    desktop_flag = True

    for ex_dir in existing_dirs:
        if not (home / "Hackathons" / ex_dir).exists():
            (home / "Hackathons" / ex_dir).mkdir()

    with pytest.raises(FileExistsError):
        fo.hackathon_dir_funnel(home, desktop_flag)


def test_hackathon_dir_funnel_without_desktop(tmp_path):
    home = tmp_path
    desktop = home / "Desktop"
    excluded_dirs = []
    expected_dirs = [
        "Hackathon_Velocity",
        "Hackathon_Yeti",
    ]

    for item in desktop.iterdir():
        excluded_dirs.append(str(item.stem))

    expected_dirs = list(set(expected_dirs) - set(excluded_dirs))

    fo.hackathon_dir_funnel(home)
    if expected_dirs:
        for exp_dir in expected_dirs:
            assert (home / "Hackathons" / exp_dir).exists()


def test_hackathon_dir_funnel_existing_dirs_without_desktop(tmp_path):
    home = tmp_path
    desktop = home / "Desktop"
    excluded_dirs = []
    existing_dirs = [
        "Hackathon_Velocity",
        "Hackathon_Yeti",
    ]

    for item in desktop.iterdir():
        excluded_dirs.append(str(item.stem))

    for ex_dir in existing_dirs:
        if not (home / "Hackathons" / ex_dir).exists():
            (home / "Hackathons" / ex_dir).mkdir()

    remaining_dirs = list(set(existing_dirs) - set(excluded_dirs))
    if remaining_dirs:
        with pytest.raises(FileExistsError):
            fo.hackathon_dir_funnel(home)


# projects_dir_funnel tests
def test_projects_dir_funnel_empty_home(tmp_path, monkeypatch):
    monkeypatch.setattr("app.file_organizer.get_non_hidden_dirs", lambda x: [])

    with pytest.raises(EmptyDirectory):
        fo.projects_dir_funnel(tmp_path)


def test_projects_dir_funnel_with_desktop(tmp_path):
    home = tmp_path
    research = home / "Research"
    expected_research_dirs = []
    expected_dirs = [
        "Terminal_Search",
        "OneStopQR",
        "ElectricGuitar",
        "Integer_Game",
    ]
    desktop_flag = True

    for res_dir in research.iterdir():
        expected_research_dirs.append(res_dir)

    fo.projects_dir_funnel(home, desktop_flag)

    for res_dir in expected_research_dirs:
        assert (home / "Research" / res_dir).exists()

    for exp_dir in expected_dirs:
        assert (home / "Projects" / exp_dir).exists()


def test_projects_dir_funnel_existing_dirs_with_desktop(tmp_path):
    home = tmp_path
    research = home / "Research"
    existing_dirs = [
        "Terminal_Search",
        "OneStopQR",
        "ElectricGuitar",
        "Integer_Game",
    ]
    excluded_dirs = []
    desktop_flag = True

    for res_dir in research.iterdir():
        excluded_dirs.append(str(res_dir.stem))

    for ex_dir in existing_dirs:
        (home / "Projects" / ex_dir).mkdir()

    with pytest.raises(FileExistsError):
        fo.projects_dir_funnel(home, desktop_flag)


def test_projects_dir_funnel_without_desktop(tmp_path):
    home = tmp_path
    research = home / "Research"
    desktop = home / "Desktop"
    excluded_dirs = []
    expected_dirs = [
        "Terminal_Search",
        "OneStopQR",
        "ElectricGuitar",
        "Integer_Game",
    ]

    for item in desktop.iterdir():
        excluded_dirs.append(str(item.stem))

    for res_dir in research.iterdir():
        excluded_dirs.append(str(res_dir.stem))

    expected_dirs = list(set(expected_dirs) - set(excluded_dirs))

    fo.projects_dir_funnel(home)
    if expected_dirs:
        for exp_dir in expected_dirs:
            assert (home / "Projects" / exp_dir).exists()


def test_projects_dir_funnel_existing_dirs_without_desktop(tmp_path):
    home = tmp_path
    research = home / "Research"
    desktop = home / "Desktop"
    excluded_dirs = []
    existing_dirs = [
        "Terminal_Search",
        "OneStopQR",
        "ElectricGuitar",
        "Integer_Game",
    ]

    for item in desktop.iterdir():
        excluded_dirs.append(str(item.stem))

    for res_dir in research.iterdir():
        excluded_dirs.append(str(res_dir.stem))

    for ex_dir in existing_dirs:
        if not (home / "Projects" / ex_dir).exists():
            (home / "Projects" / ex_dir).mkdir()

    remaining_dirs = list(set(existing_dirs) - set(excluded_dirs))
    if remaining_dirs:
        with pytest.raises(FileExistsError):
            fo.projects_dir_funnel(home)


# TODO: backups dir funnel tests
def test_backups_dir_funnel_empty_home(tmp_path, monkeypatch):
    monkeypatch.setattr("app.file_organizer.get_non_hidden_dirs", lambda x: [])

    with pytest.raises(EmptyDirectory):
        fo.backups_dir_funnel(tmp_path)


def test_backups_dir_funnel_with_desktop(tmp_path):
    home = tmp_path
    backups = home / "Backups"
    expected_files =
