import time
import logging
import pandas as pd
import typing as tp
import constants as c
from threading import Lock
from datetime import datetime, timezone
from dataclasses import dataclass

# logging.StreamHandler()
# ch.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s:%(thread)d - %(name)s - %(levelname)s - %(message)s')
# ch.setFormatter(formatter
logger = logging.getLogger('SQLLogger')
logger.setLevel(logging.INFO)
logging.basicConfig(
        filename=c.LOGGING_PATH,
        filemode='a+',
        format=c.LOGGING_FORMAT
        )


@dataclass
class DataFeed:
    ''' The base-level implementation for all data feeds, which should inherit from DataFeed and implement the get_data_point method as required.
    '''

    #NOTE: all feeds must define these class-level attributes
    NAME: str
    ID: int
    HEARTBEAT: int              #in seconds
    START_TIME: datetime
    ACTIVE: bool = False
    COUNT: int = 0              #number of data points served since starting


    @classmethod
    def get_data_dir(cls):
        return c.DATA_PATH / (cls.NAME + c.DATA_EXT)


    @classmethod
    def run(cls):

        while cls.ACTIVE:
            dp = cls.get_data_point(cls)
            logging.info('\nNext data point for {cls.NAME}: {dp}\n')
            cls.save_data_point(dp)
            cls.COUNT += 1
            time.sleep(cls.HEARTBEAT)


    @classmethod
    def get_data_point(cls):
        raise NotImplementedError


    @classmethod
    def save_data_point(cls, dp):
        with Lock():
            with open(cls.get_data_dir(), 'a+') as datafile:
                datafile.write(cls.format_data(dp))


    @staticmethod
    def format_data(dp):
        timenow =  datetime.now(timezone.utc)
        strtime = timenow.strftime(c.DATEFORMAT)
        return f'{strtime}, {dp}, \n'
