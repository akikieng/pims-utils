from setuptools import setup

setup(
    name='PimsUtils',
    packages=['PimsUtils'],
    version='0.0',
    python_requires='>=3.5',
    url='https://github.com/akikieng/pims-utils',
    author=['Shadi Akiki'],
    author_email=['shadi@akikieng.com'],
    description=('Utility tools to read/convert files exported from PIMS'
                 'e.g. read stock rebuild xls'),
    # TODO # license='BSD',
    scripts=['PimsUtils/PimsRebuildXls.py'],
    install_requires=[
      'pandas==0.23.4',
      'xlrd==1.1.0',
      'pytest==3.8.2',
    ],
)

