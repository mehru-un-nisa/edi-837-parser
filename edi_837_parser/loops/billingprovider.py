from typing import Iterator, Tuple, Optional, List
from warnings import warn
from edi_837_parser.segments.claim import Claim as ClaimSegment
from edi_837_parser.segments.billingprovider import Billingprovider as BillingproviderSegment
from edi_837_parser.segments.entity import Entity as EntitySegment
from edi_837_parser.segments.date import Date as DateSegment
from edi_837_parser.segments.address import Address as AddressSegment
from edi_837_parser.segments.city_information import City_information as city_informationSegment
from edi_837_parser.segments.dept_contact_information import Dept_Contact_Information as dept_contact_informationSegment



from edi_837_parser.segments.utilities import find_identifier


class Billingprovider:
	initiating_identifier = BillingproviderSegment.identification
	terminating_identifiers = [
		'HL',
		BillingproviderSegment.identification,
		'SBR',
		'LX',
		'SE'
	]

	def __init__(
			self,
			billingprovider: BillingproviderSegment = None,
			entities: List[EntitySegment] = None,
			dates: List[DateSegment] = None,
			address:List[AddressSegment]=None,
			city_information:List[city_informationSegment]=None,
			dept_contact_information:dept_contact_informationSegment=None,


	):
		self.billingprovider = billingprovider
		self.address = address if address else []
		self.city_information = city_information if city_information else []
		self.entities = entities if entities else []
		self.dates = dates if dates else []
		self.dept_contact_information=dept_contact_information


	def __repr__(self):
		return '\n'.join(str(item) for item in self.__dict__.items())



	@classmethod
	def build(cls, segment: str, segments: Iterator[str]) -> Tuple['Billingprovider', Optional[Iterator[str]], Optional[str]]:
		billingprovider = Billingprovider()
		billingprovider.billingprovider = BillingproviderSegment(segment)

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
					billingprovider.entities.append(entity)
					segment = None

				elif identifier == DateSegment.identification:
					date = DateSegment(segment)
					billingprovider.dates.append(date)
					segment = None

				elif identifier == AddressSegment.identification:
					address = AddressSegment(segment)
					billingprovider.address.append(address)
					segment = None
				elif identifier == city_informationSegment.identification:
					city_information = city_informationSegment(segment)
					billingprovider.city_information.append(city_information)
					segment = None

				elif identifier == dept_contact_informationSegment.identification:
					dept_contact_information = dept_contact_informationSegment(segment)
					billingprovider.dept_contact_information=dept_contact_information
					segment = None

				elif identifier in cls.terminating_identifiers:
					return billingprovider, segments, segment

				else:
					segment = None
					message = f'Identifier: {identifier} not handled in billingprovider loop.'
					# warn(message)

			except StopIteration:
				return billingprovider, None, None
