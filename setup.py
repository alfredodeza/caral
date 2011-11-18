from setuptools import setup

scripts = ['bin/caral']


long_description = """ caral - A flexible PyPi mirror """

requirements = [
              "BeautifulSoup",
            ]


setup(
    name                 = "caral",
    version              = "0.1.1",
    packages             = ['caral'],
    scripts              = scripts,
    author               = "Alfredo Deza",
    author_email         = "alfredodeza [at] gmail.com",
    description          = "A flexible PyPi mirror",
    license              = "MIT",
    include_package_data = True,
    zip_safe             = False,
    keywords             = "pypi, mirror",
    install_requires     = requirements,
    classifiers          = [
                            'Development Status :: 4 - Beta',
                            'Intended Audience :: Developers',
                            'License :: OSI Approved :: MIT License',
                            'Topic :: Software Development :: Build Tools',
                            'Topic :: Software Development :: Libraries',
                            'Topic :: Software Development :: Testing',
                            'Topic :: Utilities',
                            'Operating System :: MacOS :: MacOS X',
                            'Operating System :: Microsoft :: Windows',
                            'Operating System :: POSIX',
                            'Programming Language :: Python :: 2.5',
                            'Programming Language :: Python :: 2.6',
                            'Programming Language :: Python :: 2.7',
                      ],
    long_description = long_description,
)
#from setuptools import setup, find_packages
#
#version = '0.1'
#
#requirements = [
#              "simplegeneric >= 0.7",
#            ]
#
##
## Testing Requirements 
##
#requirements.extend([
#              "pecanraw == 0.0.2",
#              "teja == 0.0.5",
#              "BeautifulSoup"
#              ])
#
#
##
## call setup
##
#setup(
#    name                 = 'pipy',
#    version              = version,
#    description          = "private pypi",
#    long_description     = None,
#    classifiers          = [],
#    keywords             = '',
#    author               = 'alfredo deza',
#    author_email         = 'alfredo@shootq.com',
#    url                  = 'http://shootq.com/',
#    license              = 'Commercial',
#    packages             = find_packages(exclude=['ez_setup', 'examples', 'tests']),
#    include_package_data = True,
#    zip_safe             = False,
#    paster_plugins       = ['Pecan'],    
#    install_requires     = requirements,
#)
