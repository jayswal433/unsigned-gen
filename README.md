# unsigned-gen

A robust unsigned certificate generation library for Python 3.8+.

This library generates unsigned certificate data for various use cases.

## Key Features

- Generates unsigned certificate data.
- Supports various issuer and subject configurations.
- Provides a flexible API for customization.

## Installation

This package is available on PyPI. You can install it using pip:

```sh
pip install unsigned-gen
```

(You might need to use `pip3` depending on your local environment.)

## Quick Start

If you're generating an unsigned certificate, you might do this:

```python
from unsigned_gen import UnsignedCertGenerator, Issuer, Subject

issuer = Issuer(
    name="Test Issuer",
    website="https://issuer.example.com",
    email="issuer@example.com",
    did="did:example:123",
    profile_link="https://issuer.example.com/profile",
    revocation_list="https://issuer.example.com/revocation",
    crypto_address="123abc"
)

subject = Subject(
    title="Test Certificate",
    did="did:example:456",
    profile_link="https://subject.example.com/profile"
)

generator = UnsignedCertGenerator()
cert = generator.generate_unsigned_cert_data(
    issuer,
    subject,
    '{"records": []}',
    "path/to/issuer_image.png",
    "path/to/subject_image.png",
    {"field1": "value1"},
    "TestApp",
    {"recipient1": "value1"}
)

print(cert)
```

## Usage

### Overview

The module provides a class `UnsignedCertGenerator` which takes issuer and subject details and generates unsigned certificate data.

### Detailed Examples

Provide detailed examples of how to use your package. Include code snippets and explanations.

```python
from unsigned_gen import UnsignedCertGenerator, Issuer, Subject

# Example 1
issuer = Issuer(
    name="Test Issuer",
    website="https://issuer.example.com",
    email="issuer@example.com",
    did="did:example:123",
    profile_link="https://issuer.example.com/profile",
    revocation_list="https://issuer.example.com/revocation",
    crypto_address="123abc"
)

subject = Subject(
    title="Test Certificate",
    did="did:example:456",
    profile_link="https://subject.example.com/profile"
)

generator = UnsignedCertGenerator()
cert = generator.generate_unsigned_cert_data(
    issuer,
    subject,
    '{"records": []}',
    "path/to/issuer_image.png",
    "path/to/subject_image.png",
    {"field1": "value1"},
    "TestApp",
    {"recipient1": "value1"}
)

print(cert)
```

## Options

Describe any options or configurations that can be used with your package.

### Option 1

Description of option 1.

### Option 2

Description of option 2.

## Testing

Explain how to run tests for your package.

```sh
pip install -r test_requirements.txt
make test
```

## License

Provide information about the license under which your package is distributed.

## Contributing

Explain how others can contribute to your project. Include guidelines for submitting issues and pull requests.

## Help

Provide information on where users can get help with your package.

## Acknowledgements

Acknowledge any contributors or libraries that your project depends on.

## Contact

Provide contact information for users who have questions or need support.