import os
from setuptools import setup, find_packages


HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, "README.rst")) as f:
    README = f.read()

with open(os.path.join(HERE, "CHANGELOG.rst")) as f:
    CHANGES = f.read()


def get_version():
    with open(os.path.join(HERE, "grits/__init__.py")) as f:
        for line in f:
            if line.startswith("__version__"):
                return eval(line.split("=")[-1])

REQUIREMENTS = [
    "click==6.7",
    "jinja2==2.9.5",
    "lxml==3.7.2",
    "texas==0.5.2"
]

if __name__ == "__main__":
    setup(
        name="grits",
        version=get_version(),
        description="Static SPA Generator",
        long_description=README + "\n\n" + CHANGES,
        entry_points={
            "console_scripts": [
                "grits-build = grits.scripts.build:main",
                "grits-serve = grits.scripts.serve:main"
            ]
        },
        classifiers=[
            "Development Status :: 2 - Pre-Alpha",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.6",
        ],
        author="Joe Cross",
        author_email="joe.mcross@gmail.com",
        url="https://github.com/numberoverzero/grits",
        license="MIT",
        keywords="static blog spa generator",
        platforms="any",
        include_package_data=True,
        packages=find_packages(exclude=("test*", )),
        install_requires=REQUIREMENTS,
    )
