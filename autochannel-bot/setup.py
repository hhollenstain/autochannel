"""``AutoChannel-Bot`` lives on
https://github.com/hhollenstain/autochannel-bot
"""
from setuptools import setup, find_packages
import autochannel

INSTALL_REQUIREMENTS = [
    'asyncio',
    'aiomeasures',
    'coloredlogs',
    'datadog',
    'discord.py==1.2.3',
    'pip==18.0',
    'pyyaml',
    'requests==2.21.0',
]

TEST_REQUIREMENTS = {
    'test':[
        'pytest',
        'pylint',
        'sure',
        ]
    }

setup(
    name='autochannel',
    version=autochannel.VERSION,
    description='AutoChannel Discord Bot',
    url='https://github.com/hhollenstain/autochannel-bot',
    packages=find_packages(),
    include_package_data=True,
    install_requires=INSTALL_REQUIREMENTS,
    extras_require=TEST_REQUIREMENTS,
    entry_points={
        'console_scripts':  [
            'autochannel = autochannel.autochannel_bot:main',
        ],
    },
    )
