from setuptools import setup, find_packages
from bin.version import __version__

setup(name='SimulaToR',
      version=__version__,
      description='Simulate and calculate relative index by using short tandom repeat(STR) loci',
      author='Cheng-chen Shao',
      author_email='cshao07@fudan.edu.cn',
      url='https://github.com/xiaozhutousan/SimulaTeR',
      license='MIT',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
      ],
      keywords='Forensic Science',
      packages=find_packages(),
      install_requires=[
          'docopt',
          'xlrd',
          'pandas',
          'matplotlib',
          'seaborn',
          'sklearn',
          'xlsxwriter',
          'numpy'
      ],
      entry_points={
          'console_scripts': [
              'SimulaToR=bin.SimulaToR:main',
          ],
      },
      )
