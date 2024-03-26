from edi_837_parser.elements.identifier import Identifier
from edi_837_parser.segments.utilities import split_segment


class Subscriber:
	identification = 'SBR'

	identifier = Identifier()


	def __init__(self, segment: str):
		self.segment = segment
		segment = split_segment(segment)
		self.identifier = segment[0]
		self.sequencecode=segment[1]
		self.ppolicynumber = segment[2]
		self.filingindicator = segment[3]

	def __repr__(self) -> str:
		return '\n'.join(str(item) for item in self.__dict__.items())



if __name__ == '__main__':
	pass
