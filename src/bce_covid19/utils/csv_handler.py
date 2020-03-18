import csv
from typing import Dict, Any, List, Tuple, Iterator, Optional, Union


def csv_writer(csv_path: str, obj: Iterator[Dict[str, Any]], fieldnames: List[str]) -> None:
    """
    Saves a list of dictionaries into a csv file.

    (Unittest in test folder)

    Args:
        fieldnames: the header names of the csv.
        csv_path: the path to csv file to save, should end with the name.csv
        obj: an iterator with the  list of dictionaries to save to csv.

    """
    with open(csv_path, mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for entry in obj:
            writer.writerow(entry)


def csv_reader(csv_path: str, header_lines: int, header_names: List[Any] = None) -> \
        Iterator[Dict[Union[str, Tuple[str, str]], Optional[str]]]:
    """
    Read a csv file into list of dictionaries.

    The header lines are removed form the entries of the csv.

    (Unittest in test folder)

    Args:
        header_lines: the total lines in csv which constitute the header.
        header_names: the header names.
        csv_path:  the path to csv file to save, should end with the name.csv

    Returns: an iterator of dictionaries with keys the header_names and values the entries in the csv as strings.


    """
    with open(csv_path, mode='r') as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=header_names)
        # skip field names which are read as lines:
        for row in range(header_lines):
            next(reader)
        # read the rest
        for row in reader:
            yield empty_to_none_string(obj=dict(row))


def empty_to_none_string(obj: Dict[str, str]) -> Dict[str, Optional[str]]:
    """
    Replace empty string values of the dictionary  with None.

    Args:
        obj: dictionary to check.

    Returns: the input dictionary with "" values replaced by None.

    Examples:
        >>> print(empty_to_none_string(obj={'a': 'a', 'b': '','c':"1"})) #doctest: +NORMALIZE_WHITESPACE
        {'a': 'a', 'b': None, 'c': '1'}
    """
    return {key: (value if len(value) != 0 else None) for key, value in obj.items()}


def csv_header(csv_path: str, header_lines: int) -> List[List[Any]]:
    """
    Get the header from the csv file.

    Args:
        csv_path: the path to the csv file.
        header_lines: the total lines that the header consists of.

    Returns: nested lists of the headers. each list correspond to 1 line from the csv file.

    """
    headers = []
    with open(csv_path, mode='r') as csv_file:
        reader = csv.reader(csv_file)
        for i in range(header_lines):
            headers.append(next(reader))

    return headers


def make_header_tuples(headers: List[List[Any]]) -> List[Tuple[Any]]:
    """
    Make tuple headers elementwise from nested lists.

    Args:
        headers: list of lists with strings, the inner lists are of same length.

    Returns: list of tuple of strings by connecting the list elementwise.

    Examples:
        >>> list_1=["A","B","C"]
        >>> list_2=["D","E","F"]
        >>> tuples_list = make_header_tuples(headers=[list_1,list_2])
        >>> print(tuples_list) #doctest: +NORMALIZE_WHITESPACE
        [('A', 'D'), ('B', 'E'), ('C', 'F')]
        >>> list_3=[1,2,3]
        >>> tuples_list = make_header_tuples(headers=[list_1,list_2,list_3])
        >>> print(tuples_list) #doctest: +NORMALIZE_WHITESPACE
        [('A', 'D', 1), ('B', 'E', 2), ('C', 'F', 3)]

    """
    return list(zip(*headers))


def make_header_list(headers: List[List[Any]]) -> List[Any]:
    """
    Unnest a nested list.

    Args:
        headers: nested lists to unnest.

    Returns: a single list with the elements of all the other lists.

    Examples:
        >>> list_1=["A","B","C"]
        >>> list_2=["D","E","F"]
        >>> headers_list = make_header_list(headers=[list_1,list_2])
        >>> print(headers_list) #doctest: +NORMALIZE_WHITESPACE
        ['A', 'B', 'C', 'D', 'E', 'F']
        >>> list_3=[1,2,3]
        >>> headers_list = make_header_list(headers=[list_1,list_2,list_3])
        >>> print(headers_list) #doctest: +NORMALIZE_WHITESPACE
        ['A', 'B', 'C', 'D', 'E', 'F', 1, 2, 3]

    """
    return [entry for element in headers for entry in element]


def get_next_nonempty(csv_iterator: Iterator[List[str]]) -> List[str]:
    """
    Get the next non-empty line of a csv iterator

    Args:
        csv_iterator: an iterator of lists with possible empty elements.

    Returns: the next non-empty element.

    Examples:
        >>> csv_iterator=iter([["element_1"],[],["element_2"]])
        >>> print(get_next_nonempty(csv_iterator=csv_iterator)) #doctest: +NORMALIZE_WHITESPACE
        ['element_1']
        >>> print(get_next_nonempty(csv_iterator=csv_iterator)) #doctest: +NORMALIZE_WHITESPACE
        ['element_2']
        >>> print(get_next_nonempty(csv_iterator=csv_iterator)) #doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
        Traceback (most recent call last):
        ...
        StopIteration


    """
    while True:
        try:
            line = next(csv_iterator)
        except StopIteration:
            raise StopIteration
        else:
            if any(len(el) != 0 for el in line):
                return line


class HeadersError(KeyError):
    """Exception raised for errors in the input csv if the input headers are wrong"""
    pass
