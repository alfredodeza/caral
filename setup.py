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
