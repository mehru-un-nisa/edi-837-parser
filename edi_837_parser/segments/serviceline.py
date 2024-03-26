from edi_837_parser.elements.identifier import Identifier
from edi_837_parser.segments.utilities import split_segment


class Serviceline:
	identification = 'SV2'

	identifier = Identifier()


	def __init__(self, segment: str):
		self.segment = segment
		segment = split_segment(segment)
		self.identifier = segment[0]
		self.revenuecode=segment[1]
		self.procedurecode = segment[2]
		self.chargeamount = segment[3]
		self.measurementcode = segment[4]
		self.unitdays = segment[5]
		

	def __repr__(self) -> str:
		return '\n'.join(str(item) for item in self.__dict__.items())



if __name__ == '__main__':
	pass
