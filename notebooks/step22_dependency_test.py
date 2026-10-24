
from importlib.metadata import version

packages = [
    "Flask",
    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",
    "scikit-learn",
    "textblob",
]

try:
    for package in packages:
        print(f"{package}: {version(package)}")

    import flask
    import pandas
    import numpy
    import matplotlib
    import seaborn
    import sklearn
    import textblob

    print("\nPASS: All 7 dependencies installed and imported successfully.")

except Exception as error:
    print("\nFAIL:", error)
    raise
