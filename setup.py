import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as ffile:
    README = ffile.read()

setup(
    name="django-dbbackup-s3",
    python_requires=">=3.7.0",
    version="0.1",
    author="Jirka Schaefer",
    author_email="info@tschitschereengreen.com",
    packages=find_packages(),
    include_package_data=True,
    url="https://github.com/patroqueeet/django-dbbackup-s3",
    license="Apach 2.0",
    install_requires=[
        "Django>=3.2",
        "django-storages[boto3,dropbox]~=1.13.1",
        "django-environ~=0.9.0",
        "django-dbbackup~=4.0.2",
    ],
    description="Backup S3 files to tar.gz in DropBox",
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Internationalization",
        "Topic :: Software Development :: Localization",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
)
