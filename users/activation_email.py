from djoser.email import ActivationEmail
from django.conf import settings

class CustomActivationEmail(ActivationEmail):
  def get_context_data(self):
    # Add custom domain to context for email template
    context = super().get_context_data()
    context["domain"] = settings.FRONT_END_ORIGIN.split('//')[1]
    return context