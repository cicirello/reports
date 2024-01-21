# Site generator for https://reports.cicirello.org/
# Copyright (c) 2024 Vincent A. Cicirello. All rights reserved.
#
# This site generator is almost certainly useless to anyone other than me.
# It is highly customized to generate one specific website. Therefore, I am
# not licensing it to others. Notice the "All rights reserved" in the
# copyright notice at the top.

from templates import *
from text_length import calculateTextLength110, calculateTextLength110Weighted

class Report:
    """Metadata for a single Technical Report as extracted from a BibTeX
    record."""

    __slots__ = [
        "_raw_bibtex",
        "_key",
        "_fields",
        "_first_dir",
        "_seq_num"
        ]

    _line_y_values = [278, 449, 620, 791, 962]

    def __init__(self, report):
        """Initializes a report object.

        Keyword arguments:
        report - a BibTeX record of a Tech Report
        """
        self._raw_bibtex = report
        if report[:12].lower() != "@techreport{":
            raise Exception('BibTeX Not a TechReport')
        key_end = report.find(",", 12)
        self._key = report[12:key_end].strip()
        self._fields = self._find_fields(report[key_end+1:])
        number_components = self._fields["number"].split("-")
        self._seq_num = number_components[-1]
        self._first_dir = number_components[-2]

    def target_directory(self):
        """Returns the name of the target directory."""
        return self._first_dir + "/" + self._seq_num

    def output_bibtex_file(self):
        """Creates a bibtex file for the report."""
        with open(self._full_file(".bib"), "w") as f:
            f.write(
                bibtex_file_template.format(
                    self._fields["number"],
                    self._fields["title"],
                    self._fields["author"],
                    self._fields["year"],
                    self._fields["month"],
                    self._fields["number"],
                    self._fields["institution"],
                    url_root + self._full_file(".pdf"),
                    self._fields["abstract"]
                )
            )

    def output_svg_file(self):
        """Creates an svg file for the report."""
        with open(self._full_file(".svg"), "w") as f:
            svg = self._build_svg()
            svg = svg.replace("\n", "")
            f.write(svg)

    def _full_file(self, extension):
        """Forms the name of a file, relative to the root."""
        return self.target_directory() + "/" + self._fields["number"] + extension

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
        title = self._fields["title"]
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
        parts = self._fields["title"].split()
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
        parts = self._fields["title"].split()
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
        parts = self._fields["title"].split()
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
        parts = self._fields["title"].split()
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
        if self._first_dir.lstrip("0") > other._first_dir.lstrip("0"):
            return True
        if self._first_dir.lstrip("0") < other._first_dir.lstrip("0"):
            return False
        return self._seq_num.lstrip("0") > other._seq_num.lstrip("0")

    def __gt__(self, other):
        if self._first_dir.lstrip("0") < other._first_dir.lstrip("0"):
            return True
        if self._first_dir.lstrip("0") > other._first_dir.lstrip("0"):
            return False
        return self._seq_num.lstrip("0") < other._seq_num.lstrip("0")
