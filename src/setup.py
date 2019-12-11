import setuptools

setuptools.setup(
    name="gcpdemo3",
    version="0.0.1",
    author="NT Concepts",
    author_email="kendall.ocasio@ntconcepts.com",
    description="GCP Demo 3 source code package.",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    include_package_data=True,
)
