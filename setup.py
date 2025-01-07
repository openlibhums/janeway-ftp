from setuptools import setup

setup(
    name='janeway-ftp',
    version='0.5.1',
    author='OLH Tech',
    author_email='olh-tech@bbk.ac.uk',
    packages=['janeway_ftp'],
    url='https://github.com/birkbeckctp/janeway-ftp/',
    license='LICENSE',
    description='A Django FTP package for Janeway.',
    long_description=open('README.md').read(),
    install_requires=[
       "paramiko >= 2.11.0",
    ],
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
    ],
    include_package_data=True
)
