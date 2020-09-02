from setuptools import find_packages, setup

setup(
    name='pico-pytest',
    packages=find_packages(),
    entry_points={"console_scripts": ['pico-pytest = pico_pytest.cli:main']},
)
