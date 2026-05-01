import logging
import os
import sys

def setup_logging(log_file="bot.log"):
    """Configures application-wide logging."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # File handler to log all API requests and errors
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # Note: We intentionally avoid adding a StreamHandler (console output) here 
    # because we are using the 'rich' library in the CLI for user-friendly output.
    # We want the raw API data in the log file, but clean UI on the screen.
