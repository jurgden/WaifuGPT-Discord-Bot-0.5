import logging
# import os

logger = logging.getLogger("main_logger")
logger.setLevel(logging.DEBUG)
file_logger = logging.FileHandler('file.log')
file_logger.setLevel(logging.DEBUG)
# stream_logger = logging.StreamHandler(os.sys)
# stream_logger.setLevel(logging.WARNING)

filematter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
# streamatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

file_logger.setFormatter(filematter)
# stream_logger.setFormatter(streamatter)


# add the handlers to the logger
logger.addHandler(file_logger)
# logger.addHandler(stream_logger)

