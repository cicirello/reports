# Site generator for https://reports.cicirello.org/
# Copyright (c) 2024 Vincent A. Cicirello. All rights reserved.
#
# This site generator is almost certainly useless to anyone other than me.
# It is highly customized to generate one specific website. Therefore, I am
# not licensing it to others. Notice the "All rights reserved" in the
# copyright notice at the top.

import os
from report import Report
from page import PageBuilder

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
                    reports.append(Report("".join(current).strip()))
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

def make_bib_files(reports):
    """Creates BibTeX files for all of the reports.

    Keyword arguments:
    reports - An iterable of Report objects
    """
    for r in reports:
        r.output_bibtex_file()

def make_svg_files(reports):
    """Creates svg files for all of the reports.

    Keyword arguments:
    reports - An iterable of Report objects
    """
    for r in reports:
        r.output_svg_file()

def make_web_pages(builder, reports):
    """Creates abstract pages for all of the reports.

    Keyword arguments:
    builder - the PageBuilder
    reports - An iterable of Report objects
    """
    for r in reports:
        with open(r.target_directory() + "/index.html", "w") as f:
            f.write(builder.build_report_page(r))

def main():
    reports = load_bib_file()
    reports.sort()
    make_dirs(reports)
    make_bib_files(reports)
    make_svg_files(reports)
    builder = PageBuilder()
    make_web_pages(builder, reports)

if __name__ == "__main__":
    #main()
    reports = load_bib_file()
    reports.sort()
    builder = PageBuilder()
    print(builder.build_home_page(reports))
    
    