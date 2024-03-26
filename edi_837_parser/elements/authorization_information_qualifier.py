from typing import Optional

from edi_837_parser.elements import Element


class AuthorizationInformationQualifier(Element):

	def parser(self, value: str) -> Optional[str]:
		if value == '00':
			value = None

		return value
