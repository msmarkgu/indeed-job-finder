import json
import logging
import os
import sys

class CommonUtils:

    @staticmethod
    def init_logger(log_level, logger_name, log_file=None):
        log_format = "%(asctime)s [%(levelname)s] %(name)s.%(funcName)s(): %(message)s"
        date_format = "%Y-%m-%d %H:%M:%S"

        log_formatter = logging.Formatter(fmt=log_format, datefmt=date_format)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(log_formatter)

        logger = logging.getLogger(logger_name)  # name the logger using class name
        logger.setLevel(log_level)
        logger.addHandler(console_handler)

        if log_file:
            if os.path.exists(log_file):
                os.remove(log_file)
            else:
                folder_path = os.path.dirname(log_file)
                if not os.path.exists:
                    os.makedirs(folder_path)
                with open(log_file, 'w') as fp:
                    fp.write("")
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(log_formatter)
            logger.addHandler(file_handler)

        return logger

    @staticmethod
    def save_as_json_to_file(data_obj, file_path):
        """
        save the given data object to the specified file, using utf-8 encoding and handle non-utf8 encodable chars.
        """
        with open(file_path, mode="w", encoding='utf-8') as fp:
            fp.write(CommonUtils.get_json_string(data_obj))
            fp.write("\n")

    @staticmethod
    def get_json_string(data_obj):
        json_str = json.dumps(data_obj, indent=2, ensure_ascii=False)  # try decode non-ascii chars
        bytes = json_str.encode(encoding="utf-8", errors="replace")    # if the char cannot encode to utf-8, try replace it
        utf8_str = bytes.decode(encoding="utf-8")
        return utf8_str
