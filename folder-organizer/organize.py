import os
import re
import shutil
import uuid
#directory where script was invoked
DIRECTORY = os.getcwd()
BANNED_FILE_NAMES = ["organize.py"]
OPERATION_COUNT = 0

def main():
    LOGGER = Log(OPERATION_COUNT)
    try:
        files = list_all_files()
        move_file_by_extension(files, LOGGER)
        print("\n")
        print(f"| SUCCESS FINISHED |: operations {LOGGER.operations}")
    except Exception as e:
        print(str(e))
        print("| ERROR FINISHED |: An error has occurred while trying to organized the folder, try again.")

def move_file_by_extension(files, LOGGER):
    for i in files:
        extension = get_file_extension(i)
        if not extension:
            continue
        folder_for_extension = create_folder_for_extension(extension)
        move_file_to_folder(i, folder_for_extension, LOGGER)


def list_all_files():
    file_list = [f for f in os.listdir(DIRECTORY) if os.path.isfile(os.path.join(DIRECTORY, f)) and f not in BANNED_FILE_NAMES ]
    return file_list

def create_folder_for_extension(extension):
    folders = list_all_folders()
    tokenized_extension = tokenize_extension(extension)
    directory = DIRECTORY + "/" + tokenized_extension
    if not os.path.exists(directory):
        os.makedirs(directory)
        return directory
    else:
        return directory

def move_file_to_folder(file_name, folder_path, LOGGER):
    file_path = DIRECTORY + "/" + file_name
    try:
        shutil.move(file_path, folder_path)
    except Exception as e:
        exception_message = str(e)
        if("already exists" in exception_message):
            print(f"WARNING: file {file_path} already exists in directory")
            file_path = ErrorHandler.handle_already_exists_error(file_path, folder_path)
            if not file_path:
                raise
            else:
                pass

    if os.path.exists(os.path.join(folder_path, os.path.basename(file_name))):
        LOGGER.increase_operation_count()
        print(f"SUCCESS: File organization finished for '{os.path.basename(file_name)}' inserted into '{folder_path}'.")
    else:
        print(f"ERROR: File organization failed for {file_path}" )



def list_all_folders():
    folder_list = [f for f in os.listdir(DIRECTORY) if os.path.isdir(os.path.join(DIRECTORY, f))]
    return folder_list

def tokenize_extension(file_extension):
    return file_extension.upper()

def get_file_extension(file_name):
    extension = re.search(r'\.([^.]+)$', file_name)
    if not extension:
        return None

    file_extension = extension.group(1)
    return file_extension


class ErrorHandler:
    @staticmethod
    def handle_already_exists_error(file_path, folder_path):
        try: 
            unique_hash = uuid.uuid4()
            file_name_without_extension = os.path.splitext(os.path.basename(file_path))[0]
            new_file_name = file_name_without_extension + "-" + str(unique_hash) + '.pdf'
            new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)
            os.rename(file_path, new_file_path)
            file_path = new_file_path
            shutil.move(file_path, folder_path)
        except Exception as e:
            print("ERROR: Exception happened inside already exists error handler, aborting...")
            print(str(e))
            return None

        return file_path

class Log:
    def __init__(self, operations):
        self.operations = operations

    def increase_operation_count(self):
        self.operations = self.operations + 1
        


main()



