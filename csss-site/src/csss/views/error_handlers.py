from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin
import traceback

from csss.setup_logger import Loggers
from csss.views.context_creation.create_main_context import create_main_context
from csss.views.exceptions import InvalidPrivilege, NoAuthenticationMethod, CASAuthenticationMethod, \
    UnProcessedNotDetected
from csss.views.views import ERROR_MESSAGES_KEY


class HandleBusinessExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        logger = Loggers.get_logger()
        if isinstance(exception, InvalidPrivilege):
            return exception.render
        if isinstance(exception, NoAuthenticationMethod):
            return exception.render
        if isinstance(exception, CASAuthenticationMethod):
            return exception.render
        if isinstance(exception, UnProcessedNotDetected):
            return exception.render
        context = create_main_context(request, 'index')
        logger.exception(traceback.format_exc())
        context[ERROR_MESSAGES_KEY] = [f"Encountered an unexpected exception of: {exception}"]
        return render(request, 'csss/error_htmls/unknown_error.html', context)
