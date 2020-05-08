"""
Scheduled Jobs: scheduled_jobs.py
=================================
Holds a class to hold scheduling operations.
"""

from flask import current_app
from utils.logger import AppLogger
from pymongo import MongoClient
import time
import threading
from config import environment


def ping_db():
    """
        Send ping command to the system database to check health.
    """
    conn = MongoClient(host=environment.DB_HOST)
    while True:
        if not conn[environment.DB_NAME].command('ping'):
            logger: AppLogger = current_app.__getattribute__('app_logger')
            logger.log_error('Database Connection Error')
        time.sleep(10)


class ScheduledJobs:
    """
        Static Class intended to hold all Scheduled operations. Operations run as a background thread.
    """
    @staticmethod
    def job_ping_db():
        """
            Static method that runs the function "ping_db" as a scheduled job.
        """
        t = threading.Thread(name='ping_db', target=ping_db)
        t.daemon = True
        t.start()
