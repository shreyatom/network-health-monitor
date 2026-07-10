"""logger.py
Sets up logging for the entire project.
All scripts import from here.
"""

import logging
import os
from datetime import datetime

# Create logs/reports folder if it doesn't exist
os.makedirs('logs',    exist_ok=True)
os.makedirs('reports', exist_ok=True)

# daily log file
log_filename = f"logs/monitor_{datetime.now().strftime('%Y%m%d')}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',  # timestamp | level | msg
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(log_filename), # file
        logging.StreamHandler()  #console
    ]
)

# Create logger object — import this in other files
logger = logging.getLogger('NetworkMonitor')