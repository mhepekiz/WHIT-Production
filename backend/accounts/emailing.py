"""Helpers for account transactional emails."""

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.template import Context, Template
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .models import EmailTemplate


SITE_NAME = 'WhoIsHiringInTech'

DEFAULT_TEMPLATES = {
    EmailTemplate.ACCOUNT_CREATED: {
        'name': 'New account creation',
        'subject': 'Welcome to WhoIsHiringInTech',
        'html_body': (
            '<p>Hi {{ first_name|default:"there" }},</p>'
            '<p>Your WhoIsHiringInTech account has been created.</p>'
            '<p>Please verify your email before signing in.</p>'
        ),
        'text_body': 'Hi {{ first_name|default:"there" }}, your WhoIsHiringInTech account has been created. Please verify your email before signing in.',
    },
    EmailTemplate.EMAIL_VERIFICATION: {
        'name': 'Verify email',
        'subject': 'Verify your WhoIsHiringInTech email',
        'html_body': (
            '<p>Hi {{ first_name|default:"there" }},</p>'
            '<p>Please verify your email address to activate your account.</p>'
            '<p><a href="{{ verification_url }}">Verify email address</a></p>'
        ),
        'text_body': 'Verify your email address: {{ verification_url }}',
    },
    EmailTemplate.PASSWORD_RESET: {
        'name': 'Password reset',
        'subject': 'Reset your WhoIsHiringInTech password',
        'html_body': (
            '<p>Hi {{ first_name|default:"there" }},</p>'
            '<p>Use this secure link to reset your password.</p>'
            '<p><a href="{{ password_reset_url }}">Reset password</a></p>'
            '<p>If you did not request this, you can ignore this email.</p>'
        ),
        'text_body': 'Reset your password: {{ password_reset_url }}',
    },
}


def frontend_url(path):
    base_url = getattr(settings, 'FRONTEND_BASE_URL', '').rstrip('/')
    if not base_url:
        base_url = 'https://staging.whoishiringintech.com'
    return f'{base_url}{path}'


def account_uid_and_token(user):
    return (
        urlsafe_base64_encode(force_bytes(user.pk)),
        default_token_generator.make_token(user),
    )


def verification_url(user):
    uid, token = account_uid_and_token(user)
    return frontend_url(f'/verify-email/{uid}/{token}')


def password_reset_url(user):
    uid, token = account_uid_and_token(user)
    return frontend_url(f'/password-reset/{uid}/{token}')


def send_account_email(template_key, user, extra_context=None):
    template = get_email_template(template_key)
    if not template or not template.is_active or not user.email:
        return 0

    context = {
        'user': user,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'site_name': SITE_NAME,
        'login_url': frontend_url('/login'),
        'recruiter_login_url': frontend_url('/recruiter/login'),
        'verification_url': verification_url(user),
        'password_reset_url': password_reset_url(user),
    }
    if extra_context:
        context.update(extra_context)

    subject = render_template_string(template.subject, context).strip()
    html_body = render_template_string(template.html_body, context)
    text_body = render_template_string(template.text_body, context) if template.text_body else ''

    message = EmailMultiAlternatives(
        subject=subject,
        body=text_body or html_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    message.attach_alternative(html_body, 'text/html')
    return message.send(fail_silently=False)


def get_email_template(template_key):
    defaults = DEFAULT_TEMPLATES.get(template_key)
    if not defaults:
        return None
    template, _ = EmailTemplate.objects.get_or_create(
        key=template_key,
        defaults={
            'name': defaults['name'],
            'subject': defaults['subject'],
            'html_body': defaults['html_body'],
            'text_body': defaults['text_body'],
        },
    )
    return template


def render_template_string(value, context):
    return Template(value).render(Context(context))
