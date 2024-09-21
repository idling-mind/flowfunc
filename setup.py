import json
from pathlib import Path
from setuptools import setup

here = Path(__file__).parent
package = json.loads((here / "package.json").read_text())
long_description = (here / "README.md").read_text()

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
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.10",
    install_requires=[
        "pydantic>=2,<3",
    ],
    extras_require={"distributed": ["rq>=1.11"], "full": ["dash>=2.6", "rq>=1.11"]},
    classifiers=[
        "Framework :: Dash",
    ],
)
