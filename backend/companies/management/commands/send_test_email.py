from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Send a test email using the configured Django email backend.'

    def add_arguments(self, parser):
        parser.add_argument('recipient', help='Recipient email address')

    def handle(self, *args, **options):
        recipient = options['recipient']
        if not settings.DEFAULT_FROM_EMAIL:
            raise CommandError('DEFAULT_FROM_EMAIL is not configured.')

        sent = send_mail(
            subject='WHIT test email',
            message='This is a test email from WhoIsHiringInTech.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )

        if sent != 1:
            raise CommandError('Django did not report a successful send.')

        self.stdout.write(self.style.SUCCESS(f'Test email sent to {recipient}'))
