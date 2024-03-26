from edi_837_parser.elements.identifier import Identifier
from edi_837_parser.elements.dollars import Dollars
from edi_837_parser.segments.utilities import split_segment


class Drug_Quantity:
	identification = 'CTP'

	identifier = Identifier()

	def __init__(self, segment: str):
		self.segment = segment
		segment = split_segment(segment)

		self.identifier = segment[0]
		self.drug_unit = segment[4]
		self.meas_code=segment[5]

	def __repr__(self):
		return '\n'.join(str(item) for item in self.__dict__.items())


if __name__ == '__main__':
	pass
