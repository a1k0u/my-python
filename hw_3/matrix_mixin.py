import numpy as np


class StrMixin:
    def __str__(self):
        return str(self.matrix)


class WriteToFileMixin:
    def write_to_file(self, filename) -> None:
        with open(filename, "w") as file:
            file.write(str(self))


class SetterGetterMixin:
    def __get__(self):
        return self.matrix

    def __set__(self, matrix):
        self.matrix = matrix


class MatrixMixin(
    np.lib.mixins.NDArrayOperatorsMixin, SetterGetterMixin, WriteToFileMixin, StrMixin
):
    def __init__(self, matrix):
        self.matrix = np.asarray(matrix)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        out = kwargs.get("out", None)

        inputs = tuple(x.matrix if isinstance(x, MatrixMixin) else x for x in inputs)

        return MatrixMixin(getattr(ufunc, method)(*inputs, out=out, **kwargs))


if __name__ == "__main__":
    import numpy as np

    np.random.seed(0)

    A = MatrixMixin(np.random.randint(0, 10, (10, 10)))
    B = MatrixMixin(np.random.randint(0, 10, (10, 10)))

    (A + B).write_to_file("artifacts/3.2/matrix+.txt")
    (A * B).write_to_file("artifacts/3.2/matrix*.txt")
    (A @ B).write_to_file("artifacts/3.2/matrix@.txt")
