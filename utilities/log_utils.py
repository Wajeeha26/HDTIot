import json
import sys
import traceback


def log_exception(logger: object = None, extras: object = None) -> str:
    """
    Log the exception traceback
    :param logger: logger object
    :param extras: extras
    :returns error: error string
    """
    exec_type, exec_value, exec_traceback = sys.exc_info()
    logger.error(repr(traceback.format_exception(exec_type, exec_value, exec_traceback)), extra=extras)
    return str(repr(traceback.format_exception(exec_type, exec_value, exec_traceback)))

def log_request(request, logger, api_name):
    extras = {"endpoint": api_name, "user": f"{request.user.email}:{request.user.id}",
              "http_request": json.dumps(request.body)}

    logger.info(f'Request.headers: {request.headers}, Request.body: {request.body}')

    return extras
