from edi_837_parser.elements.identifier import Identifier
from edi_837_parser.elements.dollars import Dollars
from edi_837_parser.elements.service_code import ServiceCode
from edi_837_parser.elements.service_qualifier import ServiceQualifer
from edi_837_parser.elements.service_modifier import ServiceModifier
from edi_837_parser.elements.integer import Integer
from edi_837_parser.segments.utilities import split_segment, get_element


class Service:
	identification = 'LX'

	identifier = Identifier()
	assigned_number = Integer()

	def __init__(self, segment: str):
		self.segment = segment
		segment = split_segment(segment)

		self.identifier = segment[0]
		self.assigned_number = segment[1]

	def __repr__(self):
		return '\n'.join(str(item) for item in self.__dict__.items())


if __name__ == '__main__':
	pass
