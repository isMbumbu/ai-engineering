"""A first look at vectors and the dot product."""

import numpy as np


def main() -> None:
    a = np.array([1.0, 2.0, 3.0])
    b = np.array([4.0, 5.0, 6.0])

    print("Vector a:", a)
    print("Vector b:", b)
    print("a + b:", a + b)
    print("a · b:", np.dot(a, b))
    print("||a||:", np.linalg.norm(a))


if __name__ == "__main__":
    main()
