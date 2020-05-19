"""
scheduled_jobs.py
=================
Author: Roberto Guzmán <roberto.guzman3@upr.edu>
Holds a class to hold scheduling operations.
"""

from flask import current_app
from utils.logger import AppLogger
from mongoengine import connection
import time
import threading
from config import environment


def ping_db():
    """
        Retrieves the database connection instance from the current_app object of Flask and sends a ping command for
        database health check verification.
    """

    while True:
        if not connection.get_db().command('ping'):
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
