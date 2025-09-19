from setuptools import setup, find_packages

setup(
    name="taxipred",
    version="0.0.1",
    description="This package contains taxipred app which predict taxi prices",
    author="Susanne W",
    install_requires=["streamlit", "pandas", "fastapi", "scikit-learn", "uvicorn"],
    package_dir={"": "src"},                  # koden ligger under src/
    packages=find_packages(where="src"),      # hitta paket under src/
    package_data={"taxipred": ["data/*.csv"]},
    include_package_data=True,                # ta med package_data vid build
    python_requires=">=3.9",
)

