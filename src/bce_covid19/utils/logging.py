import logging
import os


def create_logging_file(logger_file_name: str, save_path: str, print_log: bool = True) -> None:
    """
    Function to create a logging file in the `save_path` named `logger_file_name.log`

    (No unittest)

    Args:
        save_path: the path where the logger will be saved.
        logger_file_name: the name of the file, without the .log suffix.
        print_log: do you to print the log to the screen as well?
    """
    logging.basicConfig(filename=os.path.join(save_path, f"{logger_file_name}.log"), level=logging.INFO,
                        format='%(asctime)s :: %(levelname)s -> %(message)s', filemode='a')
    if print_log:
        logging.getLogger().addHandler(logging.StreamHandler())
