from __future__ import absolute_import, unicode_literals
from datetime import date
from django import forms

from django.db import models

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailsearch import index

from modelcluster.fields import ParentalKey



class SideBarPlacement(models.Model):
    page = ParentalKey('wagtailcore.Page', related_name='sidebar_placements')
    sidebar = models.ForeignKey('SideBar', related_name='+')

    api_fields = ['sidebar']
    

@register_snippet
class SideBar(models.Model):
    page = models.ForeignKey(
        'wagtailcore.Page',
        related_name='sidebars',
        null=True,
        blank=True
    )
    url = models.URLField(null=True, blank=True)
    text = models.CharField(max_length=255)

    panels = [
        PageChooserPanel('page'),
        FieldPanel('url'),
        FieldPanel('text'),
    ]

    api_fields = ['page', 'url', 'text']

    def __str__(self):
        return self.text


class AboutPageAssociateLink(Orderable):
    page = ParentalKey('AboutPage', related_name='about_associate')
    ass_title = models.CharField(max_length=300, null=True, blank=True)
    ass_url = models.URLField(null=True, blank=True)
    ass_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel('ass_title'),
        FieldPanel('ass_url'),
        ImageChooserPanel('ass_image'),
    ]


class AboutPage(Page):
    # header_image = models.ForeignKey(
    #     'wagtailimages.Image',
    #     null=True,
    #     blank=True,
    #     on_delete=models.SET_NULL,
    #     related_name='+'
    # )
    heading = models.CharField(max_length=500, null=True, blank=True)
    # sub_heading = models.CharField(max_length=500, null=True, blank=True)
    body = RichTextField(null=True, blank=True)

    content_panels = [
        FieldPanel('title', classname='full'),
        # ImageChooserPanel('header_image'),
        FieldPanel('heading'),
        # FieldPanel('sub_heading'),
        FieldPanel('body', classname='about description'),
        InlinePanel('about_associate', label='Other associated content')
    ]