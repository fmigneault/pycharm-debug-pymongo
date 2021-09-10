from setuptools import find_packages, setup

with open("./requirements.txt") as req:
    REQUIREMENTS = [r for r in req.readlines() if r and not r.startswith("#")]

setup(
    name="pycharm_debug_pymongo",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.6, <4",
    install_requires=REQUIREMENTS,
    entry_points={
        "paste.app_factory": [
            "main = pycharm_debug_pymongo.app:main"
        ]
    }
)
