from typing import Dict, Optional, Union

import pathlib, json

import libcst as cst

JSON_INPUT_FNAME = pathlib.Path(__file__).parent / 'qflags-types.json'

def fqn_names_match(collected_type: str, declared_type: str, mod_name: str) -> bool:
    '''Return whether two fqn names match:
    PySide2.QtCore.QAbstractModel <-> PySide2.QtCore.QAbstractModel   => True
    PySide2.QtCore.QAbstractModel <-> QtCore.QAbstractModel   => True
    PySide2.QtCore.QAbstractModel <-> QAbstractModel + mod_name=QtCore   => True
    PySide2.QtCore.QAbstractModel <-> QAbstractModel + mod_name=QtGui   => False
    PySide2.QtCore.QAbstractModel <-> QtGui.QAbstractModel   => False
    '''
    # both start with PySide2 -> direct comparison
    if collected_type.startswith('PySide2.') and declared_type.startswith('PySide2.'):
        return collected_type == declared_type

    if collected_type.startswith('PySide2.'):
        collected_type = collected_type.split('PySide2.')[1]

    if not collected_type.startswith(mod_name + '.'):
        # not the same module!
        return False

    # both start with module name -> direct comparison
    if declared_type.startswith(mod_name + '.'):
        return collected_type == declared_type

    return collected_type == f'{mod_name}.{declared_type}'


def strip_pyside2_modname(str_type: str, mod_name: str) -> str:
    if str_type.startswith(('PySide2.')):
        str_type = str_type.split('PySide2.', 1)[1]

    if str_type.startswith(f'{mod_name}.'):
        str_type = str_type.split(f'{mod_name}.', 1)[1]

    return str_type


def auto_test():
    assert fqn_names_match('PySide2.QtCore.QAbstractModel', 'PySide2.QtCore.QAbstractModel', 'QtCore')  == True
    assert fqn_names_match('PySide2.QtCore.QAbstractModel', 'QtCore.QAbstractModel', 'QtCore')  == True
    assert fqn_names_match('PySide2.QtCore.QAbstractModel', 'QAbstractModel', 'QtCore')  == True
    assert fqn_names_match('PySide2.QtCore.QAbstractModel', 'QAbstractModel', 'QtGui')  == False
    assert fqn_names_match('PySide2.QtCore.QAbstractModel', 'QtGui.QAbstractModel', 'QtGui')  == False

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


    def leave_AnnAssign(self, original_node: cst.AnnAssign, updated_node: cst.AnnAssign) -> cst.AnnAssign:
        fqn_attr = '.'.join(self.full_name_stack + [original_node.target.value])
        # print(original_node)

        try:
            collected_type = self.fqn_attr_to_type[fqn_attr]
        except KeyError:
            print(f'No collected type for:{fqn_attr}')
            return updated_node

        declared_type = cst.helpers.get_full_name_for_node(original_node.annotation.annotation)
        if not fqn_names_match(collected_type, declared_type, self.mod_name):
            simple_type = strip_pyside2_modname(collected_type, self.mod_name)
            print(f'  Changing {fqn_attr}: {declared_type} -> {simple_type}')
            return updated_node.with_changes(
                annotation=updated_node.annotation.with_changes(
                    annotation=cst.parse_expression(simple_type)
                )
            )
        return updated_node


    def leave_ClassDef(self, original_node: cst.ClassDef, updated_node: cst.ClassDef) \
            -> Union[cst.BaseStatement, cst.FlattenSentinel[cst.BaseStatement], cst.RemovalSentinel, ]:
        """Remove a class from the stack and return the updated node."""
        self.full_name_stack.pop()
        return updated_node



def apply_qflags_types_for_module(module_path: str, d: Dict[str, str]) -> None:
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
        apply_qflags_types_for_module(fpath, d)



if __name__ == '__main__':
    # auto_test()
    main()
