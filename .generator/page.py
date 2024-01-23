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
import json

class PageBuilder:
    """Forms pages for the site."""

    __slots__ = [
        '_style',
        '_style_hash',
        '_descriptions'
    ]

    def __init__(self):
        with open(".generator/style.css", "r") as css:
            self._style = css.read()
        self._style_hash = "sha256-" + b64encode(
                sha256(("\n" + self._style).encode('utf-8')
            ).digest()).decode('utf-8')
        with open(".generator/descriptions.json", "r") as f:
            self._descriptions = json.load(f)

    def build_report_page(self, report):
        """Builds a page for a report.

        Keyword arguments:
        report - the report the page is about
        """
        description = self._descriptions[report.report_number()] if (
            report.report_number() in self._descriptions) else report.abstract()
        head_info = {
            "style-hash" : self._style_hash,
            "canonical" : report.canonical_url(),
            "title" : report.title(),
            "description" : description,
            "social-preview" : report.social_preview_image_url()
        }
        return self._build_head(
            head_info,
            self._build_citation_tags(report)
        ) + self._build_content_header(report) + self._build_report_page_content(report)

    def _build_report_page_content(self, report):
        authors = [ self._formatted_author(a) for a in report.author_list() ]
        author_field = authors[0] if len(authors)==1 else (
            authors[0] + " and " + authors[1] if len(authors)==2 else (
            ", ".join(authors[:-1]) + ", and " + authors[-1]
            )
        )
        return report_page_content.format(
            PDF_FILE=report.pdf_filename(),
            BIBTEX=report.bibtex_web(),
            TITLE=report.title(),
            REPORT_NUM=report.report_number(),
            INSTITUTION=report.institution(),
            YEAR=report.year(),
            MONTH=report.month(),
            BIB_FILE=report.bib_filename(),
            ABSTRACT=report.abstract(),
            AUTHORS=author_field 
        )

    def _formatted_author(self, author):
        me = {
            "Vincent A. Cicirello",
            "Vincent Cicirello",
            "V. A. Cicirello",
            "V. Cicirello"
        }
        me_with_link = """<a href="https://www.cicirello.org/">Vincent A. Cicirello</a>"""
        return me_with_link if author in me else author
        
    def _build_content_header(self, report):
        return content_header.format(
            HEADER_SVG=report.svg_filename(),
            PAGE_TITLE=report.title() + " - Technical Report " + report.report_number()
        )

    def _build_citation_tags(self, report):
        authors = [ citation_author.format(AUTHOR=a) for a in report.author_list() ]
        return citation_tags.format(
            TITLE=report.title(),
            YEAR=report.year(),
            REPORT_NUM=report.report_number(),
            INSTITUTION=report.institution(),
            CANONICAL=report.canonical_url(),
            PDF_URL=report.pdf_url(),
            AUTHORS="\n".join(authors)
        )

    def _build_head(self, head_info, citation_tags=None):
        return "<!DOCTYPE html>\n<html lang=en>\n<head>\n" + (
                page_head_start.format(
                    STYLEHASH=head_info["style-hash"],
                    CANONICAL=head_info["canonical"],
                    TITLE=head_info["title"],
                    DESCRIPTION=head_info["description"],
                    SOCIALPREVIEW=head_info["social-preview"]
                ) + (
                    citation_tags if citation_tags else ""
                ) + self._style_block()
            )+ "\n</head>\n"

    def _style_block(self):
        return "<style>\n" + self._style + "</style>"
        
