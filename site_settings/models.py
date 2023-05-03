from django.db import models

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
# BaseSetting, BaseGenericSetting

# Create your models here.

@register_setting
class SocialMediaSettings(BaseGenericSetting):
    facebook = models.URLField(blank=True, null=True, help_text='URL')
    twitter = models.URLField(blank=True, null=True, help_text='URL')
    youtube = models.URLField(blank=True, null=True, help_text='URL')
    
    panels = [
        MultiFieldPanel ([
            FieldPanel("facebook"),
            FieldPanel("twitter"),
            FieldPanel("youtube"),
        ], heading = "Social Media Settings")
    ]