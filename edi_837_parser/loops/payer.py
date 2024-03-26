from typing import Iterator, Tuple, Optional, List
from warnings import warn
from edi_837_parser.segments.claim import Claim as ClaimSegment
from edi_837_parser.segments.subscriber import Subscriber as SubscriberSegment
from edi_837_parser.segments.entity import Entity as EntitySegment
from edi_837_parser.segments.address import Address as AddressSegment
from edi_837_parser.segments.reference import Reference as ReferenceSegment

from edi_837_parser.segments.city_information import City_information as City_informationSegment
from edi_837_parser.segments.demographic_information import Demographic_information as Demographic_informationSegment
from edi_837_parser.segments.dept_contact_information import Dept_Contact_Information as Dept_Contact_InformationSegment



from edi_837_parser.segments.date import Date as DateSegment
from edi_837_parser.segments.utilities import find_identifier


class Payer:
	initiating_identifier = EntitySegment.identification
	terminating_identifiers = [
		EntitySegment.identification,
		ClaimSegment.identification,
		'SBR',
		'LX',
		'HL',
		'SE'
	]

	def __init__(
			self,
			tag=None,
			entities: EntitySegment= None,
			address:AddressSegment =None,
			city_information:City_informationSegment=None,
			demographic_information:Demographic_informationSegment=None,
			dept_contact_information:Dept_Contact_InformationSegment=None,
			dates:List[DateSegment]=None,
			references: List[ReferenceSegment] = None,

	):
	
		self.entities = entities 
		self.address = address 
		self.city_information = city_information 
		self.demographic_information = demographic_information
		self.dept_contact_information = dept_contact_information
		self.tag=tag
		self.dates=dates if dates else []
		self.references= references if references else []
		

	def __repr__(self):
		return '\n'.join(str(item) for item in self.__dict__.items())



	@classmethod
	def build(cls, segment: str, segments: Iterator[str]) -> Tuple['Payer', Optional[Iterator[str]], Optional[str]]:
		payer = Payer()
		
		payer.entities = EntitySegment(segment)
		# print(payer.entities )
		if payer.entities.entity=='PR':
			payer.tag='payer'
		elif payer.entities.entity=='IL':
			payer.tag='subscriber'
		
		segment = segments.__next__()
		while True:
			try:
				if segment is None:
					segment = segments.__next__()
		
				identifier = find_identifier(segment)

				if identifier == AddressSegment.identification:
					address = AddressSegment(segment)
					payer.address=address
					segment = None
				elif identifier == City_informationSegment.identification:
					city_info = City_informationSegment(segment)
					payer.city_information=city_info
					segment = None
				elif identifier == Demographic_informationSegment.identification:
					demo_info = Demographic_informationSegment(segment)
					payer.demographic_information=demo_info
					segment = None
				elif identifier == Dept_Contact_InformationSegment.identification:
					dept_info = Dept_Contact_InformationSegment(segment)
					payer.dept_contact_information=dept_info
					segment = None

				elif identifier == DateSegment.identification:
					dt = DateSegment(segment)
					payer.dates.append(dt)
					segment = None

				elif identifier == ReferenceSegment.identification:
					reference = ReferenceSegment(segment)
					payer.references.append(reference)
					segment = None

				elif identifier in cls.terminating_identifiers:
			
					return payer, segments, segment

				else:
					if identifier=='DTP':
						print(payer.entities.segment)
						print('seg',segment)
					segment = None
					message = f'Identifier: {identifier} not handled in payerloop.'
					warn(message)

			except StopIteration:
				return payer, None, None
