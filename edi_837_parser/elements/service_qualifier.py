from edi_837_parser.elements import Element
from edi_837_parser.elements.utilities import split_element


class ServiceQualifer(Element):

	def parser(self, value: str) -> str:
		value = split_element(value)
		qualifier, *_ = value
		return qualifier
