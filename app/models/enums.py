from enum import Enum

class DocumentStatus(str, Enum):
    DRAFT = "DRAFT"
    PROCESSING = "PROCESSING"
    READY = "READY"
    FAILED = "FAILED"