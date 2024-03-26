from typing import Optional

from edi_837_parser.elements import Element


class Dollars(Element):

	def parser(self, value: str) -> Optional[float]:
		if value != '':
			return float(value)
