def file_reading_gen(path: str, fields: int, sep: str = ',', header: bool =False):
    """ 
    Reads fields from a file seperated by the provided seperator.

    Args:
        path (str): path of the file we want to read.
        fields (int): Number of fields expected in the file we are reading.
        sep (str): Separator that separates the fields from one another.
        header (bool): Signifies if there is a header in the file being passed to read.
    
    Yields:
        Tuple of data after separation.
    
    Raises:
        ValueError: When we encounter a different number of fields than expected.
    """
    
    with open(path) as f:
        if header:
            data = f.readline()
            data = data.split(sep)
            if len(data) != fields:
                raise ValueError("Expected {} fields, but got {} in the header".format(fields, len(data)))
        offset = 1
        if header:
            offset = 2
        for i, line in enumerate(f, offset):
            if line[-1] == '\n':
                line = line[:-1]
            data = line.split(sep)
            if len(data) != fields:
                raise ValueError("Expected {} fields, but got {} at line {}".format(fields, len(data), i))

            yield tuple(data)