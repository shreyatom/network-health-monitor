# logger.py
# Sets up logging for the entire project.
# All scripts import from here.

import logging
import os
from datetime import datetime

# Create logs folder if it doesn't exist
os.makedirs('logs',    exist_ok=True)
os.makedirs('reports', exist_ok=True)

# Log filename with today's date
log_filename = f"logs/monitor_{datetime.now().strftime('%Y%m%d')}.log"

# Configure logging
logging.basicConfig(
    level=logging.INFO,

    # Log format: timestamp | level | message
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',

    handlers=[
        # Save logs to file
        logging.FileHandler(log_filename),

        # Also print to terminal
        logging.StreamHandler()
    ]
)

# Create logger object — import this in other files
logger = logging.getLogger('NetworkMonitor')