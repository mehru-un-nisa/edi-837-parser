from edi_837_parser.elements.identifier import Identifier
from edi_837_parser.elements.dollars import Dollars
from edi_837_parser.elements.adjustment_group_code import AdjustmentGroupCode
from edi_837_parser.elements.adjustment_reason_code import AdjustmentReasonCode
from edi_837_parser.segments.utilities import split_segment


class ServiceAdjustment:
	identification = 'CAS'

	identifier = Identifier()
	group_code = AdjustmentGroupCode()
	reason_code = AdjustmentReasonCode()
	amount = Dollars()

	def __init__(self, segment: str):
		self.segment = segment
		segment = split_segment(segment)
		# print(segment)
		self.identifier = segment[0]
		self.adjustment_group_code = segment[1]
		self.reason_code_amount={}
		self.reason_code_amount[(self.adjustment_group_code,segment[2])]=segment[3]
		current_reason_code = None
		for i, item in enumerate(segment):
			if item == '':
				current_reason_code = segment[i + 1]
				amount = segment[i + 2]
				self.reason_code_amount[(self.adjustment_group_code,current_reason_code)] = amount
		# print(self.reason_code_amount)


	def __repr__(self):
		return '\n'.join(str(item) for item in self.__dict__.items())


if __name__ == '__main__':
	pass
