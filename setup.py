from setuptools import setup

setup(
    name='ldbk',
    version='0.0.1',
    packages=['ldskbkp', 'ldskbkp.conf', 'ldskbkp.util', 'ldskbkp.filemgr', 'ldskbkp.database',
              'ldskbkp.database.models'],
    url='https://github.com/locchan/ldbk',
    license='GPLv2',
    author='locchan',
    author_email='locchan@protonmail.com',
    description='A backup solution targeting cd/dvd/blu-ray/iso drives as storage media.',
    install_requires=[
        'sqlalchemy',
        'alive-progress'
    ]
)
