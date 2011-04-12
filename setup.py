from setuptools import setup

setup(
    name='healthmodels',
    version='0.1',
    license="BSD",

    install_requires = ["rapidsms",'simple_locations'],

    dependency_links = [
        "http://github.com/mossplix/simple_locations/tarball/master#egg=simple_locations"
    ],

    description='A common set of models for mHealth-related applications.',
    long_description=open('README.rst').read(),
    author='David McCann',
    author_email='david.a.mccann@gmail.com',

    url='http://github.com/daveycrockett/healthmodels',
    download_url='http://github.com/daveycrockett/healthmodels/downloads',

    include_package_data=True,

    packages=['healthmodels'],

    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)
