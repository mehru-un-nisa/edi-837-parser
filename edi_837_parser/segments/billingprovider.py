from edi_837_parser.elements.identifier import Identifier
from edi_837_parser.segments.utilities import split_segment


class Billingprovider:
	identification='PRV'

	identifier = Identifier()
	taxonomy_code = ''

	def __init__(self, segment: str):
		self.segment = segment
		segment = split_segment(segment)

		self.identifier = segment[0]
		self.type=segment[1]
		if segment[2]=='PXC':
			self.taxonomy_code = segment[3]
		else:
			self.taxonomy_code = None


	def __repr__(self):
		return '\n'.join(str(item) for item in self.__dict__.items())


if __name__ == '__main__':
	pass
