class Iterator:
    """
    Iterator that reads lines from the specified file and allows iteration over them.
    """
    def __init__(self, name_of_file: str) -> None:
        """
        Initializes the Iterator with the file path and reads the file into a list.
        parametr:
        name_of_file: The path to the file to be read.
        """
        self.name_of_file = name_of_file
        self.counter = 0
        self.list = []
        file = open(self.name_of_file, "r")
        for row in file:
            self.list.append(row)
        file.close

    def __iter__(self):
        """
        Returns the iterator object.
        """
        return self

    def __next__(self) -> str:
        """
        Returns the next line from the file. 
        If there are no more rows, a StopIteration exception.
        """
        if self.counter < len(self.list):
            tmp = self.list[self.counter]
            self.counter += 1
            return tmp
        else:
            raise StopIteration
