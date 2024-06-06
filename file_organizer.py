import os
import shutil
import logging
from pathlib import Path

my_dirs = ['Projects', 'Hackathons', 'Documents', 'Desktop', 'Fonts', 'Templates',
             'Hacking', 'Powerhouse_Vault', 'Obsidian_Plugin_Sandbox', 'Pictures',
             'Music', 'Downloads', 'Arduino', 'anaconda3', 'Videos', 'Backups',
             'Research', 'College']

home_path = Path.home()

logging.basicConfig(
    filename='logging.log', level=logging.DEBUG,  
    format=' %(asctime) - %(levelname) - %(message)'
)

# get list of non-hidden directories
def get_non_hidden_dirs(directory=None):
    if directory is None:
        return [], []
    
    approved_items = [item for item in os.listdir(directory) if not item.startswith(".")]
    approved_dirs = [item for item in approved_items if os.path.isdir(Path(directory, item))]
    return approved_dirs


# TODO: mkdir from dirs list
def create_required_dirs(dirs, home):
    try:
        # mkdir each dir in list
        for directory in dirs:
            if Path.exists(directory):
                continue
            else:
                os.makedirs(home / directory)
                logging.debug(f'{directory} has been added!')
    
    except OSError as ose:
        logging.error(f'OSError in create_required_dirs: {ose}')

    except Exception as e:
        logging.error(f'Error in create_required_dirs: {e}')


# TODO: mv dirs to Research based on criteria
def research_dir_funnel(home):
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
                    logging.info(f'Source path in research_dir_funnel: {source_path}')
                    logging.info(f'Destination path in research_dir_funnel: {destination_path}')
                    # TODO: test before moving anything
                    # moved_dir_path = shutil.move(source_path, destination_path)
                    # logging.info(f'Directory was move to {moved_dir_path}')
    except OSError as ose:
        logging.error(f'OSError in research_dir_funnel: {ose}')
    
    except Exception as e:
        logging.error(f'Error in research_dir_funnel: {e}')


# TODO: mv dirs to College based on criteria
def college_dir_funnel(home):
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
                    logging.info(f'Source path in college_dir_funnel: {source_path}')
                    logging.info(f'Destination path in college_dir_funnel: {destination_path}')
                    # TODO: test before moving anything
                    # moved_dir_path = shutil.move(source_path, destination_path)
                    # logging.info(f'Directory was move to {moved_dir_path}')
    except OSError as ose:
        logging.error(f'OSError in college_dir_funnel: {ose}')
    
    except Exception as e:
        logging.error(f'Error in college_dir_funnel: {e}')



# TODO: mv dirs to Hackathon based on criteria
def hackathon_dir_funnel(home):
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
                    logging.info(f'Source path in hackathon_dir_funnel: {source_path}')
                    logging.info(f'Destination path in hackathon_dir_funnel: {destination_path}')
                    # TODO: test before moving anything
                    # moved_dir_path = shutil.move(source_path, destination_path)
                    # logging.info(f'Directory was move to {moved_dir_path}')
    except OSError as ose:
        logging.error(f'OSError in hackthon_dir_funnel: {ose}')
    
    except Exception as e:
        logging.error(f'Error in hackathon_dir_funnel: {e}')


# TODO: mv dirs to Projects based on criteria
def projects_dirs_funnel(home):
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
                    logging.info(f'Source path in hackathon_dir_funnel: {source_path}')
                    logging.info(f'Destination path in hackathon_dir_funnel: {destination_path}')
                    # TODO: test before moving anything
                    # moved_dir_path = shutil.move(source_path, destination_path)
                    # logging.info(f'Directory was move to {moved_dir_path}')
    except OSError as ose:
        logging.error(f'OSError in hackthon_dir_funnel: {ose}')
    
    except Exception as e:
        logging.error(f'Error in hackathon_dir_funnel: {e}')


# TODO: mv files to Backups based on criteria
def backups_dir_funnel():
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