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
        Retrieves the database connection instance from the current_app object of Flask and sends a ping command for
        database health check verification.
    """

    while True:
        # conn = MongoClient(host=environment.DB_HOST)
        conn = MongoClient('mongodb://localhost:27017')
        if not conn['IReNEdb'].command('ping'):
            logger: AppLogger = AppLogger()
            logger.log_error('Database Connection Error')
        conn.close()
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
