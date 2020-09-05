"""An adjacency matrix implementation."""

import copy


##########
# Helper #
##########
def warshall_adjacency(matrix):
    """Applies the Warshall transitive closure algorithm to a adjacency matrix.

    Args:
        matrix: The adjacency matrix.

    Returns:
        The closed form of the adjacency matrix.
    """
    for k in range(0, len(matrix)):
        for i in range(0, len(matrix)):
            if matrix[i][k] == 1:
                for j in range(0, len(matrix[0])):
                    if matrix[k][j] == 1:
                        matrix[i][j] = 1
    return matrix


####################
# Adjacency Matrix #
####################
class AdjacencyMatrix:
    """An adjacency matrix."""

    def __init__(self, headers):
        """Initializes AdjacencyMatrix.

        Args:
            headers: A list of header names.
        """
        self.headers = headers
        self.matrix = None
        self.init_matrix()

    def init_matrix(self):
        """Initializes the matrix with zeros.

        Returns:
            None
        """
        header_num = len(self.headers)
        self.matrix = [[0 for _ in range(header_num)] for _ in range(header_num)]

    def set_entry_by_names(self, row_name, column_name, val):
        """Sets a single matrix entry, identified by its row and column name, to a given value.

        Args:
            row_name: The row header name.
            column_name: The column header name.
            val: The new entry value.

        Returns:
            None
        """
        row_index = self.headers.index(row_name)
        column_index = self.headers.index(column_name)
        self.matrix[row_index][column_index] = val

    def close(self):
        """Transforms the adjacency matrix into closed form (i.e., the transitive closure).

        Returns:
            The AdjacencyMatrix instance itself.
        """
        self.matrix = warshall_adjacency(self.matrix)
        return self

    def copy_matrix(self):
        """Copies the value matrix.

        Returns:
            The copied value matrix.
        """
        return copy.deepcopy(self.matrix)

    def copy(self):
        """Copies the AdjacencyMatrix instance.

        Returns:
            The copied AdjacencyMatrix instance.
        """
        copy_obj = AdjacencyMatrix(headers=self.headers)
        copy_obj.matrix = self.copy_matrix()
        return copy_obj

    def __repr__(self):
        # https://stackoverflow.com/questions/13214809/pretty-print-2d-python-list?answertab=oldest#tab-top
        s = [[""] + self.headers]
        s += [([self.headers[i]] + [str(e) for e in row]) for i, row in enumerate(self.matrix)]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = ' '.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        return '\n'.join(table)
