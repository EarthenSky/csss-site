import time
from email.utils import parseaddr

from django.core.management.base import BaseCommand
from django_mailbox.models import Mailbox
from django_mailbox.models import Message

from about.models import UnProcessedOfficer, Term
from announcements.models import Announcement
from announcements.views.commands.process_announcements.add_sortable_date_to_email import add_sortable_date_to_email
from announcements.views.commands.process_announcements.get_officer_term_mapping import get_officer_term_mapping
from csss.models import CronJob, CronJobRunStat
from csss.setup_logger import Loggers
from csss.views.send_email import send_email
from csss.views_helper import get_term_number_for_specified_year_and_month

SERVICE_NAME = "process_announcements"


class Command(BaseCommand):
    help = "process the latest new emails and manual announcements and determines which to display"

    def add_arguments(self, parser):
        parser.add_argument(
            '--poll_email',
            action='store_true',
            default=False,
            help="pull the latest emails from gmail"
        )

    def handle(self, *args, **options):
        time1 = time.perf_counter()
        logger = Loggers.get_logger(logger_name=SERVICE_NAME)
        logger.info(options)
        there_are_no_unprocessed_officers = len(UnProcessedOfficer.objects.all()) == 0
        if options['poll_email']:
            # temporarily reverting to copying the code over instead of using it directly cause the
            #  logging.basicConfig(level=logging.INFO)  line clashes with my logger
            # will update once https://github.com/coddingtonbear/django-mailbox/issues/262 is resolved
            # from django_mailbox.management.commands.getmail import Command as GetMailCommand
            # GetMailCommand().handle()
            mailboxes = Mailbox.active_mailboxes.all()
            if args:
                mailboxes = mailboxes.filter(
                    name=' '.join(args)
                )
            for mailbox in mailboxes:
                logger.info(
                    'Gathering messages for %s',
                    mailbox.name
                )
                messages = mailbox.get_new_mail()
                for message in messages:
                    logger.info(
                        'Received %s (from %s)',
                        message.subject,
                        message.from_address
                    )

        messages = []
        messages.extend(
            [add_sortable_date_to_email(email) for email in
             Message.objects.all().filter(visibility_indicator__isnull=True)]
        )
        messages.sort(key=lambda x: x.sortable_date, reverse=False)
        officer_mapping = get_officer_term_mapping()
        emails_not_displayed = []
        for message in messages:
            announcement_datetime = message.sortable_date
            term_number = get_term_number_for_specified_year_and_month(
                announcement_datetime.month,
                announcement_datetime.year
            )
            if f"{term_number}" not in officer_mapping:
                logger.info("[process_announcements handle()] announcement with date "
                            f"{announcement_datetime} does not map to a term")
                continue
            term = Term.objects.all().filter(term_number=term_number)
            if len(term) == 0:
                logger.info("[process_announcements handle()] could not find a valid term "
                            f"for term_number {term_number}")
                continue
            term = term[0]
            if hasattr(message, 'mailbox'):
                officer_emails = officer_mapping[f"{term_number}"]
                logger.info(f"[process_announcements handle()] acquired {len(officer_emails)} "
                            f"officers for date {announcement_datetime}")

                if len(parseaddr(message.from_header)) > 0:
                    author_name = parseaddr(message.from_header)[0]
                    author_email = parseaddr(message.from_header)[1]
                    valid_email = (author_email in officer_emails)
                    if valid_email or (not valid_email and there_are_no_unprocessed_officers):
                        if not valid_email:
                            emails_not_displayed.append(f"email from [{author_email}]")
                        Announcement(term=term, email=message, date=announcement_datetime,
                                     display=valid_email, author=author_name).save()
                        logger.info("[process_announcements handle()] saved email from"
                                    f" {author_name} with email {author_email} with date {announcement_datetime} "
                                    f"for term {term}. Will {'not ' if valid_email is False else ''}display email")
                else:
                    emails_not_displayed.append(f"Unknown Email with subject [{message.subject}]")
                    Announcement(term=term, email=message, date=announcement_datetime,
                                 display=False).save()
                    logger.info("[process_announcements handle()] unable to determine sender of email "
                                f"with date {announcement_datetime} "
                                f"for term {term}. Will not display email")
            else:
                Announcement(term=term, manual_announcement=message, date=announcement_datetime,
                             display=True, author=message.author).save()
                logger.info("[process_announcements handle()] saved post from"
                            f" {message.author} with date {announcement_datetime} "
                            f"for term {term}")
        if len(emails_not_displayed) > 0:
            body = "<br>".join(emails_not_displayed)
            send_email("CSSS-Website emails not displayed", body, "csss-sysadmin@sfu.ca", "jace")
        time2 = time.perf_counter()
        total_seconds = time2 - time1
        cron_job = CronJob.objects.get(job_name=SERVICE_NAME)
        number_of_stats = CronJobRunStat.objects.all().filter(job=cron_job)
        if len(number_of_stats) == 10:
            first = number_of_stats.order_by('id').first()
            if first is not None:
                first.delete()
        CronJobRunStat(job=cron_job, run_time_in_seconds=total_seconds).save()
        Loggers.remove_logger(SERVICE_NAME)
