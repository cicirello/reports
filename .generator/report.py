# Site generator for https://reports.cicirello.org/
# Copyright (c) 2024 Vincent A. Cicirello. All rights reserved.
#
# This site generator is almost certainly useless to anyone other than me.
# It is highly customized to generate one specific website. Therefore, I am
# not licensing it to others. Notice the "All rights reserved" in the
# copyright notice at the top.

from templates import *
from text_length import calculateTextLength110, calculateTextLength110Weighted
import math

class Report:
    """Metadata for a single Technical Report as extracted from a BibTeX
    record."""

    __slots__ = [
        "_raw_bibtex",
        "_key",
        "_fields",
        "_first_dir",
        "_seq_num",
        "_other_citation"
        ]

    _line_y_values = [278, 449, 620, 791, 962]

    def __init__(self, report, additional_info):
        """Initializes a report object.

        Keyword arguments:
        report - a BibTeX record of a Tech Report
        additional_info - dictionary of additional metadata for the reports
        """
        self._raw_bibtex = report
        if report[:12].lower() != "@techreport{":
            raise Exception('BibTeX Not a TechReport')
        key_end = report.find(",", 12)
        self._key = report[12:key_end].strip()
        other_cite_start = min(
            self._not_found_is_infinite(report.find("@article", key_end+1)),
            self._not_found_is_infinite(report.find("@inproceedings", key_end+1)),
            self._not_found_is_infinite(report.find("@ARTICLE", key_end+1)),
            self._not_found_is_infinite(report.find("@INPROCEEDINGS", key_end+1))
        )
        self._fields = self._find_fields(report[key_end+1:other_cite_start] if (
            math.isfinite(other_cite_start)
            ) else report[key_end+1:])
        self._other_citation = report[other_cite_start:].strip() if (
            math.isfinite(other_cite_start)
            ) else ""
        if len(self._other_citation) > 0:
            self._other_citation += "\n\n"
        number_components = self._fields["number"].split("-")
        self._seq_num = number_components[-1]
        self._first_dir = number_components[-2]
        if self._fields["number"] in additional_info:
            self._fields.update(additional_info[self._fields["number"]])

    def _not_found_is_infinite(self, find_index):
        """Maps not found index of -1 to infinity.

        Keyword arguments:
        find_index - an index returned by find
        """
        return find_index if find_index >= 0 else math.inf

    def target_directory(self):
        """Returns the name of the target directory."""
        return self._first_dir + "/" + self._seq_num

    def output_bibtex_file(self):
        """Creates a bibtex file for the report."""
        with open(self._full_file(".bib"), "w") as f:
            f.write(
                bibtex_file_template.format(
                    KEY=self._fields["number"],
                    TITLE=self._fields["title"],
                    AUTHOR=self._fields["author"],
                    YEAR=self._fields["year"],
                    MONTH=self._fields["month"],
                    NUMBER=self._fields["number"],
                    INSTITUTION=self._fields["institution"],
                    URL=self.pdf_url(),
                    ABSTRACT=self._fields["abstract"],
                    OTHERCITE=self._other_citation
                )
            )

    def bibtex_web(self):
        """Formats a BibTeX record for inclusion on webpage."""
        return bibtex_web_template.format(
            KEY=self._fields["number"],
            TITLE=self._fields["title"],
            AUTHOR=self._fields["author"],
            YEAR=self._fields["year"],
            MONTH=self._fields["month"],
            NUMBER=self._fields["number"],
            INSTITUTION=self._fields["institution"],
            URL=self.pdf_url(),
            OTHERCITE=self._other_citation
        )

    def output_svg_file(self):
        """Creates an svg file for the report."""
        with open(self._full_file(".svg"), "w") as f:
            svg = self._build_svg()
            svg = svg.replace("\n", "")
            f.write(svg)

    def pdf_url(self):
        """Gets the full url of the pdf file."""
        return url_root + self._full_file(".pdf")

    def canonical_url(self):
        """Computes the canonical url to the page about the report."""
        return url_root + self.target_directory() + "/"

    def social_preview_image_url(self):
        """Computes the url to the social preview image."""
        return url_root + self._full_file(".png")

    def author_list(self):
        """Generates list of authors."""
        return self._fields["author"].split(" and ")

    def formatted_authors(self, link=True):
        """Formats the author list.

        Keyword arguments:
        link - if True, link me to my website
        """
        authors = [
            self._formatted_author(a) if link else a for a in self.author_list()
        ]
        return authors[0] if len(authors)==1 else (
            authors[0] + " and " + authors[1] if len(authors)==2 else (
            ", ".join(authors[:-1]) + ", and " + authors[-1]
            )
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

    def websafe(self, original):
        """Deals with LaTeX formatting stuff in abstract and title fields."""
        return original.replace(
            "$", ""
        ).replace(
            "``", "&quot;"
        ).replace(
            "''", "&quot;"
        ).replace(
            '"', "&quot;"
        ).replace(
            "\\rho", "&rho;"
        ).replace(
            "\\mu", "&mu;"
        )

    def title(self):
        """Gets the report title."""
        return self.websafe(self._fields["title"])

    def year(self):
        """Gets the year the report."""
        return self._fields["year"]

    def month(self):
        """Gets the month the report."""
        return self._fields["month"]

    def institution(self):
        """Gets the institution the report."""
        return self._fields["institution"]

    def abstract(self):
        """Gets the abstract of the report."""
        return self.websafe(self._fields["abstract"])

    def description(self):
        """Gets a description of the report for the page metadata"""
        if "description" in self._fields:
            return self._fields["description"]
        else:
            return self._fields["abstract"]

    def report_number(self):
        """Gets the report number."""
        return self._fields["number"]

    def svg_filename(self):
        """Gets name of SVG file"""
        return self._file_only(".svg")

    def pdf_filename(self):
        """Gets name of pdf file"""
        return self._file_only(".pdf")

    def bib_filename(self):
        """Gets name of bib file"""
        return self._file_only(".bib")

    def report_listing(self):
        """Generates the list element for the site homepage list
        of reports for this report."""
        other_links = ""
        if "doi" in self._fields:
            other_links += ' <a href="https://doi.org/{0}">[DOI]</a>'.format(
                self._fields["doi"])
        if "arxiv" in self._fields:
            other_links += ' <a href="{0}">[arXiv]</a>'.format(
                self._fields["arxiv"])
        if "code" in self._fields:
            other_links += ' <a href="{0}">[CODE]</a>'.format(
                self._fields["code"])
        return formatted_report_listing.format(
            ABSTRACT_PAGE=self.target_directory() + "/",
            TITLE=self.websafe(self._fields["title"]),
            AUTHORS=self.formatted_authors(False),
            REPORT_NUM=self._fields["number"],
            INSTITUTION=self._fields["institution"],
            YEAR=self._fields["year"],
            MONTH=self._fields["month"],
            PDF_FILE=self._full_file(".pdf"),
            BIB_FILE=self._full_file(".bib"),
            OTHERLINKS=other_links
        )

    def report_page(self):
        """Generates the content for the report's abstract/information page."""
        note = "<h4>" + self._fields["note"] + "</h4>\n" if (
            "note" in self._fields
        ) else ""
        arxiv = arxiv_link.format(
            self._fields["arxiv"]
            ) if "arxiv" in self._fields else ""
        code = code_link.format(
            self._fields["code"]
            ) if "code" in self._fields else ""
        doi = doi_link.format(
            self._fields["doi"]
            ) if "doi" in self._fields else ""
        formatted_cite = published_as.format(
            FORMATTED_CITE = self._fields["citation"],
            TYPE = self._fields["citation-type"] if (
                "citation-type" in self._fields) else "Journal Ref"
            ) if "citation" in self._fields else ""
        return report_page_content.format(
            PDF_FILE=self._file_only(".pdf"),
            BIBTEX=self.bibtex_web(),
            TITLE=self.websafe(self._fields["title"]),
            REPORT_NUM=self._fields["number"],
            INSTITUTION=self._fields["institution"],
            YEAR=self._fields["year"],
            MONTH=self._fields["month"],
            BIB_FILE=self._file_only(".bib"),
            ABSTRACT=self.websafe(self._fields["abstract"]),
            AUTHORS=self.formatted_authors(),
            NOTE=note,
            ARXIV=arxiv,
            CODE=code,
            DOI=doi,
            FORMATTED_CITE=formatted_cite
        )

    def _full_file(self, extension):
        """Forms the name of a file, relative to the root."""
        return self.target_directory() + "/" + self._file_only(extension)

    def _file_only(self, extension):
        """Forms the name of a file."""
        if extension == ".pdf" and "pdf-filename" in self._fields:
            return self._fields["pdf-filename"]
        return self._fields["number"] + extension

    def _find_fields(self, partial):
        """Extracts the BibTeX fields from a partial BibTeX record
        such that the record type and key have been stripped.

        Keyword arguments:
        partial - a partial BibTeX record such that the record type and key
            have been stripped
        """
        fields = {}
        where = 0
        while where < len(partial):
            split = partial.find("=", where)
            if split < 0:
                if partial.find("}", where) < 0:
                    raise Exception("Unclosed record")
            key = partial[where:split].strip()
            where = split + 1
            while where < len(partial) and partial[where] != "{":
                if not partial[where].isspace():
                    raise Exception(
                        'Unexpected character before {:',
                        partial[where])
                where += 1
            if where < len(partial):
                where += 1
            start = where
            open_braces = 0
            while where < len(partial):
                if partial[where] == "}":
                    if open_braces == 0:
                        break
                    open_braces -= 1
                elif partial[where] == "{":
                    open_braces += 1
                where += 1
            if partial[where] != "}":
                raise Exception("Missing }")
            content = partial[start:where]
            fields[key] = content.strip()
            where += 1
            while where < len(partial) and partial[where].isspace():
                where += 1
            if where < len(partial) and partial[where] == "}":
                break
            if where < len(partial) and partial[where] != ",":
                raise Exception("Unexpected character:", partial[where])
            if where < len(partial):
                where += 1
            while where < len(partial) and partial[where].isspace():
                where += 1
        return fields

    def _build_svg(self):
        """Builds an SVG for the header of a report page.

        Keyword arguments:
        number - the texh report number as a string
        title - the title of the report
        """
        number = self._fields["number"]
        title = self.websafe(self._fields["title"])
        max_length = 2160
        report_str = "Technical Report " + number
        title_length = calculateTextLength110(title)
        if title_length <= max_length:
            title_block = title_line.format(
                Report._line_y_values[2],
                title,
                title_length
            )
            return title_image_svg.format(
                report_str,
                calculateTextLength110(report_str),
                title_block
            )
        t1, t2, L = self._partition_title_2()
        if L <= max_length:
            title_block = title_line.format(
                    Report._line_y_values[1], t1, calculateTextLength110(t1)
                ) + title_line.format(
                    Report._line_y_values[2], t2, calculateTextLength110(t2)
                )
            return title_image_svg.format(
                report_str,
                calculateTextLength110(report_str),
                title_block
            )
        t1, t2, t3, L = self._partition_title_3()
        if L <= max_length:
            title_block = title_line.format(
                    Report._line_y_values[1], t1, calculateTextLength110(t1)
                ) + title_line.format(
                    Report._line_y_values[2], t2, calculateTextLength110(t2)
                ) + title_line.format(
                    Report._line_y_values[3], t3, calculateTextLength110(t3)
                )
            return title_image_svg.format(
                report_str,
                calculateTextLength110(report_str),
                title_block
            )
        t1, t2, t3, t4, L = self._partition_title_4()
        if L <= max_length:
            title_block = title_line.format(
                    Report._line_y_values[0], t1, calculateTextLength110(t1)
                ) + title_line.format(
                    Report._line_y_values[1], t2, calculateTextLength110(t2)
                ) + title_line.format(
                    Report._line_y_values[2], t3, calculateTextLength110(t3)
                ) + title_line.format(
                    Report._line_y_values[3], t4, calculateTextLength110(t4)
                )
            return title_image_svg.format(
                report_str,
                calculateTextLength110(report_str),
                title_block
            )
        t1, t2, t3, t4, t5, L = self._partition_title_5()
        if L <= max_length:
            title_block = title_line.format(
                    Report._line_y_values[0], t1, calculateTextLength110(t1)
                ) + title_line.format(
                    Report._line_y_values[1], t2, calculateTextLength110(t2)
                ) + title_line.format(
                    Report._line_y_values[2], t3, calculateTextLength110(t3)
                ) + title_line.format(
                    Report._line_y_values[3], t4, calculateTextLength110(t4)
                ) + title_line.format(
                    Report._line_y_values[4], t5, calculateTextLength110(t5)
                )
            return title_image_svg.format(
                report_str,
                calculateTextLength110(report_str),
                title_block
            )
        raise Exception("Failed to fit title on 5 lines:", title)

    def _partition_title_2(self):
        parts = self.websafe(self._fields["title"]).split()
        min_delta = 99999999
        which = 0
        for i in range(1, len(parts)-1):
            t1 = " ".join(parts[:i])
            t2 = " ".join(parts[i:])
            delta = abs(calculateTextLength110(t1) - calculateTextLength110(t2))
            if delta < min_delta:
                min_delta = delta
                which = i
        t1 = " ".join(parts[:which])
        t2 = " ".join(parts[which:])
        return t1, t2, max(calculateTextLength110(t1), calculateTextLength110(t2))

    def _partition_title_3(self):
        parts = self.websafe(self._fields["title"]).split()
        min_delta = 99999999
        which_i = 0
        which_j = 0
        the_longest = 0
        for i in range(1, len(parts)-1):
            for j in range(i+1, len(parts)-1):
                t1 = " ".join(parts[:i])
                t2 = " ".join(parts[i:j])
                t3 = " ".join(parts[j:])
                L1 = calculateTextLength110(t1)
                L2 = calculateTextLength110(t2)
                L3 = calculateTextLength110(t3)
                longest = max(L1, L2, L3)
                delta = longest - min(L1, L2, L3)
                if delta < min_delta:
                    min_delta = delta
                    which_i = i
                    which_j = j
                    the_longest = longest
        t1 = " ".join(parts[:which_i])
        t2 = " ".join(parts[which_i:which_j])
        t3 = " ".join(parts[which_j:])
        return t1, t2, t3, the_longest

    def _partition_title_4(self):
        parts = self.websafe(self._fields["title"]).split()
        min_delta = 99999999
        which_i = 0
        which_j = 0
        which_k = 0
        the_longest = 0
        for i in range(1, len(parts)-1):
            for j in range(i+1, len(parts)-1):
                for k in range(j+1, len(parts)-1):
                    t1 = " ".join(parts[:i])
                    t2 = " ".join(parts[i:j])
                    t3 = " ".join(parts[j:k])
                    t4 = " ".join(parts[k:])
                    L1 = calculateTextLength110(t1)
                    L2 = calculateTextLength110(t2)
                    L3 = calculateTextLength110(t3)
                    L4 = calculateTextLength110(t4)
                    longest = max(L1, L2, L3, L4)
                    delta = longest - min(L1, L2, L3, L4)
                    if delta < min_delta:
                        min_delta = delta
                        which_i = i
                        which_j = j
                        which_k = k
                        the_longest = longest
        t1 = " ".join(parts[:which_i])
        t2 = " ".join(parts[which_i:which_j])
        t3 = " ".join(parts[which_j:which_k])
        t4 = " ".join(parts[which_k:])
        return t1, t2, t3, t4, the_longest

    def _partition_title_5(self):
        parts = self.websafe(self._fields["title"]).split()
        min_delta = 99999999
        which_i = 0
        which_j = 0
        which_k = 0
        which_x = 0
        the_longest = 0
        for i in range(1, len(parts)-1):
            for j in range(i+1, len(parts)-1):
                for k in range(j+1, len(parts)-1):
                    for x in range(k+1, len(parts)-1):
                        t1 = " ".join(parts[:i])
                        t2 = " ".join(parts[i:j])
                        t3 = " ".join(parts[j:k])
                        t4 = " ".join(parts[k:x])
                        t5 = " ".join(parts[x:])
                        L1 = calculateTextLength110(t1)
                        L2 = calculateTextLength110(t2)
                        L3 = calculateTextLength110(t3)
                        L4 = calculateTextLength110(t4)
                        L5 = calculateTextLength110(t5)
                        longest = max(L1, L2, L3, L4, L5)
                        delta = longest - min(L1, L2, L3, L4, L5)
                        if delta < min_delta:
                            min_delta = delta
                            which_i = i
                            which_j = j
                            which_k = k
                            which_x = x
                            the_longest = longest
        t1 = " ".join(parts[:which_i])
        t2 = " ".join(parts[which_i:which_j])
        t3 = " ".join(parts[which_j:which_k])
        t4 = " ".join(parts[which_k:which_x])
        t5 = " ".join(parts[which_x:])
        return t1, t2, t3, t4, t5, the_longest

    def __str__(self):
        s = "key=" + self._key
        s += "\n" + "_first_dir=" + self._first_dir
        s += "\n" + "_seq_num=" + self._seq_num
        for key, value in self._fields.items():
            s += "\n" + key + "=" + value
        return s

    def __eq__(self, other):
        return self._key == other._key and self._fields == other._fields

    def __lt__(self, other):
        if int(self._first_dir.lstrip("0")) > int(other._first_dir.lstrip("0")):
            return True
        if int(self._first_dir.lstrip("0")) < int(other._first_dir.lstrip("0")):
            return False
        return int(self._seq_num.lstrip("0")) > int(other._seq_num.lstrip("0"))

    def __gt__(self, other):
        if int(self._first_dir.lstrip("0")) < int(other._first_dir.lstrip("0")):
            return True
        if int(self._first_dir.lstrip("0")) > int(other._first_dir.lstrip("0")):
            return False
        return int(self._seq_num.lstrip("0")) < int(other._seq_num.lstrip("0"))
