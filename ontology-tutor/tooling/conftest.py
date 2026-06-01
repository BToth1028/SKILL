from __future__ import annotations

from typing import Any


def pytest_pyfunc_call(pyfuncitem: Any) -> bool | None:
    if pyfuncitem.module.__name__ != "test_load_typedb_snapshot_search":
        return None

    result: Any = pyfuncitem.obj()
    if result is False:
        raise AssertionError(f"{pyfuncitem.name} returned False")
    if result not in (None, True):
        raise AssertionError(
            f"{pyfuncitem.name} returned unsupported value {result!r}"
        )
    return True
