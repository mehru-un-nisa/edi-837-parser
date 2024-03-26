from edi_837_parser.elements.identifier import Identifier
from edi_837_parser.segments.utilities import split_segment


class Patient:
	identification = 'PAT'
	print("hi pat")
	identifier = Identifier()
	relationship_code = ''

	def __init__(self, segment: str):
		self.segment = segment
		segment = split_segment(segment)
	

		self.identifier = segment[0]
		self.relationship_code = segment[1]

	def __repr__(self):
		return '\n'.join(str(item) for item in self.__dict__.items())


if __name__ == '__main__':
	pass
