#!/usr/bin/python3

"""Tests for file_organizer"""

import shutil
from pathlib import Path
from random import randint

import pytest

import app.file_organizer as fo
from app.special_exceptions import EmptyDirectory


@pytest.fixture
def setup_tmp_path(tmp_path: Path):
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
        "key1.txt",
        "recovery1.txt",
        "backup1.txt",
    ]

    hackathon_dirs = [
        "Hackathon_Velocity",
        "Hackathon_Yeti",
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
        if len(Path(other).suffix) == 0:
            (tmp_path / root_dirs[i] / other).mkdir()
        else:
            (tmp_path / root_dirs[i] / other).touch()

    for git_dir in project_dirs + research_dirs + hackathon_dirs:
        i = randint(0, len(root_dirs) - 1)
        (tmp_path / root_dirs[i] / git_dir).mkdir()
        (tmp_path / root_dirs[i] / git_dir / ".git").touch()

    for desk_dir in desktop_dirs:
        if len(Path(desk_dir).suffix) == 0:
            (tmp_path / "Desktop" / desk_dir).mkdir()
            (tmp_path / "Desktop" / desk_dir / ".git").touch()
        else:
            (tmp_path / "Desktop" / desk_dir).touch()

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
        "randfile19.svg",
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
def test_get_non_hidden_files_with_None():
    assert fo.get_non_hidden_files(None) == []


def test_get_non_hidden_files_with_no_hidden_files(tmp_path):
    (tmp_path / "file.txt").touch()
    (tmp_path / "words.docx").touch()

    expected_files = ["file.txt", "words.docx"]
    assert sorted(fo.get_non_hidden_files(tmp_path)) == sorted(expected_files)


def test_get_non_hidden_files_with_hidden_files(tmp_path):
    (tmp_path / "file.txt").touch()
    (tmp_path / ".hidden1.txt").touch()
    (tmp_path / "document.pdf").touch()
    (tmp_path / ".b.sh").touch()

    expected_files = ["file.txt", "document.pdf"]
    assert sorted(fo.get_non_hidden_files(tmp_path)) == sorted(expected_files)


def test_get_non_hidden_files_with_only_hidden_files(tmp_path):
    (tmp_path / ".hidden1.txt").touch()
    (tmp_path / ".bin.sh").touch()

    assert fo.get_non_hidden_files(tmp_path) == []


def test_get_non_hidden_files_with_mixed_dirs_files(tmp_path):
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

    actual_directories = [d for d in tmp_path.iterdir() if d.is_dir()]
    assert actual_directories == []


# research_dir_funnel tests
def test_research_dir_funnel_empty_home(setup_tmp_path, monkeypatch):
    monkeypatch.setattr("app.file_organizer.get_non_hidden_dirs", lambda x: [])

    with pytest.raises(EmptyDirectory):
        fo.research_dir_funnel(setup_tmp_path)


def test_research_dir_funnel_with_desktop(setup_tmp_path):
    research = setup_tmp_path / "Research"
    expected_dirs = [
        "Learn_Go",
        "Test_Selenium",
        "Study_Javascript",
    ]
    desktop_flag = True

    fo.research_dir_funnel(setup_tmp_path, desktop_flag)

    for exp_dir in expected_dirs:
        assert (research / exp_dir).exists()


def test_research_dir_funnel_existing_dirs_with_desktop(setup_tmp_path):
    research = setup_tmp_path / "Research"
    existing_dirs = [
        "Learn_Go",
        "Test_Selenium",
        "Study_Javascript",
    ]
    desktop_flag = True

    for ex_dir in existing_dirs:
        if not (research / ex_dir).exists():
            (research / ex_dir).mkdir()

    with pytest.raises(FileExistsError):
        fo.research_dir_funnel(setup_tmp_path, desktop_flag)


def test_research_dir_funnel_without_desktop(setup_tmp_path):
    desktop = setup_tmp_path / "Desktop"
    research = setup_tmp_path / "Research"
    excluded_dirs = []
    expected_dirs = [
        "Learn_Go",
        "Test_Selenium",
        "Study_Javascript",
    ]

    for item in desktop.iterdir():
        excluded_dirs.append(str(item.stem))

    expected_dirs = list(set(expected_dirs) - set(excluded_dirs))

    fo.research_dir_funnel(setup_tmp_path)
    for exp_dir in expected_dirs:
        assert (research / exp_dir).exists()

    for ex_dir in excluded_dirs:
        assert not (research / ex_dir).exists()


def test_research_dir_funnel_existing_dirs_without_desktop(setup_tmp_path):
    research = setup_tmp_path / "Research"
    desktop = setup_tmp_path / "Desktop"
    excluded_dirs = []
    existing_dirs = [
        "Learn_Go",
        "Test_Selenium",
        "Study_Javascript",
    ]

    for item in desktop.iterdir():
        excluded_dirs.append(str(item.stem))

    remaining_dirs = list(set(existing_dirs) - set(excluded_dirs))

    for ex_dir in remaining_dirs:
        if not (research / ex_dir).exists():
            (research / ex_dir).mkdir()

    if remaining_dirs:
        with pytest.raises(FileExistsError):
            fo.research_dir_funnel(setup_tmp_path)


# college_dir_funnel tests
def test_college_dir_funnel_empty_home(setup_tmp_path, monkeypatch):
    monkeypatch.setattr("app.file_organizer.get_non_hidden_dirs", lambda x: [])

    with pytest.raises(EmptyDirectory):
        fo.college_dir_funnel(setup_tmp_path)


def test_college_dir_funnel_with_desktop(setup_tmp_path):
    college = setup_tmp_path / "College"
    expected_dirs = [
        "CS_1250",
        "CSM_Assignments",
    ]
    desktop_flag = True

    fo.college_dir_funnel(setup_tmp_path, desktop_flag)

    for exp_dir in expected_dirs:
        assert (college / exp_dir).exists()


def test_college_dir_funnel_existing_dirs_with_desktop(setup_tmp_path):
    college = setup_tmp_path / "College"
    existing_dirs = [
        "CS_1250",
        "CSM_Assignments",
    ]
    desktop_flag = True

    for ex_dir in existing_dirs:
        if not (college / ex_dir).exists():
            (college / ex_dir).mkdir()

    with pytest.raises(FileExistsError):
        fo.college_dir_funnel(setup_tmp_path, desktop_flag)


def test_college_dir_funnel_without_desktop(setup_tmp_path):
    college = setup_tmp_path / "College"
    desktop = setup_tmp_path / "Desktop"
    excluded_dirs = []
    expected_dirs = [
        "CS_1250",
        "CSM_Assignments",
    ]

    for item in desktop.iterdir():
        excluded_dirs.append(str(item.name))

    fo.college_dir_funnel(setup_tmp_path)

    expected_dirs = list(set(expected_dirs) - set(excluded_dirs))
    for exp_dir in expected_dirs:
        assert (college / exp_dir).exists()

    for ex_dir in excluded_dirs:
        assert not (college / ex_dir).exists()


def test_college_dir_funnel_existing_dirs_without_desktop(setup_tmp_path):
    college = setup_tmp_path / "College"
    desktop = setup_tmp_path / "Desktop"
    research = setup_tmp_path / "Research"
    excluded_dirs = []
    existing_dirs = [
        "CS_1250",
        "CSM_Assignments",
    ]

    for item in desktop.iterdir():
        excluded_dirs.append(str(item.stem))

    remaining_dirs = list(set(existing_dirs) - set(excluded_dirs))

    for ex_dir in remaining_dirs:
        if not (college / ex_dir).exists():
            (college / ex_dir).mkdir()

    if remaining_dirs:
        for r_dir in remaining_dirs:
            if not (research / r_dir).exists():
                (research / r_dir).mkdir()
        with pytest.raises(FileExistsError):
            fo.college_dir_funnel(setup_tmp_path)


# hackathon_dir_funnel tests
def test_hackathon_dir_funnel_empty_home(setup_tmp_path, monkeypatch):
    monkeypatch.setattr("app.file_organizer.get_non_hidden_dirs", lambda x: [])

    with pytest.raises(EmptyDirectory):
        fo.hackathon_dir_funnel(setup_tmp_path)


def test_hackathon_dir_funnel_with_desktop(setup_tmp_path):
    hackathon = setup_tmp_path / "Hackathons"
    expected_dirs = [
        "Hackathon_Velocity",
        "Hackathon_Yeti",
    ]
    desktop_flag = True

    fo.hackathon_dir_funnel(setup_tmp_path, desktop_flag)

    for exp_dir in expected_dirs:
        assert (hackathon / exp_dir).exists()


def test_hackathon_dir_funnel_existing_dirs_with_desktop(setup_tmp_path):
    hackathon = setup_tmp_path / "Hackathons"
    existing_dirs = [
        "Hackathon_Velocity",
        "Hackathon_Yeti",
    ]
    desktop_flag = True

    for ex_dir in existing_dirs:
        if not (hackathon / ex_dir).exists():
            (hackathon / ex_dir).mkdir()

    with pytest.raises(FileExistsError):
        fo.hackathon_dir_funnel(setup_tmp_path, desktop_flag)


def test_hackathon_dir_funnel_without_desktop(setup_tmp_path):
    hackathon = setup_tmp_path / "Hackathons"
    desktop = setup_tmp_path / "Desktop"
    excluded_dirs = []
    expected_dirs = [
        "Hackathon_Velocity",
        "Hackathon_Yeti",
    ]

    for item in desktop.iterdir():
        excluded_dirs.append(str(item.stem))

    expected_dirs = list(set(expected_dirs) - set(excluded_dirs))

    fo.hackathon_dir_funnel(setup_tmp_path)
    if expected_dirs:
        for exp_dir in expected_dirs:
            assert (hackathon / exp_dir).exists()

        for ex_dir in excluded_dirs:
            assert not (hackathon / ex_dir).exists()


def test_hackathon_dir_funnel_existing_dirs_without_desktop(setup_tmp_path):
    hackathon = setup_tmp_path / "Hackathons"
    desktop = setup_tmp_path / "Desktop"
    excluded_dirs = []
    existing_dirs = [
        "Hackathon_Velocity",
        "Hackathon_Yeti",
    ]

    for item in desktop.iterdir():
        excluded_dirs.append(str(item.stem))

    remaining_dirs = list(set(existing_dirs) - set(excluded_dirs))

    for ex_dir in remaining_dirs:
        if not (hackathon / ex_dir).exists():
            (hackathon / ex_dir).mkdir()

    if remaining_dirs:
        with pytest.raises(FileExistsError):
            fo.hackathon_dir_funnel(setup_tmp_path)


# projects_dir_funnel tests
def test_projects_dir_funnel_empty_home(setup_tmp_path, monkeypatch):
    monkeypatch.setattr("app.file_organizer.get_non_hidden_dirs", lambda x: [])

    with pytest.raises(EmptyDirectory):
        fo.projects_dir_funnel(setup_tmp_path)


def test_projects_dir_funnel_with_desktop(setup_tmp_path):
    projects = setup_tmp_path / "Projects"
    research = setup_tmp_path / "Research"
    research_dirs = []
    expected_dirs = [
        "project1",
        "project2",
        "Terminal_Search",
        "OneStopQR",
        "ElectricGuitar",
        "Integer_Game",
    ]
    desktop_flag = True

    fo.research_dir_funnel(setup_tmp_path)

    for res_dir in research.iterdir():
        research_dirs.append(str(res_dir.name))

    fo.projects_dir_funnel(setup_tmp_path, desktop_flag)

    expected_dirs = list(set(expected_dirs) - set(research_dirs))

    for exp_dir in expected_dirs:
        assert (projects / exp_dir).exists()


def test_projects_dir_funnel_existing_dirs_with_desktop(setup_tmp_path):
    projects = setup_tmp_path / "Projects"
    research = setup_tmp_path / "Research"
    existing_dirs = [
        "project1",
        "project2",
        "Terminal_Search",
        "OneStopQR",
        "ElectricGuitar",
        "Integer_Game",
    ]
    excluded_dirs = []
    desktop_flag = True

    fo.research_dir_funnel(setup_tmp_path, desktop_flag)

    for res_dir in research.iterdir():
        excluded_dirs.append(str(res_dir.name))

    existing_dirs = list(set(existing_dirs) - set(excluded_dirs))

    for ex_dir in existing_dirs:
        if not (projects / ex_dir).exists():
            (projects / ex_dir).mkdir()

    if existing_dirs:
        with pytest.raises(FileExistsError):
            fo.projects_dir_funnel(setup_tmp_path, desktop_flag)


def test_projects_dir_funnel_without_desktop(setup_tmp_path):
    projects = setup_tmp_path / "Projects"
    research = setup_tmp_path / "Research"
    desktop = setup_tmp_path / "Desktop"
    excluded_dirs = []
    expected_dirs = [
        "Terminal_Search",
        "OneStopQR",
        "ElectricGuitar",
        "Integer_Game",
    ]

    for item in desktop.iterdir():
        excluded_dirs.append(str(item.stem))

    fo.research_dir_funnel(setup_tmp_path)

    for res_dir in research.iterdir():
        excluded_dirs.append(str(res_dir.stem))

    expected_dirs = list(set(expected_dirs) - set(excluded_dirs))

    fo.projects_dir_funnel(setup_tmp_path)
    if expected_dirs:
        for exp_dir in expected_dirs:
            assert (projects / exp_dir).exists()

        for ex_dir in excluded_dirs:
            assert not (projects / ex_dir).exists()


def test_projects_dir_funnel_existing_dirs_without_desktop(setup_tmp_path):
    projects = setup_tmp_path / "Projects"
    research = setup_tmp_path / "Research"
    desktop = setup_tmp_path / "Desktop"
    excluded_dirs = []
    existing_dirs = [
        "Terminal_Search",
        "OneStopQR",
        "ElectricGuitar",
        "Integer_Game",
    ]

    for item in desktop.iterdir():
        excluded_dirs.append(str(item.stem))

    fo.research_dir_funnel(setup_tmp_path)

    for res_dir in research.iterdir():
        excluded_dirs.append(str(res_dir.stem))

    remaining_dirs = list(set(existing_dirs) - set(excluded_dirs))

    for ex_dir in remaining_dirs:
        if not (projects / ex_dir).exists():
            (projects / ex_dir).mkdir()

    if remaining_dirs:
        with pytest.raises(FileExistsError):
            fo.projects_dir_funnel(setup_tmp_path)


def test_backups_dir_funnel_empty_home(setup_tmp_path, monkeypatch):
    monkeypatch.setattr("app.file_organizer.get_non_hidden_dirs", lambda x: [])

    with pytest.raises(EmptyDirectory):
        fo.backups_dir_funnel(setup_tmp_path)


def test_backups_dir_funnel_with_desktop(setup_tmp_path):
    backups = setup_tmp_path / "Backups"
    desktop_flag = True
    expected_files = [
        "backup-recovery.pdf",
        "recovery1.txt",
        "backup1.txt",
        "recovery-key.txt",
        "backup.txt",
        "teehee-key.txt",
        "backup-recovery-key.txt",
        "randfile18_backup.txt",
    ]

    fo.backups_dir_funnel(setup_tmp_path, desktop_flag)

    for exp_file in expected_files:
        assert (backups / exp_file).exists()


def test_backups_dir_funnel_existing_dirs_with_desktop(setup_tmp_path):
    backups = setup_tmp_path / "Backups"
    existing_files = [
        "backup-recovery.pdf",
        "recovery1.txt",
        "backup1.txt",
        "recovery-key.txt",
        "backup.txt",
        "teehee-key.txt",
        "backup-recovery-key.txt",
        "randfile18_backup.txt",
    ]
    desktop_flag = True

    for ex_file in existing_files:
        if not (backups / ex_file).exists():
            (backups / ex_file).touch()

    with pytest.raises(shutil.Error):
        fo.backups_dir_funnel(setup_tmp_path, desktop_flag)


def test_backups_dir_funnel_without_desktop(setup_tmp_path):
    backups = setup_tmp_path / "Backups"
    desktop = setup_tmp_path / "Desktop"
    excluded_files = []
    expected_files = [
        "backup-recovery.pdf",
        "recovery1.txt",
        "backup1.txt",
        "recovery-key.txt",
        "backup.txt",
        "teehee-key.txt",
        "backup-recovery-key.txt",
        "randfile18_backup.txt",
    ]

    for item in desktop.iterdir():
        excluded_files.append(str(item.name))

    expected_files = list(set(expected_files) - set(excluded_files))

    fo.backups_dir_funnel(setup_tmp_path)

    for exp_file in expected_files:
        assert (backups / exp_file).exists()

    for ex_file in excluded_files:
        assert not (backups / ex_file).exists()


def test_backups_dir_funnel_existing_dirs_without_desktop(setup_tmp_path):
    backups = setup_tmp_path / "Backups"
    desktop = setup_tmp_path / "Desktop"
    excluded_files = []
    existing_files = [
        "backup-recovery.pdf",
        "recovery1.txt",
        "backup1.txt",
        "recovery-key.txt",
        "backup.txt",
        "teehee-key.txt",
        "backup-recovery-key.txt",
        "randfile18_backup.txt",
    ]

    for item in desktop.iterdir():
        excluded_files.append(str(item.name))

    remaining_files = list(set(existing_files) - set(excluded_files))

    for ex_file in remaining_files:
        if not (backups / ex_file).exists():
            (backups / ex_file).mkdir()

    if remaining_files:
        with pytest.raises(shutil.Error):
            fo.backups_dir_funnel(setup_tmp_path)


def test_cleanup_downloads_dir_with_empty_downloads(setup_tmp_path, monkeypatch):
    monkeypatch.setattr("app.file_organizer.get_non_hidden_files", lambda x: [])

    with pytest.raises(EmptyDirectory):
        fo.cleanup_downloads_dir(setup_tmp_path)


def test_cleanup_downloads_dir_without_del_zip_files(setup_tmp_path):
    downloads = setup_tmp_path / "Downloads"
    documents = setup_tmp_path / "Documents"
    pictures = setup_tmp_path / "Pictures"
    music = setup_tmp_path / "Music"
    videos = setup_tmp_path / "Videos"

    downloads_files = [
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
        "randfile19.svg",
    ]

    exp_docs = [
        "randfile1.txt",
        "randfile2.pdf",
        "randfile3.doc",
        "randfile10.docx",
        "randfile18_backup.txt",
    ]
    exp_pics = [
        "randfile4.png",
        "randfile5.jpg",
        "randfile11.jpeg",
        "randfile19.svg",
    ]
    exp_music = [
        "randfile7.wav",
        "randfile9.ogg",
        "randfile12.mp3",
        "randfile13.mp4",
    ]
    exp_vids = [
        "randfile8.avi",
        "randfile6.mov",
    ]

    fo.cleanup_downloads_dir(setup_tmp_path)

    for exp_doc in exp_docs:
        assert (documents / exp_doc).exists()
        assert not (downloads / exp_doc).exists()

    for exp_pic in exp_pics:
        assert (pictures / exp_pic).exists()
        assert not (downloads / exp_pic).exists()

    for exp_mus in exp_music:
        assert (music / exp_mus).exists()
        assert not (downloads / exp_mus).exists()

    for exp_vid in exp_vids:
        assert (videos / exp_vid).exists()
        assert not (downloads / exp_vid).exists()

    remaining_dirs = list(
        set(downloads_files) - set(exp_docs + exp_pics + exp_music + exp_vids)
    )

    for exp_dir in remaining_dirs:
        assert (downloads / exp_dir).exists()


def test_del_zip_files_with_empty_directory(setup_tmp_path, monkeypatch):
    monkeypatch.setattr("app.file_organizer.get_non_hidden_files", lambda x: [])
    del_flag = True

    with pytest.raises(EmptyDirectory):
        fo.del_zip_files(setup_tmp_path, del_flag)


def test_del_zip_files_with_no_flag(setup_tmp_path):
    downloads = setup_tmp_path / "Downloads"
    downloads_files = [
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
        "randfile19.svg",
    ]

    for file in downloads_files:
        if not (downloads / file).exists():
            (downloads / file).touch()

    fo.del_zip_files(setup_tmp_path)

    for file in downloads_files:
        assert (downloads / file).exists()


def test_del_zip_files_with_flag_and_y_input(setup_tmp_path, monkeypatch):
    downloads = setup_tmp_path / "Downloads"
    tbr_files = [
        "randfile14.zip",
        "randfile15.tar.gz",
        "randfile16.deb",
        "randfile17.tar.bz2",
    ]
    del_flag = True

    monkeypatch.setattr("builtins.input", lambda _: "y")
    fo.del_zip_files(setup_tmp_path, del_flag)

    for file in tbr_files:
        assert not (downloads / file).exists()


def test_del_zip_files_with_flag_and_Y_input(setup_tmp_path, monkeypatch):
    downloads = setup_tmp_path / "Downloads"
    tbr_files = [
        "randfile14.zip",
        "randfile15.tar.gz",
        "randfile16.deb",
        "randfile17.tar.bz2",
    ]
    del_flag = True

    monkeypatch.setattr("builtins.input", lambda _: "Y")
    fo.del_zip_files(setup_tmp_path, del_flag)

    for file in tbr_files:
        assert not (downloads / file).exists()


def test_del_zip_files_with_flag_and_n_input(setup_tmp_path, monkeypatch):
    downloads = setup_tmp_path / "Downloads"
    downloads_files = [
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
        "randfile19.svg",
    ]
    del_flag = True

    monkeypatch.setattr("builtins.input", lambda _: "n")
    with pytest.raises(SystemExit):
        fo.del_zip_files(setup_tmp_path, del_flag)

    for file in downloads_files:
        assert (downloads / file).exists()
