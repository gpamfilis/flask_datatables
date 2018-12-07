from setuptools import setup, find_packages

setup(name='flask_datatables',
      version='0.1',
      description='A python package to handle data tables functionality in flask.',
      url='http://github.com/gpamfilis/flask_datatables',
      author='George Pamfilis',
      author_email='gpamfilis@gmail.com',
      license='MIT',
      platforms='any',
      packages=find_packages(),
      zip_safe=False, 
      install_requires=['Flask>=0.10'],
      include_package_data=True)
