"""
Simple logging utility for NEXUS AI system.
"""

import logging
from datetime import datetime
from config import LOG_FILE, LOG_LEVEL

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

def log(agent_name: str, message: str, level: str = "INFO"):
    """
    Log a message.
    
    Args:
        agent_name: Name of agent or component
        message: Message to log
        level: Log level (INFO, WARNING, ERROR, DEBUG)
    """
    logger = logging.getLogger(agent_name)
    log_func = getattr(logger, level.lower(), logger.info)
    log_func(message)