import os
from logger import get_debug_logger
import shutil
from pathlib import Path


debug_log_file = open('./debug.log', 'wt', encoding='utf-8')
debug_logger = get_debug_logger(debug_log_file)

# get list of non-hidden directories
def get_non_hidden_dirs(directory: Path=None) -> list:
    if directory is None:
        return []
    
    approved_items = [item for item in os.listdir(directory) if not item.startswith(".")]
    approved_dirs = [item for item in approved_items if os.path.isdir(Path(directory, item))]
    debug_logger.debug('Approved Directories: %s', approved_dirs)
    return approved_dirs


# get list of non-hidden files
def get_non_hidden_files(directory: Path=None) -> list:
    if directory == None:
        return None
    
    approved_items = [item for item in os.listdir(directory) if not item.startswith(".")]
    approved_files = [file for file in approved_items if os.path.isfile(Path(directory, file))]
    debug_logger.debug('Approved Files: %s', approved_files)
    return approved_files


# TODO: mkdir from dirs list
def create_required_dirs(dirs: list, home: Path):
    try:
        # mkdir each dir in list
        for directory in dirs:
            if Path.exists(directory):
                continue
            else:
                os.makedirs(home / directory)
                debug_logger.debug('%s has been added!', directory)
    
    except OSError as ose:
        debug_logger.error('OSError in create_required_dirs: %s', ose)

    except Exception as e:
        debug_logger.error('Error in create_required_dirs: %s', e)


# TODO: mv dirs to Research based on criteria
def research_dir_funnel(home: Path):
    try:
        approved_home_dirs = get_non_hidden_dirs(home)
        for directory in approved_home_dirs:
            if directory == 'Research':
                continue

            for item in os.listdir(directory):
                has_git_file = Path.exists(home / directory / item /'.git')
                is_research = item.startswith('Learn') or item.startswith('Study') or item.startswith('Test')
                is_research = is_research and has_git_file
                if not is_research:
                    continue
                if is_research:
                    source_path = home / directory / item
                    destination_path = home / 'Research'
                    debug_logger.info('Source path in research_dir_funnel: %s', source_path)
                    debug_logger.info('Destination path in research_dir_funnel: %s', destination_path)
                    # TODO: test before moving anything
                    # moved_dir_path = shutil.move(source_path, destination_path)
                    # debug_logger.info(f'Directory was move to {moved_dir_path}')
    except OSError as ose:
        debug_logger.error('OSError in research_dir_funnel: %s', ose)
    
    except Exception as e:
        debug_logger.error('Error in research_dir_funnel: %s', e)


# TODO: mv dirs to College based on criteria
def college_dir_funnel(home: Path):
    try:
        approved_home_dirs = get_non_hidden_dirs(home)
        for directory in approved_home_dirs:
            if directory == 'College':
                continue
            
            # TODO: filter out hidden files/directories
            for item in os.listdir(directory):
                is_college = item.startswith('CS') 
                if not is_college:
                    continue
                if is_college:
                    source_path = home / directory / item
                    destination_path = home / 'College'
                    debug_logger.info('Source path in college_dir_funnel: %s', source_path)
                    debug_logger.info('Destination path in college_dir_funnel: %s', destination_path)
                    # TODO: test before moving anything
                    # moved_dir_path = shutil.move(source_path, destination_path)
                    # debug_logger.info(f'Directory was move to {moved_dir_path}')
    except OSError as ose:
        debug_logger.error('OSError in college_dir_funnel: %s', ose)
    
    except Exception as e:
        debug_logger.error('Error in college_dir_funnel: %s', e)



# TODO: mv dirs to Hackathon based on criteria
def hackathon_dir_funnel(home: Path):
    try:
        approved_home_dirs = get_non_hidden_dirs(home)
        for directory in approved_home_dirs:
            if directory == 'Hackathon':
                continue

            # TODO: filter out hidden files/directories
            for item in os.listdir(directory):
                has_git_file = Path.exists(home / directory / item /'.git')
                is_hackathon = item.startswith('Hackathon') and has_git_file
                if not is_hackathon:
                    continue
                if is_hackathon:
                    source_path = home / directory / item
                    destination_path = home / 'Hackathon'
                    debug_logger.info('Source path in hackathon_dir_funnel: %s', source_path)
                    debug_logger.info('Destination path in hackathon_dir_funnel: %s', destination_path)
                    # TODO: test before moving anything
                    # moved_dir_path = shutil.move(source_path, destination_path)
                    # debug_logger.info(f'Directory was move to {moved_dir_path}')
    except OSError as ose:
        debug_logger.error('OSError in hackthon_dir_funnel: %s', ose)
    
    except Exception as e:
        debug_logger.error('Error in hackathon_dir_funnel: %s', e)


# TODO: mv dirs to Projects based on criteria
def projects_dir_funnel(home: Path):
    try:
        approved_home_dirs = get_non_hidden_dirs(home)
        for directory in approved_home_dirs:
            if directory == 'Projects':
                continue
            if directory == 'Research':
                continue

            # TODO: filter out hidden files/directories
            for item in os.listdir(directory):
                has_git_file = Path.exists(home / directory / item /'.git')
                if not has_git_file:
                    continue
                if has_git_file:
                    source_path = home / directory / item
                    destination_path = home / 'Hackathon'
                    debug_logger.info('Source path in hackathon_dir_funnel: %s', source_path)
                    debug_logger.info('Destination path in hackathon_dir_funnel: %s', destination_path)
                    # TODO: test before moving anything
                    # moved_dir_path = shutil.move(source_path, destination_path)
                    # debug_logger.info(f'Directory was move to {moved_dir_path}')
    except OSError as ose:
        debug_logger.error('OSError in hackthon_dir_funnel: %s', ose)
    
    except Exception as e:
        debug_logger.error('Error in hackathon_dir_funnel: %s', e)


# TODO: mv files to Backups based on criteria
def backups_dir_funnel(home: Path):
    pass

# TODO: clean up Downloads dir based on criteria
def cleanup_downloads_dir():
    pass


def mv_doc_files_to_documents():
    pass


def mv_pic_files_to_pictures():
    pass


def del_zip_files():
    pass


if __name__ == "__main__":
    my_dirs = ['Projects', 'Hackathons', 'Documents', 'Desktop', 'Fonts', 'Templates',
                'Hacking', 'Powerhouse_Vault', 'Obsidian_Plugin_Sandbox', 'Pictures',
                'Music', 'Downloads', 'Arduino', 'anaconda3', 'Videos', 'Backups',
                'Research', 'College']

    home_path = Path.home()
    debug_logger.info(f'Home path created: {home_path}')
    

    #  create required dirs
    #create_required_dirs(my_dirs, home_path)

    # directory funnels
    #research_dir_funnel(test_path)
    #college_dir_funnel(test_path)
    #hackathon_dir_funnel(test_path)
    #projects_dir_funnel(test_path)

    # close debug log file
    debug_log_file.close()

