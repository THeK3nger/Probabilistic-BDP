from setuptools import setup

INSTALL_REQUIRES = [
    "numpy",
    "matplotlib",
    "yoshix"
]

TESTS_REQUIRES = [
    "nose"
]

setup(
    name='Continuous BDP Benchmark',
    version='1.0.0',
    packages=['pbdp'],
    package_data={
        'maps': ['maps']
    },
    entry_points={
        'console_scripts': [
            'pbdp=pbdp.__main__:main'
        ]
    },
    url='https://github.com/THeK3nger/Probabilistic-BDP',
    license='MIT',
    author='Davide Aversa',
    author_email='thek3nger@gmail.com',
    description='Benchmarking Belief-Aware Pathfinding Algorithms',
    test_suite='nose.collector',
    install_require=INSTALL_REQUIRES,
    tests_require=TESTS_REQUIRES
)
