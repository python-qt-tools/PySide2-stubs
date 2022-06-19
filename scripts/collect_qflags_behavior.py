from typing import Union, Callable, TypeVar, Dict, Type

import pathlib, importlib, json

import pytest

JSON_OUTPUT_FNAME = pathlib.Path(__file__).parent / 'qflags-behavior.json'

def collect_qflags_behavior_for_module(module_name: str, d: Dict[str, str]) -> None:
    '''Load module, inspect all QFlags types and fill dict with the information'''
    if module_name.startswith('_'):
        return

    print('Processing %s' % module_name)
    try:
        m = importlib.import_module(f'PySide2.{module_name}')
    except ModuleNotFoundError:
        print('... Module not available!')
        # platform-specific modules can not be imported for example on other platforms
        return

    for class_name, class_type in m.__dict__.items():
        if class_name.startswith('_'):
            continue

        collect_qflags_behavior_for_class(f'{module_name}.{class_name}', class_type, d)


def collect_qflags_behavior_for_class(class_fqn: str, class_type: Type, d: Dict[str, str]) -> None:
    # we only care about classes
    if not str(type(class_type)).startswith('<class '):
        return

    try:
        class_members = class_type.__dict__.items()
    except AttributeError:
        # this is not a class
        return

    for class_attr_name, class_attr_value in class_members:
        if class_attr_name.startswith('_'):
            continue

        # tricky way to find an instance of Shiboken.EnumType
        class_type = class_attr_value.__class__
        attr_fqn = f'{class_fqn}.{class_attr_name}'
        if str(class_type.__class__) == "<class 'Shiboken.EnumType'>":
            verify_qflags_behavior_for_attr(attr_fqn, class_type, d)
        else:
            collect_qflags_behavior_for_class(attr_fqn, class_attr_value, d)


def verify_qflags_behavior_for_attr(attr_fqn, class_type, d) -> None:
    v = class_type(1)
    if isinstance(v | v, int):
        # this is not a combining flag, the a regular enum
        # we don't really care at this point to declare all operations
        return

    MultiFlagClass = (v | v).__class__
    check_qflag_behavior(class_type, MultiFlagClass)
    multi_flag_fqn = '.'.join(attr_fqn.split('.')[:-1] + [MultiFlagClass.__name__])
    one_flag_fqn = '.'.join(attr_fqn.split('.')[:-1] + [class_type.__name__])
    d[one_flag_fqn] = ('OneFlag', class_type.__name__, MultiFlagClass.__name__)
    d[multi_flag_fqn] = ('MultiFlag', class_type.__name__, MultiFlagClass.__name__)



def assert_type_of_value_int(value: int) -> None:
    '''Raise an exception if the value is not of type expected_type'''
    assert isinstance(value, int)
    assert type(value) == type(123)


OneFlagClassT = TypeVar('OneFlagClassT')
MultiFlagClassT = TypeVar('MultiFlagClassT')

def gen_assert_type_of_value_oneFlag(OneFlagClass: OneFlagClassT) -> Callable[[OneFlagClassT], None]:
    def assert_type_of_value_oneFlag(value: OneFlagClass) -> None:
        '''Raise an exception if the value is not of type expected_type'''
        assert type(value) == OneFlagClass

    return assert_type_of_value_oneFlag


def gen_assert_type_of_value_multiFlag(MultiFlagClass: MultiFlagClassT) -> Callable[[MultiFlagClassT], None]:
    '''Raise an exception if the value is not of type expected_type'''

    def assert_type_of_value_multiFlag(value: MultiFlagClass) -> None:
        assert type(value) == MultiFlagClass

    return assert_type_of_value_multiFlag



def check_one_flag_class_behavior(OneFlagClass,
                                  MultiFlagClass,
                                  oneFlagRefValue1,
                                  oneFlagRefValue2,
                                  assert_type_of_value_oneFlag,
                                  assert_type_of_value_multiFlag,
                                  ) -> None:
    '''Verify the standard behavior of a QFlag class OneFlagClass'''
    oneFlagValue1 = oneFlagRefValue1
    oneFlagValue2 = oneFlagRefValue2
    oneFlagValueTest: OneFlagClass = oneFlagValue1
    intValue = 0                    # type: int
    oneOrMultiFlagValueTest: Union[OneFlagClass, MultiFlagClass] = oneFlagValue1
    oneFlagOrIntValue: Union[int, OneFlagClass] = oneFlagValue1

    # upcast from OneFlagClass to int is forbidden
    intValue = oneFlagValue1		# type: ignore[assignment]

    # conversion works
    intValue = int(oneFlagValue1)

    # this is not supported type-safely for a good reason
    oneFlagValueTest = 1		# type: ignore

    # correct way to do it
    oneFlagValueTest = OneFlagClass()
    oneFlagValueTest = OneFlagClass(1)
    oneFlagValueTest = OneFlagClass(oneFlagValue1)

    # The rules of OneFlagClass conversion defined in PyQt5 are:
    # 1. | ~= with OneFlagClass return a MultiFlagClass (which is not compatible to int)
    #   Note that this breaks Liskov principle
    # 2. everything else returns int: & ^ &= ^=
    # 3. operations with int return int.

    assert_type_of_value_multiFlag(oneFlagValue1 | oneFlagValue2)
    assert_type_of_value_multiFlag(oneFlagValue1 & oneFlagValue2)
    assert_type_of_value_multiFlag(oneFlagValue1 ^ oneFlagValue2)
    assert_type_of_value_multiFlag(~oneFlagValue1)

    # right operand int
    assert_type_of_value_multiFlag(oneFlagValue1 | 1)
    assert_type_of_value_multiFlag(oneFlagValue1 & 1)
    assert_type_of_value_multiFlag(oneFlagValue1 ^ 1)

    # left operand int
    assert_type_of_value_multiFlag(1 | oneFlagValue1)
    assert_type_of_value_multiFlag(1 & oneFlagValue1)
    assert_type_of_value_multiFlag(1 ^ oneFlagValue1)

    oneOrMultiFlagValueTest = oneFlagValue1  # reset type and value
    assert_type_of_value_oneFlag(oneOrMultiFlagValueTest)
    oneOrMultiFlagValueTest |= oneFlagValue2
    assert_type_of_value_multiFlag(oneOrMultiFlagValueTest)   # type: ignore[arg-type]	# mypy limitation here

    oneOrMultiFlagValueTest = oneFlagValue1  # reset type and value
    assert_type_of_value_oneFlag(oneOrMultiFlagValueTest)
    oneOrMultiFlagValueTest |= 1
    assert_type_of_value_multiFlag(oneOrMultiFlagValueTest)   # type: ignore[arg-type]	# mypy limitation here

    oneFlagOrIntValue = oneFlagValue1	# reset type and value
    assert_type_of_value_oneFlag(oneFlagOrIntValue)
    oneFlagOrIntValue &= 1
    assert_type_of_value_multiFlag(oneFlagOrIntValue)   # type: ignore[arg-type]	# mypy limitation here

    oneFlagOrIntValue = oneFlagValue1	# reset type and value
    assert_type_of_value_oneFlag(oneFlagOrIntValue)
    oneFlagOrIntValue &= oneFlagValue2
    assert_type_of_value_multiFlag(oneFlagOrIntValue)   # type: ignore[arg-type]	# mypy limitation here

    oneFlagOrIntValue = oneFlagValue1	# reset type and value
    assert_type_of_value_oneFlag(oneFlagOrIntValue)
    oneFlagOrIntValue ^= 1
    assert_type_of_value_multiFlag(oneFlagOrIntValue)   # type: ignore[arg-type]	# mypy limitation here

    oneFlagOrIntValue = oneFlagValue1	# reset type and value
    assert_type_of_value_oneFlag(oneFlagOrIntValue)
    oneFlagOrIntValue ^= oneFlagValue2
    assert_type_of_value_multiFlag(oneFlagOrIntValue)   # type: ignore[arg-type]	# mypy limitation here

    # +/- operations are forbidden
    pytest.raises(TypeError, lambda: oneFlagValue1 + 1)		# type: ignore[operator]
    pytest.raises(TypeError, lambda: oneFlagValue1 - 1)		# type: ignore[operator]
    pytest.raises(TypeError, lambda: 1 + oneFlagValue1)		# type: ignore[operator]
    pytest.raises(TypeError, lambda: 1 - oneFlagValue1)		# type: ignore[operator]



def check_multi_flag_class_behavior(OneFlagClass,
                                  MultiFlagClass,
                                  oneFlagRefValue1,
                                  oneFlagRefValue2,
                                  assert_type_of_value_oneFlag,
                                  assert_type_of_value_multiFlag,
                                  ) -> None:
    '''Verify the standard behavior of a QFlags class MultiFlagClass'''
    oneFlagValue1 = oneFlagRefValue1
    multiFlagValue1 = MultiFlagClass()
    multiFlagValue2 = MultiFlagClass()
    multiFlagValueTest: MultiFlagClass = multiFlagValue1
    intValue = 0

    assert_type_of_value_multiFlag(MultiFlagClass(intValue))
    assert_type_of_value_multiFlag(MultiFlagClass(oneFlagValue1))
    assert_type_of_value_multiFlag(MultiFlagClass(multiFlagValue1))

    assert_type_of_value_oneFlag(oneFlagValue1)
    assert_type_of_value_multiFlag(multiFlagValue1)
    assert_type_of_value_multiFlag(multiFlagValue2)
    assert_type_of_value_multiFlag(multiFlagValueTest)
    assert_type_of_value_int(intValue)


    # MultiFlagClass may be created by combining MultiFlagClass together
    assert_type_of_value_multiFlag( ~multiFlagValue1 )
    assert_type_of_value_multiFlag( multiFlagValue1 | multiFlagValue2 )
    assert_type_of_value_multiFlag( multiFlagValue1 & multiFlagValue2 )
    assert_type_of_value_multiFlag( multiFlagValue1 ^ multiFlagValue2 )


    # MultiFlagClass may be created by combining MultiFlagClass and OneFlagClass, left or right
    assert_type_of_value_multiFlag( multiFlagValue1 | oneFlagValue1 )
    assert_type_of_value_multiFlag( multiFlagValue1 & oneFlagValue1 )
    assert_type_of_value_multiFlag( multiFlagValue1 ^ oneFlagValue1 )

    assert_type_of_value_multiFlag( oneFlagValue1 | multiFlagValue1 )
    assert_type_of_value_multiFlag( oneFlagValue1 & multiFlagValue1 )
    assert_type_of_value_multiFlag( oneFlagValue1 ^ multiFlagValue1 )


    # MultClassFlag may be created by combining MultiFlagClass and int, right only
    assert_type_of_value_multiFlag(multiFlagValue1 | 1)
    assert_type_of_value_multiFlag(multiFlagValue1 & 1)
    assert_type_of_value_multiFlag(multiFlagValue1 ^ 1)

    assert_type_of_value_multiFlag(1 | multiFlagValue1)
    assert_type_of_value_multiFlag(1 & multiFlagValue1)
    assert_type_of_value_multiFlag(1 ^ multiFlagValue1)


    # this is rejected by mypy and is slightly annoying: you can not pass a OneFlagClass variable to a method expecting a MultiFlagClass
    # explicit typing must be used on those methods to accept both OneFlagClass and MultiFlagClass
    multiFlagValueTest = oneFlagValue1   # type: ignore

    # correct way to do it
    multiFlagValueTest = MultiFlagClass(oneFlagValue1)
    assert_type_of_value_multiFlag(multiFlagValueTest)

    # this is rejected for the same reason as for OneFlagClass.
    intValue = multiFlagValueTest      # type: ignore

    # correct way to do it
    intValue = int(multiFlagValueTest)
    assert_type_of_value_int(intValue)

    # rejected by mypy rightfully
    multiFlagValueTest = 1            # type: ignore

    # correct way to do it
    multiFlagValueTest = MultiFlagClass(1)

    # assignments operations with OneFlagClass
    assert_type_of_value_multiFlag(multiFlagValueTest)
    multiFlagValueTest |= oneFlagValue1
    assert_type_of_value_multiFlag(multiFlagValueTest)

    assert_type_of_value_multiFlag(multiFlagValueTest)
    multiFlagValueTest &= oneFlagValue1
    assert_type_of_value_multiFlag(multiFlagValueTest)

    assert_type_of_value_multiFlag(multiFlagValueTest)
    multiFlagValueTest ^= oneFlagValue1
    assert_type_of_value_multiFlag(multiFlagValueTest)

    # assignments operations with int
    assert_type_of_value_multiFlag(multiFlagValueTest)
    multiFlagValueTest |= 1
    assert_type_of_value_multiFlag(multiFlagValueTest)

    assert_type_of_value_multiFlag(multiFlagValueTest)
    multiFlagValueTest &= 1
    assert_type_of_value_multiFlag(multiFlagValueTest)

    assert_type_of_value_multiFlag(multiFlagValueTest)
    multiFlagValueTest ^= 1
    assert_type_of_value_multiFlag(multiFlagValueTest)

    #########################################################1
    #
    #        Exploring errors
    #
    #########################################################1

    # This checks the following:
    # + and - operations are not supported on MultiFlagClass
    # combining int with MultiFlagClass does not work
    pytest.raises(TypeError, lambda: multiFlagValue1 + multiFlagValue2 )	# type: ignore[operator]
    pytest.raises(TypeError, lambda: multiFlagValue1 - multiFlagValue2 )	# type: ignore[operator]
    pytest.raises(TypeError, lambda: multiFlagValue1 + oneFlagValue1)	# type: ignore[operator]
    pytest.raises(TypeError, lambda: multiFlagValue1 - oneFlagValue1)	# type: ignore[operator]
    pytest.raises(TypeError, lambda: multiFlagValue1 + 1)				# type: ignore[operator]
    pytest.raises(TypeError, lambda: multiFlagValue1 - 1)				# type: ignore[operator]
    pytest.raises(TypeError, lambda: oneFlagValue1 + multiFlagValue1)	# type: ignore[operator]
    pytest.raises(TypeError, lambda: oneFlagValue1 - multiFlagValue1)	# type: ignore[operator]
    pytest.raises(TypeError, lambda: 1 + multiFlagValue1)				# type: ignore[operator]
    pytest.raises(TypeError, lambda: 1 - multiFlagValue1)				# type: ignore[operator]

    def f1() -> None:
        multiFlagValueTest = MultiFlagClass()
        multiFlagValueTest += oneFlagValue1	  # type: ignore[operator]
    def f2() -> None:
        multiFlagValueTest = MultiFlagClass()
        multiFlagValueTest += 1	  # type: ignore[operator, assignment]
    def f3() -> None:
        multiFlagValueTest = MultiFlagClass()
        multiFlagValueTest -= oneFlagValue1	  # type: ignore[operator]
    def f4() -> None:
        multiFlagValueTest = MultiFlagClass()
        multiFlagValueTest -= 1	  # type: ignore[operator, assignment]

    pytest.raises(TypeError, f1)
    pytest.raises(TypeError, f2)
    pytest.raises(TypeError, f3)
    pytest.raises(TypeError, f4)


def check_qflag_behavior(OneFlagClass, MultiFlagClass):
    oneFlagRefValue1 = OneFlagClass(1)
    oneFlagRefValue2 = OneFlagClass(2)

    check_one_flag_class_behavior(OneFlagClass, MultiFlagClass, oneFlagRefValue1, oneFlagRefValue2,
                                  gen_assert_type_of_value_oneFlag(OneFlagClass), gen_assert_type_of_value_multiFlag(MultiFlagClass))
    check_multi_flag_class_behavior(OneFlagClass, MultiFlagClass, oneFlagRefValue1, oneFlagRefValue2,
                                  gen_assert_type_of_value_oneFlag(OneFlagClass), gen_assert_type_of_value_multiFlag(MultiFlagClass))

def main():
    # from PySide2 import Qt3DCore
    # OneFlagClass = Qt3DCore.Qt3DCore.ChangeFlag
    # MultiFlagClass = Qt3DCore.Qt3DCore.ChangeFlags
    # check_qflag_behavior(OneFlagClass, MultiFlagClass)

    d = {}
    for fpath in (pathlib.Path(__file__).parent.parent / 'PySide2-stubs').glob('*.pyi'):
        module_name = fpath.stem
        collect_qflags_behavior_for_module(module_name, d)

    with open(JSON_OUTPUT_FNAME, 'w') as f:
        json.dump(d, f, indent=4)



if __name__ == '__main__':
    main()
