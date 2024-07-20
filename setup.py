from setuptools import setup, find_packages # type: ignore

setup(
    name="dundie",
    version="0.1.0",
    description="Reward Point System",
    author="Alex Silva",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "dundie = dundie.__main__:main"
        ]
    }
)