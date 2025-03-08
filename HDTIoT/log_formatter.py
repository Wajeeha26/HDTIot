import json
import logging


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "asctime": self.formatTime(record, self.datefmt),
            "name": record.name,
            "levelname": record.levelname,
            "message": record.getMessage()
        }

        # Prepare the additional data for user and endpoint
        additional_info = ""
        if hasattr(record, 'endpoint') and record.endpoint:
            log_entry['endpoint'] = record.endpoint
            additional_info += f"{str(record.endpoint)} "

        if hasattr(record, 'user') and record.user:
            log_entry['user'] = record.user
            additional_info += f"{str(record.user)} "

        # If additional info exists, prepend it to the log message
        if additional_info:
            record.msg = f"{additional_info}{record.msg}"

        log_entry['message'] = record.getMessage()
        return json.dumps(log_entry)
