from edi_837_parser.elements.identifier import Identifier
from edi_837_parser.elements.dollars import Dollars
from edi_837_parser.segments.utilities import split_segment


class Drug_Identification:
	identification = 'LIN'

	identifier = Identifier()

	def __init__(self, segment: str):
		self.segment = segment
		segment = split_segment(segment)

		self.identifier = segment[0]
		self.qualifier = segment[2]
		self.national_drug_code=segment[3]

	def __repr__(self):
		return '\n'.join(str(item) for item in self.__dict__.items())


if __name__ == '__main__':
	pass
