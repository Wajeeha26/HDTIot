import copy
import json

from django.http import JsonResponse

from HDTIoT.settings import JSON_RESPONSE, SUCCESS_CODES
from utilities.log_utils import log_exception

import logging

logger = logging.getLogger(__name__)

def make_response(response_code: int, message: str, data: any = None):
    """
    Makes response object
    :param response_code: response code
    :param message: response message
    :param data: response data
    """
    method_name = '[MAKE_RESPONSE]'
    extras = {"endpoint": f"{method_name}", "user": ""}
    try:
        response = copy.deepcopy(JSON_RESPONSE)
        if not response:
            return {"data": "No response data available"}

        response["status"] = "success" if response_code in SUCCESS_CODES else "failed"
        response["message"] = message or ""
        response["status_code"] = response_code
        response["data"] = data or {"data": "No response data available"}

        return response

    except Exception as e:
        log_exception(logger, extras)
        return {"data": "No response data available"}


def handle_api_exception(exception: any, status_code: int, message: str,
                         extras: object, logger_obj: object):
    """
    Helper function to handle logging and response for any api exception
    """
    log_exception(logger_obj, extras)

    # Construct response
    response = make_response(status_code, message)

    # Format log message
    logger_obj.info(f"{message}. Exception: {exception}. Returning Response: {json.dumps(response)}")

    # Update extras with response and status code
    extras.update({
        'response': json.dumps(response),
        'status_code': status_code
    })

    # Return JSON response
    return JsonResponse(response, status=status_code)


def api_success_response(status_code: int, message: str, data: object = None,
                         extras: object = None):
    """
    Helper function to return success response
    :param status_code: status code
    :param message: response message
    :param data: response data
    :param extras: logging extras
    """
    try:
        response = make_response(status_code, message, data)
        logger.info(f"Returning Response: {str(response)}")
        return JsonResponse(response, status=status_code)

    except Exception as e:
        log_exception(logger, extras)
        raise Exception(e)
