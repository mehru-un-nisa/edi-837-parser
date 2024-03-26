from edi_837_parser.elements.identifier import Identifier
from edi_837_parser.segments.utilities import split_segment


class Dept_Contact_Information:
	identification = 'PER'

	identifier = Identifier()

	def __init__(self, segment: str):
		self.segment = segment
		segment = split_segment(segment)

		self.identifier = segment[0]
		self.department = segment[2]
		if segment[3]=='TE':
			self.telephonenumber = segment[4]
		if len(segment)>5 and segment[5]=='FX':
			self.fxnumber = segment[6]
		else:
			self.fxnumber=None
		

	def __repr__(self):
		return '\n'.join(str(item) for item in self.__dict__.items())


if __name__ == '__main__':
	pass
