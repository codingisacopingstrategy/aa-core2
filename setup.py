#! /usr/bin/env python2


from setuptools import setup


setup(
    name='aacore',
    version='0.1',
    author='The active archives contributors',
    author_email='alexandre@stdin.fr',
    description=('Active Archives inverts the paradigm of uploading resources',
        'into a centralized server and instead allows resources to remain',
        '"active", in-place and online. Caching and proxy functionality allow',
        'light-weight) copies of resources to be manipulated and preserved',
        'even, as the original sources change or become (temporarily)',
        'unavailable.'),
    url='http://activearchives.org/',
    packages=['aacore', 'aacore.sniffers', 'aacore.templatetags'],
    dependency_links=[
        'git+git://git.constantvzw.org/aa.rdfutils.git#egg=rdfutils-0.1',
    ],
    install_requires=[
        'django>=1.4,<1.5',
        'html5lib',
        'requests',
        'python-magic',
        'html5tidy',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
    ]
)
