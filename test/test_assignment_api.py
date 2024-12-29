import unittest
import pdfplumber
from assignment_api import *
from datetime import date


class TestAssignmentApi(unittest.TestCase):
    def test_pdf_to_dict(self):
        pdf_path = "resources/chart_example.pdf"
        with pdfplumber.open(pdf_path) as pdf:
            pdf_dict = pdf_to_dict(pdf)
            # self.assertEqual(pdf_dict, {'key1': 'value1', 'key2': 'value2'})
            self.assertEqual(
                pdf_dict,
                {
                    0: [
                        TextualWord(x0=72.025, x1=95.928, text="First"),
                        TextualWord(x0=99.008, x1=128.963, text="Page:"),
                        TextualWord(x0=132.05, x1=174.873, text="Example"),
                    ],
                    1: [
                        TextualWord(x0=72.025, x1=111.955, text="Second"),
                        TextualWord(x0=115.013, x1=144.867, text="Page:"),
                        TextualWord(x0=148.05, x1=190.642, text="Example"),
                    ],
                },
            )
            
    def test_chart_population(self):
        pdf_path = "resources/chart2.pdf"
        with pdfplumber.open(pdf_path) as pdf:
            pdf_dict = pdf_to_dict(pdf)
            chart = populate_chart(pdf_dict)
            self.assertEqual(
                chart,
                Chart(name="John Doe the Second", dob=date(1971, 2, 2), has_valid_ekg=False),
            )
            today = date.today()
            self.assertEqual(chart.age, today.year - 1971 - (1 if (today.month, today.day) < (2, 2) else 0))