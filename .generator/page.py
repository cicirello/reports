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
from datetime import datetime

# Set this to True for a less strict content security policy for viewing
# locally. Set to False for a stricter content security policy.
VIEW_LOCAL = True

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

    def build_404(self):
        """Builds the 404 page."""
        return template_404.format(
            STYLEHASH=self._style_hash,
            STYLE=self._style_block(),
            CONTENT_HEADER=content_header.format(
                HEADER_SVG="images/404.svg",
                PAGE_TITLE="404 - File not found",
                ACTIVE=""
                )
            ) + page_footer.format(CURRENT_YEAR=datetime.now().year)

    def build_home_page(self, reports):
        """Builds the home page for the Tech Reports website.

        Keyword arguments:
        reports - a list of all of the reports in sorted order, most recent first
        """
        head_info = {
            "style-hash" : self._style_hash,
            "canonical" : url_root,
            "title" : site_title,
            "description" : site_description.replace("\n", " ").strip(),
            "social-preview" : url_root + "images/reports.png"
        }
        return self._build_head(
            head_info
        ) + content_header.format(
            HEADER_SVG="images/reports.svg",
            PAGE_TITLE=site_title,
            ACTIVE=' class="active"'
        ) + self._build_home_page_content(
            reports
        ) + page_footer.format(CURRENT_YEAR=datetime.now().year)

    def build_report_page(self, report):
        """Builds a page for a report.

        Keyword arguments:
        report - the report the page is about
        """
        global VIEW_LOCAL
        head_info = {
            "style-hash" : self._style_hash,
            "canonical" : report.canonical_url(),
            "title" : report.title(),
            "description" : report.description(),
            "social-preview" : report.social_preview_image_url()
        }
        return self._build_head(
            head_info,
            self._build_citation_tags(report),
            " frame-src {0}; object-src {0};".format(
                "'self'" if VIEW_LOCAL else report.pdf_url()
            )
        ) + self._build_content_header(
            report
        ) + report.report_page(
        ) + page_footer.format(CURRENT_YEAR=datetime.now().year)

    def _build_home_page_content(self, reports):
        return home_page_content + self._year_block(reports) + link_legend + self._report_list(reports) + "\n</article>\n"

    def _report_list(self, reports):
        lines = []
        previous_year = -1
        year_start = '<h3 id="{0}">{0} (<a href="#top"><em>Top of the page</em></a>)</h3>\n<ul>'
        for r in reports:
            if r.year() != previous_year:
                if previous_year != -1:
                    lines.append("</ul>")
                lines.append(year_start.format(r.year()))
                previous_year = r.year()
            lines.append(r.report_listing())
        lines.append("</ul>")
        return "\n".join(lines)

    def _year_block(self, reports):
        years = []
        for r in reports:
            if len(years)==0 or r.year() != years[-1]:
                years.append(r.year())
        start = '<details>\n<summary>Browse reports by year</summary>\n<ul id="pubyears">\n'
        end = '</ul>\n</details>\n'
        year_template = '<li><a href="#{0}">{0}</a>,</li>'
        last_template = '<li><a href="#{0}">{0}</a></li>'
        year_items = [ year_template.format(y) for y in years[:-1]]
        year_items.append(last_template.format(years[-1]))
        return start + "\n".join(year_items) + end
    
    def _build_content_header(self, report):
        return content_header.format(
            HEADER_SVG=report.svg_filename(),
            PAGE_TITLE=report.title() + " - Technical Report " + report.report_number(),
            ACTIVE=""
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

    def _build_head(self, head_info, citation_tags=None, object_src_policy=""):
        return "<!DOCTYPE html>\n<html lang=en>\n<head>\n" + (
                page_head_start.format(
                    STYLEHASH=head_info["style-hash"],
                    CANONICAL=head_info["canonical"],
                    TITLE=head_info["title"],
                    DESCRIPTION=head_info["description"],
                    SOCIALPREVIEW=head_info["social-preview"],
                    OBJECTSRC=object_src_policy
                ) + (
                    citation_tags if citation_tags else ""
                ) + self._style_block()
            ) + "\n</head>\n"

    def _style_block(self):
        return "<style>\n" + self._style + "</style>"
        
