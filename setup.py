import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='Rule34',
    version='0.0.2',
    author='Nubis',
    author_email='Nubis@hotmail.com',
    description='Python package that allows you to access the content from the famous adult website',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/ilNubis/Rule34',
    project_urls = {
        "Bug Tracker": "https://github.com/ilNubis/Rule34/issues"
    },
    license='MIT',
    packages=['Rule34'],
    install_requires=['requests', 'lxml'],
)
