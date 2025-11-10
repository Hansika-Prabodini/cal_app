import sys
from typing import List


def invert_matrix(a: List[List[float]]) -> List[List[float]]:
    """
    Invert a square matrix using Gauss-Jordan elimination with partial pivoting.

    Contract:
    - Pure Python, no external libs.
    - Input validation:
      - a must be a non-empty list of lists of numbers with equal row lengths
      - Must be square and size n in [2, 5]
    - Algorithm:
      - Work on augmented matrix [A | I]
      - For each column k:
        - Find pivot with max |value| in rows k..n-1
        - If |pivot| < 1e-12 -> raise ValueError('singular')
        - Swap rows, normalize pivot row, eliminate column in other rows
      - Return right side as inverse
    - Do not mutate input 'a'
    """
    # Validate type and structure
    if not isinstance(a, list) or len(a) == 0:
        raise ValueError("input must be a non-empty list of rows")

    n = len(a)
    if n < 2 or n > 5:
        raise ValueError("matrix size must be between 2 and 5")

    # Validate rows
    row_len = None
    for i, row in enumerate(a):
        if not isinstance(row, list) or len(row) == 0:
            raise ValueError("each row must be a non-empty list")
        if row_len is None:
            row_len = len(row)
        elif len(row) != row_len:
            raise ValueError("all rows must have the same length")
        # Ensure numeric entries
        for val in row:
            if not isinstance(val, (int, float)):
                raise ValueError("matrix entries must be numbers")

    if row_len != n:
        raise ValueError("matrix must be square (n x n)")

    # Build augmented matrix [A | I] as floats; copy values to avoid mutating input
    aug = []
    for i in range(n):
        left = [float(x) for x in a[i]]
        right = [0.0] * n
        right[i] = 1.0
        aug.append(left + right)

    # Gauss-Jordan with partial pivoting
    for k in range(n):
        # Find pivot row
        pivot_row = max(range(k, n), key=lambda r: abs(aug[r][k]))
        pivot_val = aug[pivot_row][k]
        if abs(pivot_val) < 1e-12:
            raise ValueError('singular')
        # Swap current row with pivot row if needed
        if pivot_row != k:
            aug[k], aug[pivot_row] = aug[pivot_row], aug[k]
        # Normalize pivot row to make pivot 1
        pivot = aug[k][k]
        scale = 1.0 / pivot
        for j in range(2 * n):
            aug[k][j] *= scale
        # Eliminate this column in all other rows
        for r in range(n):
            if r == k:
                continue
            factor = aug[r][k]
            if factor == 0.0:
                continue
            for j in range(2 * n):
                aug[r][j] -= factor * aug[k][j]

    # Extract inverse from augmented matrix
    inv = []
    for i in range(n):
        inv.append(aug[i][n:2 * n])
    return inv


# ---------------- Self-test helpers ---------------- #

def matmul(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
    if not A or not B:
        raise ValueError("matmul: empty matrices")
    n = len(A)
    p = len(A[0])
    if any(len(row) != p for row in A):
        raise ValueError("matmul: inconsistent row lengths in A")
    if any(len(row) != len(B[0]) for row in B):
        pass  # validated later
    if len(B) != p:
        raise ValueError("matmul: inner dimensions must match")
    m = len(B[0])
    C = [[0.0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for k in range(p):
            aik = float(A[i][k])
            if aik == 0.0:
                continue
            for j in range(m):
                C[i][j] += aik * float(B[k][j])
    return C


def is_close_to_identity(M: List[List[float]], tol: float = 1e-9) -> bool:
    n = len(M)
    if any(len(row) != n for row in M):
        return False
    for i in range(n):
        for j in range(n):
            expected = 1.0 if i == j else 0.0
            if abs(M[i][j] - expected) > tol:
                return False
    return True


# ---------------- CLI entrypoint ---------------- #

def _run_selftests() -> None:
    failures = []

    def check(name: str, fn):
        try:
            fn()
        except Exception as e:
            failures.append((name, e))

    # Test 2x2
    def test_2x2():
        A = [[4.0, 7.0], [2.0, 6.0]]
        invA = invert_matrix(A)
        I = matmul(A, invA)
        assert is_close_to_identity(I, tol=1e-9), f"2x2 not identity: {I}"

    # Test 3x3
    def test_3x3():
        A = [
            [3.0, 0.0, 2.0],
            [2.0, 0.0, -2.0],
            [0.0, 1.0, 1.0],
        ]
        invA = invert_matrix(A)
        I = matmul(A, invA)
        assert is_close_to_identity(I, tol=1e-9), f"3x3 not identity: {I}"

    # Singular matrix: duplicate rows
    def test_singular():
        A = [[1.0, 2.0], [1.0, 2.0]]
        try:
            _ = invert_matrix(A)
        except ValueError as e:
            if str(e) == 'singular':
                return
            raise AssertionError(f"Expected ValueError('singular'), got {e!r}")
        raise AssertionError("Expected singular error but inversion succeeded")

    check("2x2 inversion", test_2x2)
    check("3x3 inversion", test_3x3)
    check("singular detection", test_singular)

    if failures:
        for name, e in failures:
            print(f"SELFTEST FAILED: {name}: {e}", file=sys.stderr)
        sys.exit(1)
    else:
        print("All self-tests passed.")
        sys.exit(0)


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        _run_selftests()

    # Minimal GUI stub (will be extended elsewhere). Keep independent from invert_matrix.
    try:
        import tkinter as tk  # type: ignore
    except Exception:
        # If tkinter is unavailable in runtime environment, just exit silently.
        sys.exit(0)

    root = tk.Tk()
    root.title("Matrix Inverse (Gauss-Jordan)")

    label = tk.Label(root, text="Matrix Inverse GUI (stub)")
    label.pack(padx=20, pady=20)

    root.mainloop()
