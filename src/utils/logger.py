import logging
import sys
from pathlib import Path
from typing import Optional
from rich.logging import RichHandler
from rich.console import Console

console = Console()

def setup_logger(
    name: str,
    log_level: str = "INFO",
    log_file: Optional[str] = None
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    if logger.handlers:
        return logger
    
    logger.handlers.clear()
    
    rich_handler = RichHandler(
        console=console,
        rich_tracebacks=True,
        tracebacks_show_locals=True,
        markup=True
    )
    rich_handler.setLevel(getattr(logging, log_level.upper()))
    
    formatter = logging.Formatter(
        "%(message)s",
        datefmt="[%X]"
    )
    rich_handler.setFormatter(formatter)
    logger.addHandler(rich_handler)
    
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, log_level.upper()))
        
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger
