from django import forms
from django.db import models

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField, StreamField, StreamBlock
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel, StreamFieldPanel
from wagtail.wagtailcore.blocks import TextBlock, StructBlock, StreamBlock, FieldBlock, CharBlock, RichTextBlock, RawHTMLBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtaildocs.blocks import DocumentChooserBlock


from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index

from staffs.models import StaffPage



class PullQuoteBlock(StructBlock):
    quote = TextBlock("quote title")
    attribution = CharBlock()

    class Meta:
        icon = "openquote"

class ImageFormatChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('left', 'Wrap left'), ('right', 'Wrap right'), ('mid', 'Mid width'), ('full', 'Full width'),
    ))

class HTMLAlignmentChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('normal', 'Normal'), ('full', 'Full width'),
    ))

class ImageBlock(StructBlock):
    image = ImageChooserBlock()
    caption = RichTextBlock()
    alignment = ImageFormatChoiceBlock()

class AlignedHTMLBlock(StructBlock):
    html = RawHTMLBlock()
    alignment = HTMLAlignmentChoiceBlock()

    class Meta:
        icon = "code"



class BlogIndexPage(Page):
    intro = RichTextField(blank=True)


    def get_context(self, request):   
        context = super(BlogIndexPage, self).get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')

        #Pagination
        page = request.GET.get('page')
        paginator = Paginator(blogpages, 9) # Show 9 blogs per page
        try:
            blogpages = paginator.page(page)
        except PageNotAnInteger:
            blogpages =paginator.page(1)
        except EmptyPage:
            blogpages = paginator.page(paginator.num_pages)

        context['blogpages'] = blogpages
        return context

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]


# class BlogTagIndexPage(Page):
#     def get_context(self, request):
#         tag = request.GET.get('tag')
#         blogpages = BlogPage.objects.filter(tags__name=tag)

#         context = super(BlogTagIndexPage, self).get_context(request)
#         context['blogpages'] = blogpages
#         return context



# class BlogPageTag(TaggedItemBase):
#     content_object = ParentalKey('BlogPage', related_name='tagged_items')


class BlogPageAuthor(Orderable):
    page = ParentalKey('BlogPage', related_name='related_author') 
    author = models.ForeignKey(
        'staffs.StaffPage',
        null=True,
        blank=True,
        related_name='+'
    )

    panels = [
        PageChooserPanel('author'),
    ]


class BlogPage(Page):
    header_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    intro = models.CharField(max_length=250)
    # body = RichTextField(blank=True)
    body = StreamField([
        ('h1', CharBlock(icon="title", classanme="title")),
        ('h2', CharBlock(icon="title", classanme="title")),
        ('h3', CharBlock(icon="title", classanme="title")),
        ('h4', CharBlock(icon="title", classanme="title")),
        ('h5', CharBlock(icon="title", classanme="title")),
        ('h6', CharBlock(icon="title", classanme="title")),
        # ('intro', RichTextBlock(icon="pilcrow")),
        ('paragraph', RichTextBlock(icon="pilcrow")),
        ('aligned_image', ImageBlock(label="Aligned image", icon="image")),
        ('pullquote', PullQuoteBlock()),
        ('raw_html', RawHTMLBlock(label='Raw HTML', icon="code")),
        ('embed', EmbedBlock(icon="code")),
    ])
    # tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    date = models.DateField("Post date")
    # categories = ParentalManyToManyField('blog.BlogCategory', blank=True)
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )


    # def main_image(self):
    #     gallery_item = self.gallery_images.first()
    #     if gallery_item:
    #         return gallery_item.image
    #     else:
    #         return None

    @property
    def has_authors(self):
        for author in self.related_author.all():
            if author.author:
                return True

    search_field = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        # MultiFieldPanel([
        #     FieldPanel('date'),
        #     FieldPanel('tags'),
        #     FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        # ], heading="Blog information"),
        # FieldPanel('date'),
        ImageChooserPanel('header_image'),
        FieldPanel('date'),
        FieldPanel('intro'),
        StreamFieldPanel('body'),
        InlinePanel('related_author', label="Author"),
        # FieldPanel('tags'),
        ImageChooserPanel('feed_image'),


        # InlinePanel('gallery_images', label='Gallery images')
    ]


# class BlogPageGalleryImage(Orderable):
#     page = ParentalKey(BlogPage, related_name='gallery_images')
#     image = models.ForeignKey('wagtailimages.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='+')
#     caption = models.CharField(blank=True, max_length=250)

#     panesl = [
#         ImageChooserPanel('image'),
#         FieldPanel('caption')
#     ]

@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('icon'),
    ]
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'blog categories'

