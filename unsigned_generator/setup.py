from setuptools import setup, find_packages

setup(
    name="unsigned_gen",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "jsonpath-rw==1.4.0",
    ],
    include_package_data=True,
    description="A package to generate unsigned certificate data.",
    author="Your Name",
    author_email="your.email@example.com",
    # url="https://github.com/yourusername/unsigned_generator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
