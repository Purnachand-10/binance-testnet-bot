import logging
def setup_logging(log_file="bot.log"):
    """Configure application-wide logging."""

    logger = logging.getLogger()

    # Prevent duplicate handlers (important when re-running)
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    # File handler (main requirement)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    # Optional: Enable console logging (for debugging if needed)
    # Commented out by default (clean CLI output)
    """
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    """

    return logger
