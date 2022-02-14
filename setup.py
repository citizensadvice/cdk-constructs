from setuptools import setup

setup(name='cdk-constructs',
      version='0.0.2',
      description='Constructs for Python AWS CDK',
      url='https://github.com/citizensadvice/cdk-constructs',
      author='Citizens Advice',
      author_email='ca-devops@citizensadvice.org.uk',
      license='MIT',
      install_requires=[
          'aws-cdk-lib>=2.4.0,<3.0.0',
          'constructs>=10.0.0,<11.0.0',
          'cdk-remote-stack>=2.0.8,<3.0.0'
      ],
      packages=['cdk_constructs'],
      package_data={'cdk_constructs': ['assets/*.json']},
      include_package_data=True)
