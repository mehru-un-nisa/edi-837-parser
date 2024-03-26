from edi_837_parser.elements.identifier import Identifier
from edi_837_parser.elements.dollars import Dollars
from edi_837_parser.segments.utilities import split_segment


class Service_Line_Adjudication:
	identification = 'SVD'

	identifier = Identifier()
	# qualifier = AmountQualifier()
	service_line_paid_amount = Dollars()

	def __init__(self, segment: str):
		self.segment = segment
		segment = split_segment(segment)

		self.identifier = segment[0]
		self.identification_code = segment[1]
		self.service_line_paid_amount=segment[2]
		self.procedure_code=segment[3]
		self.description=segment[4]
		self.unit_count = segment[5]

	def __repr__(self):
		return '\n'.join(str(item) for item in self.__dict__.items())


if __name__ == '__main__':
	pass
