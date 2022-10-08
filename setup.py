import json
import os
from setuptools import setup


with open("package.json") as f:
    package = json.load(f)

package_name = package["name"].replace(" ", "_").replace("-", "_")

setup(
    name=package_name,
    version=package["version"],
    author=package["author"],
    packages=[package_name],
    include_package_data=True,
    license=package["license"],
    description=package.get("description", package_name),
    install_requires=[
        "pydantic>=1.9"
    ],
    extras_require={
        "distributed": ["rq>=1.11"],
        "full": ["dash>=2.6", "rq>=1.11"]
    },
    classifiers=[
        "Framework :: Dash",
    ],
)
