from __future__ import absolute_import, unicode_literals
from datetime import date
from django import forms

from django.db import models
from django.utils.functional import cached_property

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailsearch import index

from modelcluster.fields import ParentalKey




class StaffPageRelatedLink(Orderable):
    page = ParentalKey('StaffPage', related_name='related_links')
    name = models.CharField(max_length=255,null=True, blank=True)
    url = models.URLField()

    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
    ]


class StaffPage(Page):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    intro = models.TextField(max_length=None, blank=True)
    biography = RichTextField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + [
        index.SearchField('first_name'),
        index.SearchField('last_name'),
        index.SearchField('intro'),
        index.SearchField('biography'),
    ]

StaffPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('first_name'),
    FieldPanel('last_name'),
    FieldPanel('intro'),
    FieldPanel('biography', classname="Person's biography"),
    ImageChooserPanel('image'),
    ImageChooserPanel('feed_image'),
    InlinePanel('related_links', label="Other links to be added")
]
# PersonPage.promote_panels = Page.promote_panels


class StaffIndexPage(Page):
    header_intro = models.TextField()
    team_intro = models.TextField()

    @cached_property
    def people(self):
        return StaffPage.objects.live().public()

    content_panels = Page.content_panels + [
        FieldPanel('header_intro'),
        FieldPanel('team_intro')
    ]