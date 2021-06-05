from rest_framework.parsers import BaseParser
import io
import csv
import re


class CSVTextParser(BaseParser):
    """
    Custom CSV text parser.
    """

    media_type = 'text/csv'

    def parse(self, stream, media_type, parser_context):
        form = re.match("charset=([\w\W]*)", media_type)
        if form is None:
            form = "utf-8"
        csv_reader = csv.reader(io.StringIO(stream.read().decode("utf-8")))
        ans = []
        for row in csv_reader:
            ans.append(row)
        return ans
