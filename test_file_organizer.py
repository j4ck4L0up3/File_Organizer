"""Tests for file_organizer"""

from logging import StreamHandler
from pathlib import Path
from random import randint

import pytest

import file_organizer as fo
from logger import get_test_logger

with open("./test.log", "wt", encoding="utf-8") as test_log_file:
    test_logger = get_test_logger(test_log_file)


@pytest.fixture(autouse=True)
def patch_logger(monkeypatch):
    monkeypatch.setattr("file_organizer.debug_logger", test_logger)


@pytest.fixture(autouse=True)
def clear_log_stream():
    for handler in test_logger.handlers:
        if isinstance(handler, StreamHandler):
            handler.stream = []


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
        "Hackathon_Velocity",
        "Random_Dir",
        "Random_Dir2",
    ]

    research_dirs = [
        "Learn_Go",
        "Test_Selenium",
        "Study_Javascript",
    ]

    project_dirs = [
        "Terminal_Search",
        "OneStopQR",
        "ElectricGuitar",
        "Integer_Game",
    ]

    for directory in root_dirs:
        (tmp_path / directory).mkdir()

    for other in other_dirs:
        i = randint(0, len(root_dirs) - 1)
        (tmp_path / root_dirs[i] / other).mkdir()

    for git_dir in project_dirs + research_dirs:
        i = randint(0, len(root_dirs) - 1)
        (tmp_path / root_dirs[i] / git_dir).mkdir()
        (tmp_path / root_dirs[i] / git_dir / ".git").touch()

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
