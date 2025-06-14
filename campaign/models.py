from django.db import models


class EmailCampaign(models.Model):
    subject = models.CharField(max_length=255)
    message = models.TextField()
    recipients = models.TextField(help_text="Comma-separated email addresses")
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.subject

    def get_recipient_list(self):
        return [email.strip() for email in self.recipients.split(",") if email.strip()]

    