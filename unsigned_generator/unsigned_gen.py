"""
Module to generate unsigned certificate data.

This module defines the UnsignedCertGenerator class, which is responsible for generating
the data required for creating unsigned certificates.
"""

import copy
import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from unsigned_generator.constants import (
    EVERYCRED_CREDENTIAL_V1_CONTEXT,
    URN_UUID_PREFIX,
    VERIFIABLE_CREDENTIAL_V2_CONTEXT,
)
from unsigned_generator.schema import Issuer, Subject

from .utils import Utils, Recipient


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
            dict: A dictionary containing all the necessary data
            for generating unsigned certificates.
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

    def create_certificate_template(self, unsigned_cert_data: object):
        """
        Create the certificate template using the provided unsigned certificate data.

        Args:
            unsigned_cert_data (object): The unsigned certificate data.

        Returns:
            dict: The certificate template.
        """
        return self._create_assertion(unsigned_cert_data)

    @staticmethod
    def create_unsigned_certificates_from_roster(
        template: object,
        recipients: list,
        use_identities: str,
        additional_fields: object,
        holder_data,
    ):
        """This function will generate unsigned certificate from roster file.

        Args:
            template (object): Certificate template json
            recipients (list): List of recipients
            use_identitties (str): Certificate identity type
            additional_fields (object): Additional fields
            hase_mails (bool): Use hash mail mode or normal mode

        Return:
            Return unsigned certificates json content
        """
        # Time of certificate generation
        issued_on = datetime.now(timezone.utc).isoformat()[:-13] + "Z"

        # Store unsigned certificate json in certs dict
        certs = {}
        certs_info = {}

        # Update recipient information in template file
        for recipient in recipients:
            # Generate unique id
            if use_identities:
                uid = recipient.identity
                uid = "".join(c for c in uid if c.isalnum())
            else:
                uid = str(uuid.uuid4())

            cert = copy.deepcopy(template)

            # Add subject field data
            credential_meta_data = copy.deepcopy(recipient)
            credential_meta_data.slug.pop("pubkey")
            credential_meta_data.slug.pop("html")
            if "additional_slug" in credential_meta_data.slug:
                credential_meta_data.slug.pop("additional_slug")

            # Instantiate Assertion
            cert["issuanceDate"] = issued_on
            cert["id"] = URN_UUID_PREFIX + uid
            holder_did = holder_data[recipient.identity]
            cert["holder"] = {"id": holder_did, "profile": holder_data[holder_did]}

            cert["credentialSubject"]["subjectMetaData"] = credential_meta_data.slug

            # Instantiate Recipient
            if additional_fields:
                if not recipient.additional_fields:
                    raise Exception(
                        "expected additional recipient fields but none found"
                    )

            else:
                if recipient.additional_fields:
                    # throw an exception on this in case it's a user error.
                    # We may decide to remove this if it's a nuisance
                    raise Exception(
                        "there are fields that are not expected by the\
                            additional_per_recipient_fields configuration"
                    )

            certs[uid] = cert

            # Store certificate info in a dict
            certs_info[uid] = {
                "candidate_name": recipient.name,
                "candidate_email": recipient.identity,
                "slug": recipient.slug,
                "holder_did": holder_data[recipient.identity],
            }

        return certs, certs_info

    @staticmethod
    def generate_unsigned_certificates_w3c(unsigned_cert_data, holder_data: dict):
        """This function will instantiate batch to generate unsigned
        certificate in batch.

        Args:
            unsigned_cert_data (dict): Required information
            to generate unsigned certificates.
            holder_data (dict): Dictionary containing holder information.
                Format:
                {
                    "identity1": "holder_did1",
                    "holder_did1": "holder_profile_link1",
                    "identity2": "holder_did2",
                    "holder_did2": "holder_profile_link2",
                    #...
                }

        Returns:
            Generate unsigned certificates.
        """

        # Create list of recipients details.
        try:
            recipients_map = map(lambda x: Recipient(x), unsigned_cert_data["roster"])
            recipients = list(recipients_map)
        except Exception as exp:
            raise RuntimeError("Error processing recipients") from exp

        # Create certificate template
        template = UnsignedCertGenerator().create_certificate_template(
            unsigned_cert_data
        )

        # Check file formate time for each certificate
        use_identities = unsigned_cert_data["filename_format"] == "certname_identity"

        # Load additional recipient fields json content
        recipient_fields = json.loads(
            unsigned_cert_data["additional_per_recipient_fields"]
        )["fields"]

        # Generate unsigned certificate json content
        certs, certs_info = UnsignedCertGenerator().create_unsigned_certificates_from_roster(
            template,
            recipients,
            use_identities,
            recipient_fields,
            holder_data
        )

        # Store each certificates of batch in output_dir.
        credentials_json = [json.dumps(certs[uid]) for uid in certs.keys()]

        return certs_info, credentials_json

    def _create_assertion(self, unsigned_cert_data: dict) -> dict:
        """
        Create the assertion section of credentials.

        Args:
            unsigned_cert_data (dict): The unsigned certificate data.

        Returns:
            dict: The assertion section of the credentials.
        """
        assertion = {
            "@context": [
                VERIFIABLE_CREDENTIAL_V2_CONTEXT,
                EVERYCRED_CREDENTIAL_V1_CONTEXT,
            ],
            "type": ["VerifiableCredential", "EveryCREDCredential"],
            "issuer": {
                "id": unsigned_cert_data["issuer_did"],
                "profile": unsigned_cert_data["issuer_id"],
            },
            "issuanceDate": "*|DATE|*",
        }

        if unsigned_cert_data["validFrom"]:
            assertion["validFrom"] = unsigned_cert_data["validFrom"]

        if unsigned_cert_data["validUntil"]:
            assertion["validUntil"] = unsigned_cert_data["validUntil"]

        assertion["id"] = URN_UUID_PREFIX + "*|CERTUID|*"

        assertion["credentialSubject"] = {
            "id": unsigned_cert_data["subject_did"],
            "profile": unsigned_cert_data["subject_profile"],
        }

        global_fields = json.loads(unsigned_cert_data["additional_global_fields"])[
            "fields"
        ]

        if global_fields:
            field = global_fields[1]
            assertion = Utils().set_field(assertion, field["path"], field["value"])

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
