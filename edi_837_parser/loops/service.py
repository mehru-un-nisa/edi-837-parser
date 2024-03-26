from typing import Tuple, Iterator, Optional, List
from warnings import warn

from edi_837_parser.segments.service import Service as ServiceSegment
from edi_837_parser.segments.claim import Claim as ClaimSegment
from edi_837_parser.segments.date import Date as DateSegment
from edi_837_parser.segments.reference import Reference as ReferenceSegment
from edi_837_parser.segments.amount import Amount as AmountSegment
from edi_837_parser.segments.service_adjustment import ServiceAdjustment as ServiceAdjustmentSegment
from edi_837_parser.segments.service_line_adjudication import Service_Line_Adjudication as Service_Line_AdjudicationSegment
from edi_837_parser.segments.serviceline import Serviceline as ServicelineSegment
from edi_837_parser.segments.drug_identification import Drug_Identification as Drug_IdentificationSegment
from edi_837_parser.segments.drug_quantity import Drug_Quantity as Drug_QuantitySegment

from edi_837_parser.segments.utilities import find_identifier


class Service:
	initiating_identifier = ServiceSegment.identification
	terminating_identifiers = [
		ServiceSegment.identification,
		ClaimSegment.identification,
		'HL',
		'SE'
	]

	def __init__(
			self,
			service: ServiceSegment = None,
			dates: List[DateSegment] = None,
			references: List[ReferenceSegment] = None,
			serviceline: List[ServicelineSegment] = None,
			amount: AmountSegment = None,
			adjustments: List[ServiceAdjustmentSegment] = None,
			service_line_adjudication: Service_Line_AdjudicationSegment = None,
			drug_identification:Drug_IdentificationSegment=None,
			drug_quantity:Drug_QuantitySegment=None,

	):
		self.service = service
		self.dates = dates if dates else []
		self.references = references if references else []
		self.serviceline = serviceline if serviceline else []
		self.amount = amount
		self.adjustments = adjustments if adjustments else []
		self.service_line_adjudication = service_line_adjudication 
		self.drug_identification=drug_identification
		self.drug_quantity=drug_quantity
	

	def __repr__(self):
		return '\n'.join(str(item) for item in self.__dict__.items())

	@classmethod
	def build(cls, segment: str, segments: Iterator[str]) -> Tuple['Service', Optional[str], Optional[Iterator[str]]]:
		service = Service()
		service.service = ServiceSegment(segment)

		while True:
			try:
				segment = segments.__next__()
				identifier = find_identifier(segment)

				if identifier == DateSegment.identification:
					date = DateSegment(segment)
					service.dates.append(date)

				elif identifier == ServicelineSegment.identification:
					serviceline = ServicelineSegment(segment)
					service.serviceline.append(serviceline)

				elif identifier == Service_Line_AdjudicationSegment.identification:
					service.service_line_adjudication = Service_Line_AdjudicationSegment(segment)

				elif identifier == Drug_IdentificationSegment.identification:
					di = Drug_IdentificationSegment(segment)
					service.drug_identification=di
				elif identifier == Drug_QuantitySegment.identification:
					dq = Drug_QuantitySegment(segment)
					service.drug_quantity=dq

				elif identifier == ReferenceSegment.identification:
					reference = ReferenceSegment(segment)
					service.references.append(reference)

				elif identifier == ServiceAdjustmentSegment.identification:
					service.adjustments.append(ServiceAdjustmentSegment(segment))

				elif identifier in cls.terminating_identifiers:
					return service, segment, segments

				else:
					message = f'Identifier: {identifier} not handled in service loop.'
					warn(message)

			except StopIteration:
				return service, None, None


if __name__ == '__main__':
	pass
