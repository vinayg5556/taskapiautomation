import inspect
import logging
import time


def custom_logger():
    logName = inspect.stack()[1][3]  # used to get the class/methode name from where logger methode called
    logger = logging.getLogger(logName)  # creating logging object to pass the logname
    logger.setLevel(logging.DEBUG)  # set log level
    fileHandler = logging.FileHandler('Logs/' + time.strftime("%d-%m-%y") + '.text', mode='a')  # create file handler to save the file
    fileHandler.setLevel(logging.DEBUG)  # set log level to file handler
    # create logging formate
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s : %(message)s",
                                  datefmt='%d/%m/%y %I:%M:%S %p %A')
    fileHandler.setFormatter(formatter)  # set the formater to filehandler
    logger.addHandler(fileHandler)  # add file handler to logging

    return logger  # retun logging object
