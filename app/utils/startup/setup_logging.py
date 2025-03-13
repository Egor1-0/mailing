import logging
import os
from datetime import datetime
from pathlib import Path

from pytz import timezone


def setup_logging():
    file_log = logging.FileHandler(os.path.join(Path(__file__).resolve().parents[3], 'logs', 'logs.log'),
                                   mode='a')
    file_log.setLevel(logging.ERROR)

    console_out = logging.StreamHandler()
    console_out.setLevel(logging.INFO)

    def timetz(*args):
        tz = timezone('Europe/Moscow')
        return datetime.now(tz).timetuple()


    logging.Formatter.converter = timetz

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(filename)s %(message)s",
                        handlers=[console_out, file_log])
    logging.info('startup logging')