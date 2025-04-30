import ast
import re
from python_repr import PythonREPL


_jm_for_statement_check = """In JijModeling, you cannot use Python loops directly. Instead, you should use the Element objects.

# How to write summation in JijModeling without Python loops.

The wrong code:
```python
objective = 0
for l in range(n_l):
    for t in range(n_t):
        for p in range(n_p):
            for q in range(n_p):
                if p != q:
                    objective += ChangeCost[p, q] * Switch[p, q, l, t]
```

The correct code:
```
l = jm.Element("l", belongs_to=range(0, n_l))
t = jm.Element("t", belongs_to=range(0, n_t))
p = jm.Element("p", belongs_to=range(0, n_p))
q = jm.Element("q", belongs_to=range(0, n_p))
objective = jm.sum([l, t, p, (q, p != q)], ChangeCost[p, q] * Switch[p, q, l, t])
```

# How to write forall in JijModeling without Python loops.

The wrong code:
```python
for l in range(n_l):
    for t in range(n_t):
        problem += jm.Constraint(
            "SingleProductPerLine",
            jm.sum([X[p, l, t] for p in range(n_p)]) <= 1,
            forall=[]
        )
```

The correct code:
```python
l = jm.Element("l", belongs_to=range(0, n_l))
t = jm.Element("t", belongs_to=range(0, n_t))
p = jm.Element("p", belongs_to=range(0, n_p))
problem += jm.Constraint(
    "SingleProductPerLine",
    jm.sum(p, X[p, l, t]) <= 1,
    forall=[l, t]
)
```
"""


def jijmodeling_check(code_string: str) -> dict:
    """
    Pythonコード文字列をJijModelingのルールに従ってチェックする関数

    Args:
        code_string (str): 解析対象のPythonコード文字列

    Returns:
        dict: チェック結果を含む辞書
    """
    # for文の検出
    for_loop_detected = detect_for_loop(code_string)
    if for_loop_detected:
        return {
            "for_loop_detected": True,
            "message": _jm_for_statement_check,
        }

    # PythonREPLを使用してコードを実行し、エラーをキャッチ
    result = PythonREPL.run(code_string)

    if result["status"] == "error":
        return {
            "for_loop_detected": False,
            "message": _jm_for_statement_check,
            "error": result["error"],
        }

    return {
        "for_loop_detected": False,
        "message": "No for loop detected and no errors found.",
    }


def detect_for_loop(code_string):
    """
    Pythonコード文字列からfor文の存在を検出する関数

    Args:
        code_string (str): 解析対象のPythonコード文字列

    Returns:
        bool: for文が存在する場合はTrue、存在しない場合はFalse
    """
    # 方法1: ASTを使用した解析（構文的に正しいコードの場合）
    try:
        tree = ast.parse(code_string)
        for node in ast.walk(tree):
            if isinstance(node, ast.For):
                return True
    except SyntaxError:
        # 構文エラーがある場合は正規表現による検出に進む
        pass

    # 方法2: 正規表現を使用した解析（ASTが適用できない場合のバックアップ）
    # for文の正規表現パターン: 'for'の後にスペースまたはタブ、その後に変数名、'in'が続く形式
    pattern = r"\bfor\s+[a-zA-Z_][a-zA-Z0-9_]*\s+in\b"

    if re.search(pattern, code_string):
        return True

    return False
