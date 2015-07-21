#!/usr/bin/env python

from distutils.core import setup

def gen_data_files( directory ):
    import os.path
    results = []
    for root, dirs, files in os.walk( directory ):
        results.extend([ "../" + os.path.join(root, f) for f in files])
    return results

pymata_package_data = gen_data_files('ArduinoSketch')

setup(
    name='PyMata',
    packages=['PyMata'],
    version='2.08',
    description="A Python Protocol Abstraction Library For Arduino Firmata",
    author='Alan Yorinks',
    author_email='MisterYsLab@gmail.com',
    url='https://github.com/MrYsLab/PyMata',
    download_url='https://github.com/MrYsLab/PyMata',
    install_requires=['pyserial == 2.7'],
    package_data={'PyMata': pymata_package_data},
    keywords=['Firmata', 'Arduino', 'Protocol'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Utilities',
        'Topic :: Home Automation',
    ],
)
