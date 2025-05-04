"""
Module to generate unsigned certificate data.

This module defines the UnsignedCertGenerator class, which is responsible for generating
the data required for creating unsigned certificates.
"""

import json
from typing import Any, Dict, Optional

from unsigned_generator.constants import (
    EVERYCRED_CREDENTIAL_V1_CONTEXT,
    URN_UUID_PREFIX,
    VERIFIABLE_CREDENTIAL_V2_CONTEXT
)
from unsigned_generator.schema import Issuer, Subject


class UnsignedCertGenerator:
    """
    Class to generate unsigned certificate data.

    Methods:
        generate_unsigned_cert_data: Generate the dictionary of data required for
        generating unsigned certificates.
        _create_base_template: Create the base template for unsigned certificate data.
    """

    def generate_unsigned_cert_data(
        self,
        issuer: Issuer,
        subject: Subject,
        records_json: str,
        issuer_image: str,
        subject_image: str,
        additional_global_fields: Dict[str, Any],
        app_name: str,
        recipient_fields: Dict[str, Any],
        valid_from: Optional[str] = None,
        valid_until: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Generate the dictionary of data required for generating unsigned certificates.

        This function constructs a dictionary containing various parameters needed for generating
        unsigned certificates. It takes issuer and subject information, certificate data, and
        additional fields as input and creates the required data structure.

        Args:
            issuer (Issuer): An object representing the issuer of the certificate.
            subject (Subject): An object representing the subject of the certificate.
            records_json (str): JSON data containing certificate records.
            issuer_image (str): Path to the issuer's logo image file.
            subject_image (str): Path to the certificate image file.
            additional_global_fields (dict): Additional global fields for the certificate.
            app_name (str): Name of the application generating the certificate.
            recipient_fields (dict): Additional per-recipient fields for the certificate.
            valid_from (str, optional): Start date of the certificate's validity.
            valid_until (str, optional): End date of the certificate's validity.

        Returns:
            dict: A dictionary containing all the necessary data for generating unsigned certificates.
        """
        # Construct the unsigned_cert_data dictionary
        unsigned_cert_data = self._create_base_template(
            issuer,
            subject,
            records_json,
            issuer_image,
            subject_image,
            additional_global_fields,
            app_name,
            recipient_fields,
            valid_from,
            valid_until,
        )
        return unsigned_cert_data
    
    @staticmethod
    def create_certificate_template(unsigned_cert_data: object):
        """
        Create the certificate template using the provided unsigned certificate data.

        Args:
            unsigned_cert_data (object): The unsigned certificate data.

        Returns:
            dict: The certificate template.
        """
        # Create assertion section of credentials
        assertion = {
            "@context": [
                VERIFIABLE_CREDENTIAL_V2_CONTEXT,
                EVERYCRED_CREDENTIAL_V1_CONTEXT,
                # example subjectCredential type if not overridden
                "https://www.w3.org/2018/credentials/examples/v1",
            ],
            "type": ["VerifiableCredential", "EveryCREDCredential"],
            "issuer": {
                "id": unsigned_cert_data["issuer_did"],
                "profile": unsigned_cert_data["issuer_id"],
            },
            'issuanceDate': '*|DATE|*'
        }
        
        if unsigned_cert_data['validFrom']:
            assertion['validFrom'] = unsigned_cert_data['validFrom']
            
        if unsigned_cert_data['validUntil']:
            assertion['validUntil'] = unsigned_cert_data['validUntil']
        
        assertion['id'] = URN_UUID_PREFIX + '*|CERTUID|*'

        assertion["credentialSubject"] = {
            "id": unsigned_cert_data["subject_did"],
            "profile": unsigned_cert_data["subject_profile"]
        }

        # Create json content of additional fields
        global_fields = json.loads(unsigned_cert_data["additional_global_fields"])["fields"]
        recipient_fields = json.loads(
            unsigned_cert_data["additional_per_recipient_fields"]
        )["fields"]

        # Insert additional fields in template json
        if global_fields:
            field = global_fields[1]
            assertion = set_field(assertion, field["path"], field["value"])

        return assertion

    def _create_base_template(
        self,
        issuer: Issuer,
        subject: Subject,
        records_json: str,
        issuer_image: str,
        subject_image: str,
        additional_global_fields: Dict[str, Any],
        app_name: str,
        recipient_fields: Dict[str, Any],
        valid_from: Optional[str] = None,
        valid_until: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create the base template for unsigned certificate data.

        This function constructs the base template dictionary containing various parameters needed
        for generating unsigned certificates.

        Args:
            issuer (Issuer): An object representing the issuer of the certificate.
            subject (Subject): An object representing the subject of the certificate.
            records_json (str): JSON data containing certificate records.
            issuer_image (str): Path to the issuer's logo image file.
            subject_image (str): Path to the certificate image file.
            additional_global_fields (dict): Additional global fields for the certificate.
            app_name (str): Name of the application generating the certificate.
            recipient_fields (dict): Additional per-recipient fields for the certificate.
            valid_from (str, optional): Start date of the certificate's validity.
            valid_until (str, optional): End date of the certificate's validity.

        Returns:
            dict: A dictionary containing the base template for unsigned certificates.
        """
        return {
            # Credentials validity information
            "validFrom": valid_from,
            "validUntil": valid_until,
            # Issuer information
            "issuer_url": issuer.website,
            "issuer_email": issuer.email,
            "issuer_name": issuer.name,
            "issuer_did": issuer.did,
            "issuer_id": issuer.profile_link,
            "revocation_list": issuer.revocation_list,
            "issuer_public_key": f"ecdsa-koblitz-pubkey:{issuer.crypto_address}",
            # Subject information
            "subject_did": subject.did,
            "subject_profile": subject.profile_link,
            # Certificate information
            "certificate_title": subject.title,
            "roster": records_json,
            # Certificate images
            "issuer_logo_file": issuer_image,
            "cert_image_file": subject_image,
            # Additional fields
            "additional_global_fields": json.dumps(additional_global_fields),
            "additional_per_recipient_fields": json.dumps(recipient_fields),
            # Static information
            "certificate_description": f"Certificates are generated by {app_name}.",
            "criteria_narrative": "This is a blockchain-based certificate which is issued by a blockchain transaction.",
            "filename_format": "uuid",
            "no_clobber": True,
            "hash_emails": False,
        }
