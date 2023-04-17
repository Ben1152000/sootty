## Instructions for how to update the version of the sootty package of PyPI:

1. Update the version number in `setup.py`.
2. Run this command to package the new version into the `dist` directory:

<!--  -->

    python3 setup.py sdist bdist_wheel


3. Run to check that the package contains the correct files:

<!--  -->

    tar tzf dist/sootty-<version>.tar.gz

4. Run to check whether the package will correctly render to PyPI:

<!--  -->

    twine check dist/*

5. Upload the newly created files to PyPI:

<!-- -->

    twine upload dist/sootty-<version>.tar.gz  dist/sootty-<version>-py3-none-any.whl

## Install project locally

    python3 -m pip install .

## Run all unit tests

    python3 -m unittest test
