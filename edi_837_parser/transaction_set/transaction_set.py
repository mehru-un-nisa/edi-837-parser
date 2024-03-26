from typing import List, Iterator, Optional
from collections import namedtuple
import pandas as pd
from edi_837_parser.loops.claim import Claim as ClaimLoop
from edi_837_parser.loops.service import Service as ServiceLoop
from edi_837_parser.segments.utilities import find_identifier,split_segment
from edi_837_parser.loops.patient import Patient as PatientLoop
from edi_837_parser.loops.billingprovider import Billingprovider as BillingproviderLoop
from edi_837_parser.loops.subscriber import Subscriber as SubscriberLoop
from edi_837_parser.loops.payer import Payer as PayerLoop

BuildAttributeResponse = namedtuple('BuildAttributeResponse', 'key value segment segments')


class TransactionSet:

	def __init__(
			self,
			claims: List[ClaimLoop],
			file_path: str,
			patient:PatientLoop,
			billingprovider:BillingproviderLoop,
			subscriber:SubscriberLoop,
	):
		self.claims = claims
		self.file_path = file_path
		self.patient=patient
		self.billingprovider=billingprovider
		self.subscriber=subscriber

	def __repr__(self):
		return '\n'.join(str(item) for item in self.__dict__.items())


	def to_dataframe(self) -> pd.DataFrame:
		"""flatten the remittance advice by service to a pandas DataFrame"""
		data = []
		# print("hello")
		# print(self.claims[0])
		cl=None
		# print("length",len(self.patient))
		for claim in self.claims:
			for service in claim.services:
				datum = TransactionSet.serialize_service(
					claim,
					service,
					self.patient,
					self.billingprovider
					
			)
				
				# for index, adjustment in enumerate(service.adjustments):
				# 	datum[f'adj_{index}_group'] = adjustment.group_code.code
				# 	datum[f'adj_{index}_code'] = adjustment.reason_code.code
				# 	datum[f'adj_{index}_amount'] = adjustment.amount

				for index, reference in enumerate(service.references):
					datum[f'ref_{index}_qual'] = reference.qualifier.code
					datum[f'ref_{index}_value'] = reference.value

				# for index, remark in enumerate(service.remarks):
				# 	datum[f'rem_{index}_qual'] = remark.qualifier.code
				# 	datum[f'rem_{index}_code'] = remark.code.code

				data.append(datum)
		
	
		return pd.DataFrame(data)

	@staticmethod
	def serialize_service(
			claim: ClaimLoop,
			service: ServiceLoop,
			patient:PatientLoop,
			billingprovider:BillingproviderLoop
	) -> dict:
		# if the service doesn't have a start date assume the service and claim dates match
		servicedate = None
		if service:
			if service.dates and service.dates[0].qualifier=='service':
			
				servicedate = service.dates[0].date

		# if the service doesn't have an end date assume the service and claim dates match
		service_chargeamount = None
		if service:
			if service.serviceline:
				service_chargeamount = service.serviceline[0].chargeamount

		attendingprovider_fname=''
		attendingprovider_lname=''
		attendingprovider_identifier=''
		billingprovider_name=''
		billingprovider_identfication_code=''
		subscriber_amount={}

		for entity in claim.entities:
			
			if entity.entity=='71':
				# print('hi')
				
				attendingprovider_fname=entity.first_name
				attendingprovider_lname=entity.last_name
				attendingprovider_identifier=entity.identification_code

		for nm in claim.billingprovider.entities:
			if nm.entity=='billing provider':
				billingprovider_name=nm.last_name
				billingprovider_identfication_code=nm.identification_code

		diagnosis_codes = []

		# Iterate over each object in claim.diagnosis list
		if claim.diagnosis:
			for diagnosis_obj in claim.diagnosis:
				# Extract diagnosis codes list from the current object and concatenate it with all_diagnosis_codes
				diagnosis_codes.extend(diagnosis_obj.diagnosis_codes)
		adjustments={}
		if claim.subscriber_other:
			for adj in claim.subscriber_other.adjustments:
				dictionary=adj.reason_code_amount
				adjustments = {**adjustments, **dictionary}
		
		if claim.subscriber_other:
			if len(claim.subscriber_other.amount)>0:
				for amt in claim.subscriber_other.amount:
					subscriber_amount[amt.qualifier]=amt.amount
		

		datum = {
			'claim_id': claim.claim.marker,
		
			'patient_firstname': claim.patient.entities[0].first_name,
			'patient_lastname': claim.patient.entities[0].last_name,
			'patient_firstname': claim.patient.entities[0].first_name,
			'patient_dob': claim.patient.demographic_information.date,
			'patient_gender': claim.patient.demographic_information.gender_code,

			'patient_address': claim.patient.address[0].address,
			'patient_city': claim.patient.city_information[0].city,
			'patient_state': claim.patient.city_information[0].state,
			'patient_zipcode': claim.patient.city_information[0].zipcode,

			# 'patient': claim.patient.name,
			'service_date': servicedate,
			'service_chargeamount': service_chargeamount,
			'service_revenue_code':service.serviceline[0].revenuecode,
			'service_procedure_code':service.serviceline[0].procedurecode,
			'service_measurement_code':service.serviceline[0].measurementcode,
			'service_units':service.serviceline[0].unitdays,
			'drug_identification_code':service.drug_identification.national_drug_code if service.drug_identification else None,
			'drug_quantity': service.drug_quantity.drug_unit +" "+service.drug_quantity.meas_code  if service.drug_quantity else None,
			'note':claim.note.note_text if claim.note else None,

			'paid_amount': claim.claim.paid_amount,
			'rendering_provider': claim.rendering_provider.name if claim.rendering_provider else None,
			'payer_classification': str(claim.claim.status.payer_classification),
			'diagnosis':diagnosis_codes,
			'adjustments':adjustments,
			'attending_provider_firstname':attendingprovider_fname,
			'attending_provider_lastname':attendingprovider_lname,
			'attending_provider_identifier':attendingprovider_identifier,
			'attending_provider_taxonomy_code':claim.attending_provider_taxonomy.taxonomy_code if claim.attending_provider_taxonomy else None,
			'service_facility_location': claim.service_facility_location.entities.last_name if claim.service_facility_location and claim.service_facility_location.entities is not None else None,
			'service_facility_location_address':claim.service_facility_location.address.address if claim.service_facility_location and claim.service_facility_location.address is not None else None,
			'service_facility_location_city':claim.service_facility_location.city_information.city if claim.service_facility_location and claim.service_facility_location.city_information is not None else None,
			'service_facility_location_state':claim.service_facility_location.city_information.state if claim.service_facility_location and claim.service_facility_location.city_information is not None else None,
			'service_facility_location_zipcode':claim.service_facility_location.city_information.zipcode if claim.service_facility_location and claim.service_facility_location.city_information is not None else None,
			'submiiter_name':claim.submitter.entities.last_name if claim.submitter.entities else None,
			'submiiter_identifier':claim.submitter.entities.identification_code if claim.submitter.entities is not None else None,
			'submiiter_dept_telephone':claim.submitter.dept_contact_information.telephonenumber if claim.submitter.dept_contact_information is not None else None,
			'submiiter_dept_fx':claim.submitter.dept_contact_information.fxnumber if claim.submitter.dept_contact_information is not None else None,
			'receiver_name':claim.receiver.entities.last_name if claim.receiver.entities else None,
			'receiver_identifier':claim.receiver.entities.identification_code if claim.receiver.entities is not None else None,
			'billingprovider_name':billingprovider_name,
			'billingprovider_identfication_code':billingprovider_identfication_code,
			'billingprovider_taxonomy_code':claim.billingprovider.billingprovider.taxonomy_code,
			'billingprovider_dept_telephone':claim.billingprovider.dept_contact_information.telephonenumber,
			'billingprovider_dept_fx':claim.billingprovider.dept_contact_information.fxnumber,
			'billing_provider_city':claim.billingprovider.city_information[0].city,
			'billing_provider_state':claim.billingprovider.city_information[0].state,
			'billing_provider_zipcode':claim.billingprovider.city_information[0].zipcode,
			'billing_provider_address':claim.billingprovider.address[0].address,
			'subscriber(other)_first_name':claim.subscriber_other.payer[0].entities.first_name if (claim.subscriber_other and claim.subscriber_other.payer[0].tag=='subscriber') else None,
			'subscriber(other)_last_name':claim.subscriber_other.payer[0].entities.last_name if claim.subscriber_other and claim.subscriber_other.payer[0].tag=='subscriber' else None,
			'subscriber(other)_identification_code':claim.subscriber_other.payer[0].entities.identification_code if (claim.subscriber_other and claim.subscriber_other.payer[0].tag=='subscriber') else None,
			'subscriber(other)_address':claim.subscriber_other.payer[0].address.address if (claim.subscriber_other and claim.subscriber_other.payer[0].tag=='subscriber' and claim.subscriber_other.payer[0].address is not None) else None,
			'subscriber(other)_city':claim.subscriber_other.payer[0].city_information.city if (claim.subscriber_other and claim.subscriber_other.payer[0].tag=='subscriber' and claim.subscriber_other.payer[0].city_information is not None) else None,
			'subscriber(other)_state':claim.subscriber_other.payer[0].city_information.state if (claim.subscriber_other and claim.subscriber_other.payer[0].tag=='subscriber' and claim.subscriber_other.payer[0].city_information is not None) else None,
			'subscriber(other)_zipcode':claim.subscriber_other.payer[0].city_information.zipcode if (claim.subscriber_other and claim.subscriber_other.payer[0].tag=='subscriber' and claim.subscriber_other.payer[0].city_information is not None) else None,
			'subscriber(other)_amount':subscriber_amount ,
			'payer(other)_name':claim.subscriber_other.payer[1].entities.last_name  if (claim.subscriber_other and claim.subscriber_other.payer[1].tag=='payer') else None,
			'payer(other)_identification_code':claim.subscriber_other.payer[1].entities.identification_code if (claim.subscriber_other and claim.subscriber_other.payer[1].tag=='payer') else None,
			'payer(other)_address':claim.subscriber_other.payer[1].address.address if (claim.subscriber_other and claim.subscriber_other.payer[1].tag=='payer' and claim.subscriber_other.payer[1].address is not None) else None,
			'payer(other)_city':claim.subscriber_other.payer[1].city_information.city if (claim.subscriber_other and claim.subscriber_other.payer[1].tag=='payer' and claim.subscriber_other.payer[1].city_information is not None) else None,
			'payer(other)_state':claim.subscriber_other.payer[1].city_information.state if (claim.subscriber_other and claim.subscriber_other.payer[1].tag=='payer' and claim.subscriber_other.payer[1].city_information is not None) else None,
			'payer(other)_zipcode':claim.subscriber_other.payer[1].city_information.zipcode if (claim.subscriber_other and claim.subscriber_other.payer[1].tag=='payer' and claim.subscriber_other.payer[1].city_information is not None) else None


		}

		return datum

	@classmethod
	def build(cls, file_path: str) -> 'TransactionSet':
		claims = []
		organizations = []
		patient=[]
		billingprovider=[]
		subscriber=[]



		with open(file_path) as f:
			file = f.read()
		
		segments = file.split('~')
		segments = [segment.strip() for segment in segments]
		
		segments = iter(segments)
		segment = None
		pat=PatientLoop()
		bp=BillingproviderLoop()
		sub=SubscriberLoop()
		submit=PayerLoop()
		receive=PayerLoop()


		while True:
			response = cls.build_attribute(segment, segments)
			
			segment = response.segment
			segments = response.segments

			# no more segments to parse
			if response.segments is None:
				break

			if response.key == 'interchange':
				interchange = response.value

			if response.key == 'financial information':
				financial_information = response.value

			if response.key == 'organization':
				organizations.append(response.value)

			if response.key == 'claim':
	
				response.value.patient=pat
				response.value.billingprovider=bp
				response.value.subscriber=sub
				response.value.submitter=submit
				response.value.receiver=receive

				claims.append(response.value)
			if response.key == 'patient':
				patient.append(response.value)
				pat=response.value
			if response.key == 'billingprovider':
			
				billingprovider.append(response.value)
				bp=response.value
				
			if response.key == 'subscriber':
	
				subscriber.append(response.value)
				sub=response.value
			
			if response.key == 'submitter':
				submit=response.value

			if response.key == 'receiver':
				receive=response.value
	


		
		return TransactionSet(claims, file_path,patient,billingprovider,subscriber)

	@classmethod
	def build_attribute(cls, segment: Optional[str], segments: Iterator[str]) -> BuildAttributeResponse:
		if segment is None:
			try:
				segment = segments.__next__()
			except StopIteration:
				return BuildAttributeResponse(None, None, None, None)
		
		identifier = find_identifier(segment)
		identifier2=split_segment(segment)
		
		if identifier == PatientLoop.initiating_identifier:
			patient, segments, segment = PatientLoop.build(segment, segments)
	
			
			return BuildAttributeResponse('patient', patient, segment, segments)
		
		elif identifier == ClaimLoop.initiating_identifier:
	
			claim, segments, segment = ClaimLoop.build(segment, segments)
			
			return BuildAttributeResponse('claim', claim, segment, segments)
		
		elif identifier == SubscriberLoop.initiating_identifier:
			subscriber, segments, segment = SubscriberLoop.build(segment, segments)
			
			return BuildAttributeResponse('subscriber', subscriber, segment, segments)
		
		elif (identifier2[0]== BillingproviderLoop.initiating_identifier and identifier2[1] == 'BI' ):
			billingprovider, segments, segment = BillingproviderLoop.build(segment, segments)
			
			return BuildAttributeResponse('billingprovider', billingprovider, segment, segments)
		elif (identifier2[0]== PayerLoop.initiating_identifier and identifier2[1] == '41' ):
			submitter, segments, segment = PayerLoop.build(segment, segments)
			
			return BuildAttributeResponse('submitter', submitter, segment, segments)
		
		elif (identifier2[0]== PayerLoop.initiating_identifier and identifier2[1] == '40' ):
			receiver, segments, segment = PayerLoop.build(segment, segments)
			
			return BuildAttributeResponse('receiver', receiver, segment, segments)

		else:
			return BuildAttributeResponse(None, None, None, segments)


if __name__ == '__main__':
	pass