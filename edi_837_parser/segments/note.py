from edi_837_parser.elements.identifier import Identifier
from edi_837_parser.segments.utilities import split_segment


class Note:
	identification = 'NTE'

	identifier = Identifier()


	def __init__(self, segment: str):
		self.segment = segment
		segment = split_segment(segment)
		self.identifier = segment[0]
		self.referencecode=segment[1]
		self.note_text = segment[2]

	def __repr__(self) -> str:
		return '\n'.join(str(item) for item in self.__dict__.items())



if __name__ == '__main__':
	pass
