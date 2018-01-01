from __future__ import absolute_import, unicode_literals
from datetime import date
from django import forms

from django.db import models

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailsearch import index

from modelcluster.fields import ParentalKey



class HomePageRelatedLink(Orderable):
    page = ParentalKey('HomePage', related_name='related_links')
    name = models.CharField(max_length=255,null=True, blank=True)
    url = models.URLField()

    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
    ]


class HomePageLanding(Orderable):
    page = ParentalKey('HomePage', related_name='home_landing')
    landing_title = models.CharField(max_length=255,null=True,blank=True)
    landing_intro = RichTextField(null=True, blank=True)

    panels = [
        FieldPanel('landing_title'),
        FieldPanel('landing_intro', classname='after header image intro')
    ]



class HomePageMarketing(Orderable):
    page = ParentalKey('HomePage', related_name='home_market')
    market_title = models.CharField(max_length=300, null=True, blank=True)
    market_desc = models.CharField(max_length=300, null=True, blank=True)
    market_url = models.URLField(null=True, blank=True)
    market_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+')

    search_fields = Page.search_fields + [
    index.SearchField('market_title'),
    # index.SearchField('sub_heading'),
    # index.SearchField('intro')
    ]


    panels = [
        FieldPanel('market_title'),
        FieldPanel('market_url'),
        FieldPanel('market_desc'),
        ImageChooserPanel('market_image')
    ]



class HomePage(Page):
    heading = models.CharField(max_length=200, null=True, blank=True)
    sub_heading = models.CharField(max_length=200, null=True, blank=True)
    # intro = RichTextField(blank=True)
    # landing_image = models.ForeignKey(
    #     'wagtailimages.Image',
    #     null=True,
    #     blank=True,
    #     on_delete=models.SET_NULL,
    #     related_name='+' 
    # )
    # body = RichTextField(blank=True)

    def page_landing(self):
        landing_item = self.home_landing.first()
        if landing_item:
            return landing_item.landing_title
        else:
            return None

    def page_market(self):
        market_item = self.home_market.first()
        if market_item:
            return market_item.market_title
        else:
            return None

    

    search_fields = Page.search_fields + [
        index.SearchField('heading'),
        index.SearchField('sub_heading'),
        # index.SearchField('intro')
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('heading'),
            FieldPanel('sub_heading'),
            # FieldPanel('intro', classname='full intro'),
            # ImageChooserPanel('landing_image'),

        ], heading="Homepage Landing information"),
        
        InlinePanel('home_landing', label='Home landing message'),
        InlinePanel('home_market', label='Home section for external service'),
        InlinePanel('related_links', label="Related links")
    ]

HomePage.promote_panels = Page.promote_panels
