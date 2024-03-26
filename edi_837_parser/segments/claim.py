from edi_837_parser.elements.identifier import Identifier
from edi_837_parser.elements.claim_status import ClaimStatus
from edi_837_parser.elements.dollars import Dollars
from edi_837_parser.segments.utilities import split_segment


class Claim:
	identification = 'CLM'

	identifier = Identifier()
	status = ClaimStatus()
	charge_amount = Dollars()
	paid_amount = Dollars()

	def __init__(self, segment: str):
		self.segment = segment
		segment = split_segment(segment)
		# print(segment)
		self.identifier = segment[0]
		self.marker = segment[1]
		self.charge_amount = segment[2]
		self.status = segment[3]
		self.paid_amount = segment[4]
		
		

	def __repr__(self):
		return '\n'.join(str(item) for item in self.__dict__.items())


if __name__ == '__main__':
	pass
