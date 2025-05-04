"""
Unit tests for the UnsignedCertGenerator class.

This module contains tests for the UnsignedCertGenerator class,
which is responsible for generating unsigned certificate data.
"""

import importlib.util
import os
import sys
import unittest

# Add the unsigned_generator directory to the sys.path
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
unsigned_generator_dir = os.path.join(base_dir, 'unsigned_generator')
sys.path.insert(0, unsigned_generator_dir)

# Function to import a module from a file path
def import_module_from_path(module_name, file_path):
    """
    Import a module from a specific file path.

    Args:
        module_name (str): The name to assign to the imported module.
        file_path (str): The file path to the module.

    Returns:
        module: The imported module.
    """
    print(f"Importing {module_name} from {file_path}")
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None:
        raise ImportError(f"Cannot find module {module_name} at {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

# Define the paths to the modules
schema_path = os.path.join(unsigned_generator_dir, 'schema.py')
unsigned_gen_path = os.path.join(unsigned_generator_dir, 'unsigned_gen.py')

# Verify the paths
print(f"Schema path: {schema_path}")
print(f"Unsigned gen path: {unsigned_gen_path}")

# Import the modules
schema = import_module_from_path('schema', schema_path)
unsigned_gen = import_module_from_path('unsigned_gen', unsigned_gen_path)

Issuer = schema.Issuer
Subject = schema.Subject
UnsignedCertGenerator = unsigned_gen.UnsignedCertGenerator

class TestUnsignedCertGenerator(unittest.TestCase):
    """
    Test case for the UnsignedCertGenerator class.
    """

    def setUp(self):
        """
        Set up the test case with necessary objects and data.
        """
        self.generator = UnsignedCertGenerator()
        self.issuer = Issuer(
            name="Test Issuer",
            website="https://issuer.example.com",
            email="issuer@example.com",
            did="did:example:123",
            profile_link="https://issuer.example.com/profile",
            revocation_list="https://issuer.example.com/revocation",
            crypto_address="123abc"
        )
        self.subject = Subject(
            title="Test Certificate",
            did="did:example:456",
            profile_link="https://subject.example.com/profile"
        )
        self.records_json = '{"records": []}'
        self.issuer_image = "path/to/issuer_image.png"
        self.subject_image = "path/to/subject_image.png"
        self.additional_global_fields = {"field1": "value1"}
        self.app_name = "TestApp"
        self.recipient_fields = {"recipient1": "value1"}

    def test_generate_certificate(self):
        """
        Test the generate_unsigned_cert_data method of UnsignedCertGenerator.
        """
        cert = self.generator.generate_unsigned_cert_data(
            self.issuer,
            self.subject,
            self.records_json,
            self.issuer_image,
            self.subject_image,
            self.additional_global_fields,
            self.app_name,
            self.recipient_fields
        )
        self.assertIn("issuer_name", cert)
        self.assertEqual(cert["issuer_name"], self.issuer.name)
        self.assertIn("subject_did", cert)
        self.assertEqual(cert["subject_did"], self.subject.did)

if __name__ == '__main__':
    unittest.main()
