from django.db import models
from wagtail.models import Page

from streams import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField

class FlexPage(Page):
    content = StreamField(
        [
            ('title_and_text', blocks.TitleAndTextBlock()),
            ('Rich_text', blocks.RichTextBlock()),
            ('cards', blocks.CardBlock()),
            ('cta', blocks.CTABlock()),
            ('button', blocks.ButtonBlock()),
        ],
        use_json_field=True,
        null=True,
        blank=True
    )
    
    subtitle = models.CharField(max_length=100, null=True, blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('content')
    ]
    
    class Meta:
        verbose_name = "Flex Page"
        verbose_name_plural = "Flex Pages"