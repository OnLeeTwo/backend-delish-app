from base import db

class StatusEnum(db.Enum):
    pending = 1
    completed = 2
    cancelled = 3