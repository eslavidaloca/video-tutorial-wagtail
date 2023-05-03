from django.db import models
from django.shortcuts import render

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel, PageChooserPanel

from modelcluster.fields import ParentalKey
from wagtail.search import index
from streams import blocks

from wagtail.contrib.routable_page.models import RoutablePageMixin, path, re_path, route

class HomePage(RoutablePageMixin, Page):
    """Home page model"""
    max_count = 1 # This doesn't allow another home page from existing
    # template = "templates/home/home_page.html"
    banner_title = models.CharField(max_length=100, blank=False, null=True)
    banner_subtitle = RichTextField(blank=True)
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    banner_cta = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    # def main_image(self):
    #     banner_item = self.banner_image.first()
    #     if banner_item:
    #         return banner_item.image
    #     else:
    #         return None

    search_fields = Page.search_fields + [
        index.SearchField('banner_title'),
        index.SearchField('banner_subtitle'),
    ]
    
    content = StreamField(
        [
            ('cta', blocks.CTABlock()),
        ],
        use_json_field=True,
        null=True,
        blank=True
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("banner_title"),
            FieldPanel("banner_subtitle"),
            FieldPanel("banner_image"),
            PageChooserPanel('banner_cta'),
        ], heading = 'Banner Options'),
        InlinePanel('carousel_images', label="Imagenes del carrusel", max_num=5, min_num=1),
        FieldPanel('content'),
    ]
    
    class Meta:
        verbose_name = "Home page"
        verbose_name_plural = "Home pages"
    
    
class HomePageCarouselImages(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='carousel_images')
    
    carousel_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('carousel_image'),
        FieldPanel('caption'),
    ]
    
    # IDK why this doesnt work # Now I know, because we havent established the home paht correctly
    @path('subscribe/') # will override the default Page serving mechanism
    def the_subscribe_page(self, request, *args, **kwargs):
        """
        View function for the current events page
        """
        context = self.get_context(request, *args, **kwargs)
        context['a_special_test'] = 'Hello everyone, im asleep already and I slept pretty well actually'
        # events = EventPage.objects.live().filter(event_date__gte=datetime.date.today())

        # NOTE: We can use the RoutablePageMixin.render() method to render
        # the page as normal, but with some of the context values overridden
        return self.render(
            request,
            context_overrides={
                'title': "Pruebas ",
                'context': context,
            },
            template="home/subscribe.html"
        )
    
    # @path('subscribe/')
    # @path('')
    # @re_path(r'^subscribe/$', name='subscribe')
    # @route(r'^subscribe/$')
    # def the_subscribe_page(self, request, *args, **kwargs):
    #     context = self.get_context(request, *args, **kwargs)
    #     context['a_special_test'] = 'Hello everyone, im asleep already and I slept pretty well actually'
    #     return self.render(request, context, template="home/subscribe.html")