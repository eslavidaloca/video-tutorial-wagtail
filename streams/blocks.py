"""Streamfields live in here"""

import wagtail.blocks as blocks
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock

class TitleAndTextBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, help_text='Agrega tu titulo')
    text = blocks.TextBlock(required=True, help_text='Agrega texto adicional')
    
    class Meta:
        # template = 'streams/title_text_block.html'
        icon = 'edit'
        label = 'Titulo y texto'

class CardBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, help_text='Agrega tu titulo')
    
    # CardBody = StreamField([
    #     (
    #         'cards', blocks.ListBlock(
    #             blocks.StructBlock(
    #                 [
    #                     ('image', ImageChooserBlock(required=True)),
    #                     ('title', blocks.CharBlock(required=True, max_length=40)),
    #                     ('text', blocks.CharBlock(required=True, max_length=200)),
    #                     ('button_page', blocks.PageChooserBlock(required=False)),
    #                     ('button_url', blocks.URLBlock(required=False, help_text='El boton de la pagina tiene prioridad sobre esto')),
    #                 ]
    #             )
    #         )
    #     ),
    # ], use_json_field=True)
    
    
    cards = blocks.ListBlock(
        blocks.StructBlock(
            [
                ('image', ImageChooserBlock(required=True)),
                ('title', blocks.CharBlock(required=True, max_length=40)),
                ('text', blocks.CharBlock(required=True, max_length=200)),
                ('button_page', blocks.PageChooserBlock(required=False)),
                ('button_url', blocks.URLBlock(required=False, help_text='El boton de la pagina tiene prioridad sobre esto')),
            ]
        )
    )
    
    class Meta:
        template = 'streams/card_block.html'
        icon = 'placeholder'
        label = 'Staff cards'

class RichTextBlock(blocks.RichTextBlock):
    class Meta:
        icon = 'edit'
        label = 'Full Rich Text'

class CTABlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True,max_length=40)
    text = blocks.RichTextBlock(required=True)
    button_page = blocks.PageChooserBlock(required=False)
    button_url = blocks.URLBlock(required=False)
    button_text = blocks.CharBlock(required=True, default='Aprende mas',max_length=30)
    
    class Meta:
        template = 'streams/cta_block.html'
        icon = 'arrow-right'
        label = 'Call To Action'

# This import is down here bc otherwise the imports become circular imports and make
from blog.models import BlogDetailPage

class LinkStructValue(blocks.StructValue):
    """ Additional logic for our urls """
    
    def url(self):
        button_page = self.get('button_page')
        button_url = self.get('button_url')
        if button_page:
            return button_page.url
        elif button_url:
            return button_url
        
        return None
    
    def latest_posts(self):
        return BlogDetailPage.objects.live()[:3]
    
class ButtonBlock(blocks.StructBlock):
    button_page = blocks.PageChooserBlock(required=False, help_text='If selected, this url will be used first')
    button_url = blocks.URLBlock(required=False, help_text='If added, this url will be used secondarily to the button')
    
    # def get_context(self, request, *args, **kwargs):
    #     context = super().get_context(request, *args, **kwargs)
    #     context['latest_posts'] = BlogDetailPage.objects.live.public()[:3]
    #     return context
    
    class Meta:
        template = 'streams/button_block.html'
        icon = 'placeholder'
        label = 'Single button'
        value_class = LinkStructValue