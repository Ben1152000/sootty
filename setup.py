import setuptools 

setuptools.setup( 
    name='sootty', 
    version='0.1',
    description='Converts vcd files into svg', 
    packages=setuptools.find_packages(), 
    entry_points={ 
        'console_scripts': [ 
            'sootty = sootty.main:main'
        ] 
    },
    package_data={
        "sootty.static": ["*.lark"],
    },
    install_requires=[
        'lark',
    ],
    dependency_links=[
        'https://github.com/Nic30/pyDigitalWaveTools.git'
    ],
)