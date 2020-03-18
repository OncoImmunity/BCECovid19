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


def get_ncbi_entrez_covid_19_path() -> str:
    """
    Get path of the ncbi_entrez_covid_19 folder

    Returns: path of the directory of the `ncbi_entrez_covid_19` folder as string.

    Example:
        >>> path = get_ncbi_entrez_covid_19_path()
        >>> print(path) # doctest: +ELLIPSIS
        /.../BCECovid19/src/bce_covid19/data/ncbi_entrez_covid_19
    """
    return os.path.join(get_data_path(), "ncbi_entrez_covid_19")

