from typing import List, Dict
from dataclasses import dataclass
import pdfplumber
from pdfplumber.page import Page


@dataclass
class TextualWord:
    x0: float
    x1: float
    text: str


@dataclass
class ExtraTextualWord(TextualWord):
    fontname: str
    size: float

    @property
    def is_bold(self) -> bool:
        return "Bold" in self.fontname


PagesToWords = Dict[int, List[TextualWord]]
PagesToExtraWords = Dict[int, List[ExtraTextualWord]]


def extract_extra_words_from_page(page: Page) -> List[ExtraTextualWord]:
    return [
        ExtraTextualWord(
            round(word["x0"], 3),
            round(word["x1"], 3),
            word["text"],
            word["fontname"],
            word["size"],
        )
        for word in page.extract_words(extra_attrs=("fontname", "size"))
    ]

# HOTFIX: no time to make pdf_to_dict rely on pdf_to_extra_dict
def extract_words_from_page(page: Page) -> List[TextualWord]:
    return [
        TextualWord(
            round(word["x0"], 3),
            round(word["x1"], 3),
            word["text"],
        )
        for word in page.extract_words()
    ]


def pdf_to_extra_dict(pdfplumber_pdf: pdfplumber.PDF) -> PagesToExtraWords:
    return {
        i: extract_extra_words_from_page(page) for i, page in enumerate(pdfplumber_pdf.pages)
    }


def pdf_to_dict(pdfplumber_pdf: pdfplumber.PDF) -> PagesToWords:
    return {
        i: extract_words_from_page(page) for i, page in enumerate(pdfplumber_pdf.pages)
    }
