import os

from setuptools import find_packages, setup

# Package meta-data.
NAME = 'redux'
DESCRIPTION = ''
URL = 'https://github.com/rogthedodge/redux'
EMAIL = 'rogthedodge@gmail.com'
AUTHOR = 'Roger Holmes'

# What packages are required for this module to be executed?
REQUIRED = [
    'falcon==1.2.0',
    'psycopg2==2.7.3.1',
    'python-mimeparse==1.6.0',
    'six==1.10.0',
    'nose2==0.7.2'
]

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Where the magic happens:
setup(
    name=NAME,
    # version=about['__version__'],
    description=DESCRIPTION,
    # long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    # If your package is a single module, use this instead of 'packages':
    # py_modules=['mypackage'],

    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
    install_requires=REQUIRED,
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],

)