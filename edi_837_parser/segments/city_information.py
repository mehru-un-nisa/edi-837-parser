from edi_837_parser.elements.identifier import Identifier
from edi_837_parser.segments.utilities import split_segment


class City_information:
	identification = 'N4'

	identifier = Identifier()

	def __init__(self, segment: str):
		self.segment = segment
		segment = split_segment(segment)

		self.identifier = segment[0]
		self.city = segment[1]
		self.state = segment[2]
		self.zipcode = segment[3]
		

	def __repr__(self):
		return '\n'.join(str(item) for item in self.__dict__.items())


if __name__ == '__main__':
	pass
