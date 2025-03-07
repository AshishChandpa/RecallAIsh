import logging
import queue
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from logging.handlers import QueueHandler, QueueListener
from typing import Any, Dict, List

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("web_scraper")
log_queue = queue.Queue()

queue_handler = QueueHandler(log_queue)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        record.auditAt = str(datetime.fromtimestamp(record.created, timezone.utc))

        colors = {
            "levelname": COLORS.get(record.levelname, COLORS["RESET"]),
            "auditAt": COLORS.get("AUDIT_AT", COLORS["RESET"]),
        }
        colored_attrs = {
            attr: f"{colors[attr]}{getattr(record, attr)}{COLORS['RESET']}"
            for attr in colors
        }

        formatted_record = super().format(record)
        for attr, colored_value in colored_attrs.items():
            formatted_record = formatted_record.replace(
                getattr(record, attr), colored_value
            )
        return formatted_record


COLORS = {
    "AUDIT_AT": "\033[36m",
    "DEBUG": "\033[94m",
    "INFO": "\033[1;32m",
    "WARNING": "\033[33m",
    "ERROR": "\033[1;31m",
    "CRITICAL": "\033[4;1;31m",
    "REQUEST_INIT": "\033[1;96m",
    "FUNCTION_INVOKE": "\033[35m",
    "FUNCTION_RETURN": "\033[32m",
    "REQUEST_END": "\033[1;96m",
    "QUALNAME": "\033[94m",
    "RESET": "\033[0;0;37m",
}

console_format = ColoredFormatter(
    fmt=" ".join(["%(auditAt)s", "%(name)s", "%(levelname)s ", "message: %(message)s"])
)
console_handler.setFormatter(console_format)

logger.addHandler(queue_handler)

listener = QueueListener(log_queue, console_handler, respect_handler_level=True)

listener.start()


class BaseScraper(ABC):
    @abstractmethod
    def extract_data(self, url: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_internal_links(self, url: str) -> List[str]:
        pass

    def safe_get_attribute(self, element, attribute, default=""):
        """Safely get attribute from element"""
        try:
            if element is None:
                return default
            value = element.get_attribute(attribute)
            return value if value is not None else default
        except:
            return default
