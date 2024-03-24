from typing import Iterable
from typing import Callable


class MatrixHashMixin:
    def __hash__(self):
        # Sum of the elements
        return sum([sum(row) for row in self.matrix])


class Matrix(MatrixHashMixin):
    def __init__(self, matrix: Iterable[Iterable]) -> None:
        assert isinstance(matrix, Iterable)
        assert len(matrix)
        assert all([isinstance(row, Iterable) for row in matrix])
        assert len({len(row) for row in matrix}) == 1

        self.matrix = matrix
        self.__rows = len(matrix)
        self.__columns = len(matrix[0])

    def get_size(self) -> tuple[int, int]:
        return self.__rows, self.__columns

    def is_size_equal(self, other) -> bool:
        if not isinstance(other, Matrix):
            raise TypeError

        if self.get_size() != other.get_size():
            return False
        return True

    def is_size_fit_to_matmul(self, other) -> bool:
        if not isinstance(other, Matrix):
            raise TypeError

        if self.__columns != other.__rows:
            return False
        return True

    def __matrix_element_operation(self, other, operation: Callable) -> "Matrix":
        if not self.is_size_equal(other):
            raise ValueError

        result = [[0 for _ in range(self.__columns)] for _ in range(self.__rows)]
        for i in range(self.__rows):
            for j in range(self.__columns):
                result[i][j] = operation(self.matrix[i][j], other.matrix[i][j])
        return Matrix(result)

    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        return self.__add__(other)

    def __add__(self, other):
        return self.__matrix_element_operation(other, lambda x, y: x + y)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __imul__(self, other):
        return self.__mul__(other)

    def __mul__(self, other):
        return self.__matrix_element_operation(other, lambda x, y: x * y)

    def __imatmul__(self, other):
        return self.__matmul__(other)

    def __matmul__(self, other):
        if not self.is_size_fit_to_matmul(other):
            raise ValueError

        result = [[0 for _ in range(other.__columns)] for _ in range(self.__rows)]
        for i in range(self.__rows):
            for j in range(other.__columns):
                result[i][j] = sum(
                    [
                        self.matrix[i][k] * other.matrix[k][j]
                        for k in range(self.__columns)
                    ]
                )
        return Matrix(result)

    def __str__(self) -> str:
        return self.matrix.__str__()

    def __repr__(self) -> str:
        return self.__str__()


if __name__ == "__main__":
    import numpy as np

    def write_artifacts(artifact, filename):
        with open(filename, "w") as f:
            f.write(str(artifact))

    np.random.seed(0)

    # 3.1

    A = Matrix(np.random.randint(0, 10, (10, 10)))
    B = Matrix(np.random.randint(0, 10, (10, 10)))

    write_artifacts(A + B, "artifacts/3.1/matrix+.txt")
    write_artifacts(A * B, "artifacts/3.1/matrix*.txt")
    write_artifacts(A @ B, "artifacts/3.1/matrix@.txt")

    # 3.3

    A = Matrix([[1, 5], [3, 8]])
    B = D = Matrix([[1, 0], [0, 1]])
    C = Matrix([[9, 4], [2, 2]])

    write_artifacts(A, "artifacts/3.3/A.txt")
    write_artifacts(B, "artifacts/3.3/B.txt")
    write_artifacts(C, "artifacts/3.3/C.txt")
    write_artifacts(D, "artifacts/3.3/D.txt")
    write_artifacts(A @ B, "artifacts/3.3/AB.txt")
    write_artifacts(C @ D, "artifacts/3.3/CD.txt")
    write_artifacts(f"{hash(A @ B)}\n{hash(C @ D)}", "artifacts/3.3/hash.txt")
