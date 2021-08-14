import setuptools 

setuptools.setup( 
    name='sootty', 
    version='1.0',
    description='Converts vcd files into svg', 
    packages=setuptools.find_packages(), 
    entry_points={ 
        'console_scripts': [ 
            'sootty = src.main:main'
        ] 
    },
    package_data={
        "src.static": ["*.lark"],
    },
    install_requires=[
        'lark',
    ],
    dependency_links=[
        'https://github.com/Nic30/pyDigitalWaveTools.git'
    ],
)