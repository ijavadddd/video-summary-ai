from enum import Enum


class MessageStatus(Enum):
    INFO = "text-sky-700 bg-sky-300 border-sky-400"
    SUCCESS = "text-green-700 bg-green-300 border-green-400"
    WARNING = "bg-orange-100 text-orange-600 "
    ERROR = "text-red-700 bg-red-300 border-red-400"
