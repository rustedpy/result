from setuptools import setup

readme = open('README.rst').read()

setup(name='result',
      version='0.1.1',
      description='A rust-like result type for Python',
      author='Danilo Bargen',
      author_email='mail@dbrgn.ch',
      url='https://github.com/dbrgn/result',
      packages=['result'],
      zip_safe=True,
      include_package_data=True,
      license='MIT',
      keywords='rust result enum',
      long_description=readme,
      classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
      ],
)
