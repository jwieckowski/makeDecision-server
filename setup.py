from setuptools import setup, find_packages

# Read the version from the package
with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()

setup(
    name="mdserver",
    version="1.1.0",
    author="Jakub Więckowski",
    author_email="j.wieckowski@il-pib.pl",
    description="Python Flask-RESTX server for make-decision.it application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="python, decision making, mcda, gui, rest api, flask server",
    license="MIT License",
    url="https://github.com/jwieckowski/makeDecision-server",
    classifiers=[
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.10",
    packages=find_packages(),
    install_requires=[
        "Flask==2.2.2",
        "flask-restx==1.1.0",
        "Flask-Cors==3.0.10",
        "Werkzeug==2.2.2",
        "numpy==1.23.1",
        "pymcdm==1.2.0",
        "pyfdm==1.1.12",
        "pandas==1.4.4",
        "Pillow==9.2.0",
        "pytest==7.1.2",
        "setuptools==63.2.0",
        "wheel==0.38.4",
        "pymongo==4.6.1",
        "python-dotenv==1.0.1"
    ],
)