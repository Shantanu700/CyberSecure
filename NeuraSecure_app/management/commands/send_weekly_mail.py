# myapp/management/commands/send_weekly_email.py
from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from NeuraSecure_app.models import *

class Command(BaseCommand):
    help = 'Sends a weekly email with both plain text and HTML content'

    def handle(self, *args, **kwargs):
        subject = 'Weekly Update Regarding Cyber Security'
        from_email = 'shantanugupta13524@gmail.com'
        recipient_list_1 = list(subscribed_cat.objects.filter(subscribed_category_id=1).values('subscription_id__scr_user__email'))
        email_list_1 = [item['subscription_id__scr_user__email'] for item in recipient_list_1]
        unique_email_list_1 = list(set(email_list_1))
        
        recipient_list_2 = list(subscribed_cat.objects.filter(subscribed_category_id=2).values('subscription_id__scr_user__email'))
        email_list_2 = [item['subscription_id__scr_user__email'] for item in recipient_list_2]
        unique_email_list_2 = list(set(email_list_2))
        
        recipient_list_3 = list(subscribed_cat.objects.filter(subscribed_category_id=3).values('subscription_id__scr_user__email'))
        email_list_3 = [item['subscription_id__scr_user__email'] for item in recipient_list_3]
        unique_email_list_3 = list(set(email_list_3))
        
        recipient_list_4 = list(subscribed_cat.objects.filter(subscribed_category_id=4).values('subscription_id__scr_user__email'))
        email_list_4 = [item['subscription_id__scr_user__email'] for item in recipient_list_4]
        unique_email_list_4 = list(set(email_list_4))

        cat_1_news = Data.objects.filter(category_id=1).order_by('-date').values('title','info')[:5]
        cat_2_news = Data.objects.filter(category_id=2).order_by('-date')[:5]
        cat_3_news = Data.objects.filter(category_id=3).order_by('-date')[:5]
        cat_4_news = Data.objects.filter(category_id=4).order_by('-date')[:5]
        # Create the email content
        text_content = 'This is your weekly update in plain text.'
        html_content = '<p>This is your <strong>weekly update</strong> in HTML.</p>'

        # Create the EmailMultiAlternatives object
        email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
        email.attach_alternative(html_content, "text/html")

        # Send the email
        email.send()
        self.stdout.write(self.style.SUCCESS('Weekly email sent successfully'))
