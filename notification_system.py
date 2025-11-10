"""
Notification System for Motion Detector
Supports email, desktop notifications, and webhooks
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from datetime import datetime, timedelta
import json
from pathlib import Path
from typing import Optional
import requests


class NotificationSystem:
    """
    Handles various types of notifications for motion detection events
    """

    def __init__(self, config: dict = None):
        """
        Initialize notification system

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.last_notification_time = None
        self.cooldown = self.config.get('cooldown', 60)  # seconds

    def can_send_notification(self) -> bool:
        """
        Check if enough time has passed since last notification

        Returns:
            bool: True if notification can be sent
        """
        if self.last_notification_time is None:
            return True

        elapsed = (datetime.now() - self.last_notification_time).total_seconds()
        return elapsed >= self.cooldown

    def send_email_notification(self, subject: str, body: str, image_path: Optional[str] = None) -> bool:
        """
        Send email notification

        Args:
            subject: Email subject
            body: Email body text
            image_path: Optional path to image attachment

        Returns:
            bool: Success status
        """
        if not self.can_send_notification():
            return False

        try:
            email_config = self.config.get('email', {})

            if not all([
                email_config.get('smtp_server'),
                email_config.get('smtp_port'),
                email_config.get('sender'),
                email_config.get('password'),
                email_config.get('recipient')
            ]):
                print("Email configuration incomplete")
                return False

            # Create message
            msg = MIMEMultipart()
            msg['From'] = email_config['sender']
            msg['To'] = email_config['recipient']
            msg['Subject'] = subject

            # Add body
            msg.attach(MIMEText(body, 'plain'))

            # Add image if provided
            if image_path and Path(image_path).exists():
                with open(image_path, 'rb') as f:
                    img = MIMEImage(f.read())
                    img.add_header('Content-Disposition', 'attachment',
                                 filename=Path(image_path).name)
                    msg.attach(img)

            # Send email
            with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port']) as server:
                server.starttls()
                server.login(email_config['sender'], email_config['password'])
                server.send_message(msg)

            self.last_notification_time = datetime.now()
            return True

        except Exception as e:
            print(f"Error sending email: {e}")
            return False

    def send_desktop_notification(self, title: str, message: str) -> bool:
        """
        Send desktop notification

        Args:
            title: Notification title
            message: Notification message

        Returns:
            bool: Success status
        """
        if not self.can_send_notification():
            return False

        try:
            # Try to use plyer for cross-platform notifications
            from plyer import notification

            notification.notify(
                title=title,
                message=message,
                app_name='Motion Detector',
                timeout=10
            )

            self.last_notification_time = datetime.now()
            return True

        except ImportError:
            print("plyer not installed. Desktop notifications unavailable.")
            return False
        except Exception as e:
            print(f"Error sending desktop notification: {e}")
            return False

    def send_webhook_notification(self, webhook_url: str, data: dict) -> bool:
        """
        Send webhook notification (e.g., to Discord, Slack, etc.)

        Args:
            webhook_url: Webhook URL
            data: Data to send

        Returns:
            bool: Success status
        """
        if not self.can_send_notification():
            return False

        try:
            response = requests.post(webhook_url, json=data, timeout=5)

            if response.status_code == 200:
                self.last_notification_time = datetime.now()
                return True
            else:
                print(f"Webhook failed with status {response.status_code}")
                return False

        except Exception as e:
            print(f"Error sending webhook: {e}")
            return False

    def send_discord_notification(self, webhook_url: str, message: str,
                                  image_url: Optional[str] = None) -> bool:
        """
        Send Discord webhook notification

        Args:
            webhook_url: Discord webhook URL
            message: Message text
            image_url: Optional image URL

        Returns:
            bool: Success status
        """
        data = {
            "content": message,
            "username": "Motion Detector Bot"
        }

        if image_url:
            data["embeds"] = [{
                "title": "Motion Detected",
                "description": message,
                "color": 16711680,  # Red
                "image": {"url": image_url},
                "timestamp": datetime.now().isoformat()
            }]

        return self.send_webhook_notification(webhook_url, data)

    def send_slack_notification(self, webhook_url: str, message: str) -> bool:
        """
        Send Slack webhook notification

        Args:
            webhook_url: Slack webhook URL
            message: Message text

        Returns:
            bool: Success status
        """
        data = {
            "text": message,
            "username": "Motion Detector Bot",
            "icon_emoji": ":video_camera:"
        }

        return self.send_webhook_notification(webhook_url, data)

    def notify_motion_detected(self, duration: Optional[float] = None,
                              image_path: Optional[str] = None) -> bool:
        """
        Send motion detection notification through all configured channels

        Args:
            duration: Duration of motion event in seconds
            image_path: Optional path to snapshot image

        Returns:
            bool: Success status
        """
        if not self.can_send_notification():
            return False

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if duration:
            message = f"Motion detected at {timestamp}. Duration: {duration:.1f}s"
        else:
            message = f"Motion detected at {timestamp}"

        success = False

        # Desktop notification
        if self.config.get('desktop_enabled', True):
            success |= self.send_desktop_notification("Motion Detected!", message)

        # Email notification
        if self.config.get('email_enabled', False):
            subject = "Motion Detector Alert"
            success |= self.send_email_notification(subject, message, image_path)

        # Discord webhook
        discord_webhook = self.config.get('discord_webhook')
        if discord_webhook:
            success |= self.send_discord_notification(discord_webhook, message)

        # Slack webhook
        slack_webhook = self.config.get('slack_webhook')
        if slack_webhook:
            success |= self.send_slack_notification(slack_webhook, message)

        return success


# Example configuration
EXAMPLE_CONFIG = {
    'cooldown': 60,  # seconds between notifications
    'desktop_enabled': True,
    'email_enabled': False,
    'email': {
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'sender': 'your-email@gmail.com',
        'password': 'your-app-password',
        'recipient': 'recipient@email.com'
    },
    'discord_webhook': None,  # 'https://discord.com/api/webhooks/...'
    'slack_webhook': None  # 'https://hooks.slack.com/services/...'
}
