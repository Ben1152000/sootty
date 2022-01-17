import pathlib
import setuptools 

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


setuptools.setup( 
    name='sootty',
    version='0.2.3',
    description='Displays vcd files to the command line.', 
    long_description=README,
    packages=setuptools.find_packages(exclude=("tests",)), 
    long_description_content_type="text/markdown",
    url="https://github.com/Ben1152000/sootty",
    author="Ben Darnell",
    author_email="ben@bdarnell.com",
    license="BSD",
    entry_points={ 
        'console_scripts': [ 
            'sootty = sootty.__main__:main'
        ]
    },
    package_data={
        "sootty.static": ["*.lark"],
    },
    install_requires=[
        'lark>=1',
        'pyvcd>=0.3',
        'sortedcontainers>=2.4'
    ],
)