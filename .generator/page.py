# Site generator for https://reports.cicirello.org/
# Copyright (c) 2024 Vincent A. Cicirello. All rights reserved.
#
# This site generator is almost certainly useless to anyone other than me.
# It is highly customized to generate one specific website. Therefore, I am
# not licensing it to others. Notice the "All rights reserved" in the
# copyright notice at the top.

from templates import *
from hashlib import sha256
from base64 import b64encode

class PageBuilder:
    """Forms pages for the site."""

    __slots__ = [
        '_style',
        '_style_hash'
    ]

    def __init__(self):
        with open(".generator/style.css", "r") as css:
            self._style = css.read()
        self._style_hash = "sha256-" + b64encode(
                sha256(("\n" + self._style).encode('utf-8')
            ).digest()).decode('utf-8')

    def build_report_page(self, report):
        """Builds a page for a report.

        Keyword arguments:
        report - the report the page is about
        """
        head_info = {
            "style-hash" : self._style_hash,
            "canonical" : report.canonical_url(),
            "title" : report.title(),
            "description" : report.page_description(),
            "social-preview" : report.social_preview_image_url()
        }
        return self._build_head(head_info)

    def _build_head(self, head_info):
        return "<!DOCTYPE html>\n<html lang=en>\n<head>\n" + (
                page_head_start.format(
                    STYLEHASH=head_info["style-hash"],
                    CANONICAL=head_info["canonical"],
                    TITLE=head_info["title"],
                    DESCRIPTION=head_info["description"],
                    SOCIALPREVIEW=head_info["social-preview"]
                ) + self._style_block()
            )+ "\n</head>"

    def _style_block(self):
        return "<style>\n" + self._style + "</style>"
        
