
import shiboken2 as Shiboken

import typing

class Object: ...


_T = typing.TypeVar("_T", bound="Shiboken.Object")

def isValid(arg__1: typing.Any) -> bool:
    ...

def invalidate(arg__1: Shiboken.Object) -> None:
    ...

def wrapInstance(arg__1: int, arg__2: typing.Type[_T]) -> _T:
    ...

def getCppPointer(arg__1: Shiboken.Object) -> tuple[int, ...]:
    ...

def delete(arg__1: Shiboken.Object) -> None:
    ...

def ownedByPython(arg__1: Shiboken.Object) -> bool:
    ...

def createdByPython(arg__1: Shiboken.Object) -> bool:
    ...

def dump(arg__1: typing.Any) -> str:
    ...

def getAllValidWrappers() -> list[Shiboken.Object]:
    ...


