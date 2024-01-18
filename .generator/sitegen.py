# Site generator for https://reports.cicirello.org/
# Copyright (c) 2024 Vincent A. Cicirello. All rights reserved.
#
# This site generator is almost certainly useless to anyone other than me.
# It is highly customized to generate one specific website. Therefore, I am
# not licensing it to others. Notice the "All rights reserved" in the
# copyright notice at the top.

import os

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

def load_bib_file(bib_file="reports.bib"):
    """LaTeX bib file with BibTeX for the reports, including the abstracts.

    Keyword arguments:
    bib_file - the BibTeX file.
    """
    reports = []
    with open(bib_file, "r") as bib:
        current = []
        for line in bib:
            if line.startswith("@techreport"):
                if len(current) > 0:
                    reports.append(Report("\n".join(current).strip()))
                    current = []
            current.append(line)
        reports.append(Report("".join(current).strip()))
    return reports

def make_dirs(reports):
    """Create any directories that we need that don't already exist.

    Keyword arguments:
    reports - An iterable of Report objects
    """
    for r in reports:
        directory = r.target_directory()
        if not os.path.isdir(directory):
            os.makedirs(directory)

def main():
    reports = load_bib_file()
    reports.sort()
    make_dirs(reports)

if __name__ == "__main__":
    main()
