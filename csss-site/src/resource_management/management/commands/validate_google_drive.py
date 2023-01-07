from django.core.management.base import BaseCommand

from csss.setup_logger import Loggers
from resource_management.views.resource_views import validate_google_drive

SERVICE_NAME = "validate_google_drive"


class Command(BaseCommand):
    help = "validates the access for the google drive"

    def handle(self, *args, **options):
        logger = Loggers.get_logger(logger_name=SERVICE_NAME)
        logger.info(options)
        logger.info("[resource_management/validate_access.py handle()] user has selected to validate the access "
                    "to google drive")
        validate_google_drive()
        Loggers.remove_logger(SERVICE_NAME)