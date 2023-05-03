from django import forms
from django.db import models
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render

from wagtail.models import Page, Orderable
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.fields import StreamField
from wagtail.contrib.routable_page.models import RoutablePageMixin, path, re_path, route
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey, ParentalManyToManyField

from streams import blocks

@register_snippet
class BlogAuthor(models.Model):
    """ Blog author for snippets """
    
    name = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name='+'
    )
    
    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                FieldPanel("image")
            ],
            heading="Nombre e imagen"
        ),
        MultiFieldPanel(
            [
                FieldPanel("website"),
            ],
            heading="Links"
        )
    ]
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Blog Author'
        verbose_name_plural = 'Blog Authors'

class BlogAuthorsOrderable(Orderable):
    """ This allow us to select one or more blog authors from snippets """
    
    page = ParentalKey("BlogDetailPage", related_name='blog_authors')
    author = models.ForeignKey(
        'blog.BlogAuthor',
        on_delete=models.CASCADE,
    )
    
    panels = [
        FieldPanel('author')
    ]

@register_snippet
class BlogCategory(models.Model):
    """ Blog Category for a snippet """
    
    name = models.CharField(max_length=255)
    slug = models.SlugField(
        verbose_name="slug",
        allow_unicode=True,
        max_length=255,
        help_text='A slug to identify posts by this category',
    )
    
    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"
        ordering = ["name"]

class BlogListingPage(RoutablePageMixin, Page):
    """
    Getting all the Blog Details and putting
    them into the context of this template
    """
    
    custom_title = models.CharField(max_length=100, blank=False, null=False, help_text='Sobrescribe el titulo por defecto')
    
    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
    ]
    
    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context"""
        
        contexto = super().get_context(request, *args, **kwargs)
        # contexto['posts'] = BlogDetailPage.objects.live().public()
        # contexto['authors']= BlogAuthor.objects.all()
        # contexto['articles'] = BlogDetailPage.objects.live().exact_type(ArticleBlogPage).specific(defer=False) #To get only one child type from parent
        # contexto['articles'] = BlogDetailPage.objects.live().not_exact_type(BlogDetailPage).specific() #To get childs without have the blogDetailPage type
        
        all_posts = BlogDetailPage.objects.live().public().order_by('-first_published_at')
        paginator = Paginator(all_posts, 2)
        
        page = request.GET.get("page")
        
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        
        
        contexto['posts'] = posts
        contexto['categories'] = BlogCategory.objects.all()
        return contexto
    
    @route(r'^latest/?$', name="latest_post")
    def latest_blog_posts(self, request, *args, **kwargs):
        contexto = self.get_context(request, *args, **kwargs)
        contexto['posts'] = contexto['posts'][:1]
        contexto['link_return'] = self.reverse_subpage('latest_post')
        return render(request, "blog/latest_posts.html", contexto)
    
    def get_sitemap_urls(self, request):
        sitemap = super().get_sitemap_urls(request)
        sitemap.append(
            {
                "location": self.full_url + self.reverse_subpage("latest_post"),
                "lastmod": (self.last_published_at or self.latest_revision_created_at),
                "priority": 0.8 #Goes from 0 to 1 (0, 0.1, 0.2 ... 1)
            }
        )
        return sitemap

class BlogDetailPage(Page):
    """ Parental blog detail page """
    
    custom_title = models.CharField(max_length=100, blank=False, null=False, help_text='Sobrescribe el titulo por defecto')
    # authors = ParentalManyToManyField('blog.BlogAuthor', blank=True) # Gotta activate this in order to make functional the fieldpanel of authors
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=False,
        null=True,
        related_name='+',
        on_delete=models.SET_NULL,
    )
    
    categories = ParentalManyToManyField("blog.BlogCategory", blank=True)
    
    content = StreamField(
        [
            ('title_and_text', blocks.TitleAndTextBlock()),
            ('Rich_text', blocks.RichTextBlock()),
            ('cards', blocks.CardBlock()),
            ('cta', blocks.CTABlock()),
        ],
        use_json_field=True,
        null=True,
        blank=True
    )
    
    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
        FieldPanel('banner_image'),
        MultiFieldPanel(
            [
                InlinePanel('blog_authors', label="Author", min_num=1, max_num=4), #This now works
                # FieldPanel('authors', widget=forms.CheckboxSelectMultiple),
            ],
            heading="Author(s)"
        ),
        MultiFieldPanel(
            [
                FieldPanel("categories", widget=forms.CheckboxSelectMultiple)
            ],
            heading="Categories"     
        ),
        FieldPanel('content')
    ]

# First subclassed blog post page
class ArticleBlogPage(BlogDetailPage):
    """ A subclassed blog post page for articles """
    
    subtitle = models.CharField(max_length=100, default='', blank=True, null=True)
    intro_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, help_text="Best size for this image will be 1400x400")
    
    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
        FieldPanel('subtitle'),
        FieldPanel('banner_image'),
        FieldPanel('intro_image'),
        MultiFieldPanel(
            [
                InlinePanel('blog_authors', label="Author", min_num=1, max_num=4), #This now works
                # FieldPanel('authors', widget=forms.CheckboxSelectMultiple),
            ],
            heading="Author(s)"
        ),
        MultiFieldPanel(
            [
                FieldPanel("categories", widget=forms.CheckboxSelectMultiple)
            ],
            heading="Categories"     
        ),
        FieldPanel('content')
    ]
    
# Second subclassedpage
class VideoBlogPage(BlogDetailPage):
    """ A video subclassed page """
    
    youtube_video_id = models.CharField(max_length=30)
    
    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
        FieldPanel('banner_image'),
        MultiFieldPanel(
            [
                InlinePanel('blog_authors', label="Author", min_num=1, max_num=4), #This now works
                # FieldPanel('authors', widget=forms.CheckboxSelectMultiple),
            ],
            heading="Author(s)"
        ),
        MultiFieldPanel(
            [
                FieldPanel("categories", widget=forms.CheckboxSelectMultiple)
            ],
            heading="Categories"     
        ),
        FieldPanel('youtube_video_id'),
        FieldPanel('content')
    ]