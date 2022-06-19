from typing import Dict, Optional, Union

import pathlib, json

import libcst as cst
import libcst.matchers as matchers

JSON_INPUT_FNAME = pathlib.Path(__file__).parent / 'qflags-behavior.json'

class TypingTransformer(cst.CSTTransformer):
    """TypingTransformer that visits classes and methods."""

    def __init__(self, mod_name: str, d: Dict[str, str]) -> None:
        super().__init__()
        self.mod_name = mod_name
        self.full_name_stack = [mod_name]
        self.fqn_attr_to_type = d
        self.annotation = []


    def visit_ClassDef(self, node: cst.ClassDef) -> Optional[bool]:
        """Put a class on top of the stack when visiting."""
        self.full_name_stack.append( node.name.value )
        return True


    def leave_ClassDef(self, original_node: cst.ClassDef, updated_node: cst.ClassDef) \
            -> Union[cst.BaseStatement, cst.FlattenSentinel[cst.BaseStatement], cst.RemovalSentinel, ]:
        """Remove a class from the stack and return the updated node."""
        fqn_class = '.'.join(self.full_name_stack)
        self.full_name_stack.pop()

        if not fqn_class in self.fqn_attr_to_type:
            return updated_node

        flagType, oneFlagClassName, multiFlagClassName = self.fqn_attr_to_type[fqn_class]
        return self.add_missing_methods(updated_node, flagType, oneFlagClassName, multiFlagClassName)


    def add_missing_methods(self, updated_node: cst.ClassDef, flagType: str, oneFlagClassName: str, multiFlagClassName: str) \
            -> Union[cst.BaseStatement, cst.FlattenSentinel[cst.BaseStatement], cst.RemovalSentinel,]:

        methods_of_oneFlag = {
            '__index__':    f'def __index__(self) -> int: ...',
            '__init__':     f'def __init__(self, value: typing.Union[int, {oneFlagClassName}] = ...) -> None: ...',
            '__or__':       f'def __or__(self, other: typing.Union[int, {oneFlagClassName}]) -> {multiFlagClassName}: ...',
            '__and__':      f'def __and__(self, other: typing.Union[int, {oneFlagClassName}]) -> {multiFlagClassName}: ...',
            '__xor__':      f'def __xor__(self, other: typing.Union[int, {oneFlagClassName}]) -> {multiFlagClassName}: ...',
            '__ror__':      f'def __ror__(self, other: typing.Union[int, {oneFlagClassName}]) -> {multiFlagClassName}: ...',
            '__rand__':     f'def __rand__(self, other: typing.Union[int, {oneFlagClassName}]) -> {multiFlagClassName}: ...',
            '__rxor__':     f'def __rxor__(self, other: typing.Union[int, {oneFlagClassName}]) -> {multiFlagClassName}: ...',
            '__ior__':      f'def __ior__(self, other: typing.Union[int, {oneFlagClassName}]) -> {multiFlagClassName}: ...',
            '__iand__':     f'def __iand__(self, other: typing.Union[int, {oneFlagClassName}]) -> {multiFlagClassName}: ...',
            '__ixor__':     f'def __ixor__(self, other: typing.Union[int, {oneFlagClassName}]) -> {multiFlagClassName}: ...',
            '__invert__':   f'def __invert__(self) -> {multiFlagClassName}: ...',
        }

        methods_of_multiFlag = {
            '__index__':    f'def __index__(self) -> int: ...',
            '__init__':     f'def __init__(self, value: typing.Union[int, {oneFlagClassName}, {multiFlagClassName}] = ...) -> None: ...',
            '__or__':       f'def __or__(self, other: typing.Union[int, {oneFlagClassName}, {multiFlagClassName}]) -> {multiFlagClassName}: ...',
            '__and__':      f'def __and__(self, other: typing.Union[int, {oneFlagClassName}, {multiFlagClassName}]) -> {multiFlagClassName}: ...',
            '__xor__':      f'def __xor__(self, other: typing.Union[int, {oneFlagClassName}, {multiFlagClassName}]) -> {multiFlagClassName}: ...',
            '__ror__':      f'def __ror__(self, other: typing.Union[int, {oneFlagClassName}, {multiFlagClassName}]) -> {multiFlagClassName}: ...',
            '__rand__':     f'def __rand__(self, other: typing.Union[int, {oneFlagClassName}, {multiFlagClassName}]) -> {multiFlagClassName}: ...',
            '__rxor__':     f'def __rxor__(self, other: typing.Union[int, {oneFlagClassName}, {multiFlagClassName}]) -> {multiFlagClassName}: ...',
            '__ior__':      f'def __ior__(self, other: typing.Union[int, {oneFlagClassName}, {multiFlagClassName}]) -> {multiFlagClassName}: ...',
            '__iand__':     f'def __iand__(self, other: typing.Union[int, {oneFlagClassName}, {multiFlagClassName}]) -> {multiFlagClassName}: ...',
            '__ixor__':     f'def __ixor__(self, other: typing.Union[int, {oneFlagClassName}, {multiFlagClassName}]) -> {multiFlagClassName}: ...',
            '__invert__':   f'def __invert__(self) -> {multiFlagClassName}: ...',
        }

        methods_of_qflag = methods_of_oneFlag if flagType == 'OneFlag' else methods_of_multiFlag

        # find method not already defined
        methods_to_add = tuple(
            cst.parse_statement(method_def)
            for method, method_def in methods_of_qflag.items()
            if not len(matchers.findall(updated_node.body, matchers.FunctionDef(name=matchers.Name(method))))
        )

        if not methods_to_add:
            return updated_node

        if isinstance(updated_node.body, cst.SimpleStatementSuite):
            # class is defined on one line:
            # "class Toto: ...
            # create an indented body
            updated_node = updated_node.with_changes(body=cst.IndentedBlock(body=()))

        # if they are not, add them to updated_node
        return updated_node.with_changes(
            body=updated_node.body.with_changes(
                body=updated_node.body.body + (methods_to_add[0].with_changes(leading_lines=(cst.EmptyLine(),)),) + methods_to_add[1:]
            ))


def apply_qflags_behavior_for_module(module_path: str, d: Dict[str, str]) -> None:
    if module_path.name.startswith('_'):
        return

    module_name = module_path.stem

    print('Fixing ', module_name)
    with open(module_path, "r", encoding="utf-8") as fhandle:
        stub_tree = cst.parse_module(fhandle.read())

    transformer = TypingTransformer(module_name, d)
    modified_tree = stub_tree.visit(transformer)

    with open(module_path, "w", encoding="utf-8") as fhandle:
        fhandle.write(modified_tree.code)


def main():
    with open(JSON_INPUT_FNAME, 'r') as f:
        d = json.load(f)

    for fpath in (pathlib.Path(__file__).parent.parent / 'PySide2-stubs').glob('*.pyi'):
        apply_qflags_behavior_for_module(fpath, d)



if __name__ == '__main__':
    # auto_test()
    main()
