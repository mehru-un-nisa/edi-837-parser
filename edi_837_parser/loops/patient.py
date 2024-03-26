from typing import Iterator, Tuple, Optional, List
from warnings import warn
from edi_837_parser.segments.claim import Claim as ClaimSegment
from edi_837_parser.segments.patient import Patient as PatientSegment
from edi_837_parser.segments.entity import Entity as EntitySegment
from edi_837_parser.segments.date import Date as DateSegment
from edi_837_parser.segments.address import Address as AddressSegment
from edi_837_parser.segments.city_information import City_information as City_informationSegment
from edi_837_parser.segments.demographic_information import Demographic_information as Demographic_informationSegment


from edi_837_parser.segments.utilities import find_identifier


class Patient:
	initiating_identifier = PatientSegment.identification
	terminating_identifiers = [
		ClaimSegment.identification,
		PatientSegment.identification,
		'SE'
	]

	def __init__(
			self,
			patient: PatientSegment = None,
			entities: List[EntitySegment] = None,
			dates: List[DateSegment] = None,
			address:List[AddressSegment]=None,
			city_information:List[City_informationSegment]=None,
			demographic_information:Demographic_informationSegment=None,

	):
		self.patient = patient
		self.entities = entities if entities else []
		self.dates = dates if dates else []
		self.address = address if address else []
		self.demographic_information=demographic_information
		self.city_information = city_information if city_information else []

	def __repr__(self):
		return '\n'.join(str(item) for item in self.__dict__.items())



	@classmethod
	def build(cls, segment: str, segments: Iterator[str]) -> Tuple['Patient', Optional[Iterator[str]], Optional[str]]:
		patient = Patient()
		patient.patient = PatientSegment(segment)

		segment = segments.__next__()
		while True:
			# print(segment)
			try:
				if segment is None:
					segment = segments.__next__()

				identifier = find_identifier(segment)
				# print(identifier)
				if identifier == EntitySegment.identification:
					entity = EntitySegment(segment)
					patient.entities.append(entity)
					segment = None

				elif identifier == DateSegment.identification:
					date = DateSegment(segment)
					patient.dates.append(date)
					segment = None

				elif identifier in cls.terminating_identifiers:
					return patient, segments, segment
				
				elif identifier == AddressSegment.identification:
					address = AddressSegment(segment)
					patient.address.append(address)
					segment = None
				elif identifier == City_informationSegment.identification:
					city_information = City_informationSegment(segment)
					patient.city_information.append(city_information)
					segment = None

				elif identifier == Demographic_informationSegment.identification:
					demographic_information = Demographic_informationSegment(segment)
					patient.demographic_information=demographic_information
					segment = None

				else:
					segment = None
					message = f'Identifier: {identifier} not handled in patientloop.'
					# warn(message)

			except StopIteration:
				return patient, None, None
