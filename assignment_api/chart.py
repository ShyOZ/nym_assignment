from datetime import date, datetime
from dataclasses import dataclass
from io import StringIO
from .text import PagesToWords


@dataclass
class Chart:
    name: str
    dob: date
    has_valid_ekg: bool

    @property
    def age(self) -> float:
        today = date.today()
        return round(
            today.year
            - self.dob.year
            - (1 if (today.month, today.day) < (self.dob.month, self.dob.day) else 0),
            2,
        )


def populate_chart(page_to_words: PagesToWords) -> Chart:
    page = page_to_words[0]

    i = 0
    while i < len(page):
        if page[i].text.lower() == "name:":
            break
        i += 1
    i += 1

    name_builder = StringIO()
    while i < len(page):
        if page[i].text.lower() == "dob:":
            break
        name_builder.write(page[i].text)
        name_builder.write(" ")
        i += 1
    i += 1

    name = name_builder.getvalue().strip()
    dob = datetime.strptime(page[i].text, "%d/%m/%Y").date()

    while i < len(page):
        if page[i - 1].text.lower() == "ekg" and page[i].text.lower() == "results":
            break
        i += 1
    i += 1

    has_valid_ekg = (page[i].text.lower() == "valid") and not (
        page[i - 4].text.lower() == "no" and page[i - 3].text.lower() == "valid"
    )
    return Chart(name, dob, has_valid_ekg)