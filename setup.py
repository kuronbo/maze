from setuptools import setup, find_packages

setup(
    name='maze',
    version='0.0.9',
    packages=find_packages(exclude=['tests', 'venv']),
    url='https://github.com/kuronbo/maze',
    license='MIT',
    author='kuronbo',
    author_email='kurinbo.i2o@gmail.com',
    description='solve maze program',
    requires=['pytest'],
    keywords=['maze']
)
