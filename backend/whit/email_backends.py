"""Email backends for the WHIT project."""

import base64
import json
import mimetypes
from email.utils import parseaddr
from html import escape
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import EmailMultiAlternatives


class BrevoEmailBackend(BaseEmailBackend):
    """Send Django email messages through Brevo's transactional email API."""

    def send_messages(self, email_messages):
        if not email_messages:
            return 0

        api_key = getattr(settings, 'BREVO_API_KEY', '')
        if not api_key:
            if self.fail_silently:
                return 0
            raise RuntimeError('BREVO_API_KEY is not configured.')

        sent_count = 0
        for message in email_messages:
            try:
                self._send_message(message, api_key)
                sent_count += 1
            except Exception:
                if not self.fail_silently:
                    raise
        return sent_count

    def _send_message(self, message, api_key):
        payload = self._build_payload(message)
        request = Request(
            getattr(settings, 'BREVO_API_URL', 'https://api.brevo.com/v3/smtp/email'),
            data=json.dumps(payload).encode('utf-8'),
            headers={
                'accept': 'application/json',
                'api-key': api_key,
                'content-type': 'application/json',
            },
            method='POST',
        )

        try:
            with urlopen(request, timeout=getattr(settings, 'BREVO_API_TIMEOUT', 15)) as response:
                response.read()
        except HTTPError as exc:
            detail = exc.read().decode('utf-8', errors='replace')
            raise RuntimeError(f'Brevo email API returned HTTP {exc.code}: {detail}') from exc
        except URLError as exc:
            raise RuntimeError(f'Unable to reach Brevo email API: {exc.reason}') from exc

    def _build_payload(self, message):
        sender = self._format_address(message.from_email or settings.DEFAULT_FROM_EMAIL)
        payload = {
            'sender': sender,
            'to': [self._format_address(address) for address in message.to],
            'subject': message.subject,
        }

        if message.cc:
            payload['cc'] = [self._format_address(address) for address in message.cc]
        if message.bcc:
            payload['bcc'] = [self._format_address(address) for address in message.bcc]
        if message.reply_to:
            payload['replyTo'] = self._format_address(message.reply_to[0])

        text_content, html_content = self._message_content(message)
        if text_content:
            payload['textContent'] = text_content
        if html_content:
            payload['htmlContent'] = html_content

        if not payload.get('htmlContent') and payload.get('textContent'):
            payload['htmlContent'] = f'<pre>{escape(payload["textContent"])}</pre>'

        attachments = self._attachments(message)
        if attachments:
            payload['attachment'] = attachments

        return payload

    def _message_content(self, message):
        text_content = message.body or ''
        html_content = message.body if getattr(message, 'content_subtype', None) == 'html' else ''

        if isinstance(message, EmailMultiAlternatives):
            for content, mimetype in message.alternatives:
                if mimetype == 'text/html':
                    html_content = content
                elif mimetype == 'text/plain' and not text_content:
                    text_content = content

        return text_content, html_content

    def _attachments(self, message):
        attachments = []
        for attachment in message.attachments:
            if hasattr(attachment, 'read'):
                content = attachment.read()
                filename = getattr(attachment, 'name', 'attachment')
                content_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
            else:
                filename, content, content_type = attachment

            if isinstance(content, str):
                content = content.encode('utf-8')

            attachments.append({
                'name': filename,
                'content': base64.b64encode(content).decode('ascii'),
                'contentType': content_type or 'application/octet-stream',
            })
        return attachments

    def _format_address(self, address):
        name, email = parseaddr(address)
        formatted = {'email': email or address}
        if name:
            formatted['name'] = name
        return formatted
