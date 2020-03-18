import os


def get_data_path() -> str:
    """
    Get path of the data folder of the package.

    Returns:
        path of the directory of the `data` folder as string.

    Example:
        >>> path = get_data_path()
        >>> print(path) # doctest: +ELLIPSIS
        /.../BCECovid19/src/bce_covid19/data
    """
    return os.path.join(os.path.dirname(__file__), "data")

