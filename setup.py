from setuptools import setup

setup(
    name='qt_files_converter',
    version='0.1',
    description='Converts .qt files',
    author='Lukasz Kolat',
    author_email='lukasz.kolat@stxnext.com',
    packages=['QTconverter'],
    package_dir={'': '..'},
    zip_safe=False
)
