"""
Schema definitions for the unsigned-gen package.

This module defines the data classes for representing the issuer and subject information
required for generating unsigned certificates.
"""

from dataclasses import dataclass


@dataclass
class Issuer:
    """
    Data class to represent the issuer's information.

    Attributes:
        name (str): The name of the issuer.
        email (str): The email address of the issuer.
        website (str): The website of the issuer.
        did (str): The decentralized identifier (DID) of the issuer.
        profile_link (str): The profile link of the issuer.
        revocation_list (str): The revocation list URL of the issuer.
        crypto_address (str): The cryptocurrency address of the issuer.
    """
    name: str
    email: str
    website: str
    did: str
    profile_link: str
    revocation_list: str
    crypto_address: str


@dataclass
class Subject:
    """
    Data class to represent the subject's information.

    Attributes:
        title (str): The title of the subject.
        did (str): The decentralized identifier (DID) of the subject.
        profile_link (str): The profile link of the subject.
    """
    title: str
    did: str
    profile_link: str
