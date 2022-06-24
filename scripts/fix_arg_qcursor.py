from typing import Dict, Optional, Union

import pathlib, json

import libcst as cst

from scripts.utils import resolve_cst_attr

JSON_OUTPUT_FNAME = pathlib.Path(__file__).parent / 'args-qcursor.json'

def fix_args_qcursor_for_module(module_path: pathlib.Path, d: Dict[str, str]) -> None:
    '''Load module, inspect all QFlags types and fill dict with the information'''
    module_name = module_path.stem
    if module_name.startswith('_'):
        return

    print('Processing %s' % module_name)
    if module_name.startswith('_'):
        return

    with open(module_path, "r", encoding="utf-8") as fhandle:
        stub_tree = cst.parse_module(fhandle.read())

    transformer = TypingTransformer(module_name, d)
    modified_tree = stub_tree.visit(transformer)

    with open(module_path, "w", encoding="utf-8") as fhandle:
        fhandle.write(modified_tree.code)


def self_test():
    assert resolve_cst_attr(cst.parse_expression('PySide2.QtGui.QCursor')) == 'PySide2.QtGui.QCursor'
    assert resolve_cst_attr(cst.parse_expression('PySide2.QtGui.QCursor  ')) == 'PySide2.QtGui.QCursor'
    assert resolve_cst_attr(cst.parse_expression('Union[PySide2.QtGui.QCursor] ')) == 'Union[PySide2.QtGui.QCursor]'
    assert resolve_cst_attr(cst.parse_expression('Union[PySide2.QtGui.QCursor ] ')) == 'Union[PySide2.QtGui.QCursor]'
    assert resolve_cst_attr(cst.parse_expression('Union[PySide2.QtGui.QCursor, aa.bb ] ')) == 'Union[PySide2.QtGui.QCursor, aa.bb]'
    print('Self-test: OK')


class TypingTransformer(cst.CSTTransformer):
    """TypingTransformer that visits classes and methods."""

    def __init__(self, mod_name: str, d: Dict[str, str]) -> None:
        super().__init__()
        self.full_name_stack = [mod_name]
        self.d = d

    def fqn_name(self) -> str:
        return '.'.join(self.full_name_stack)


    def visit_ClassDef(self, node: cst.ClassDef) -> Optional[bool]:
        """Put a class on top of the stack when visiting."""
        self.full_name_stack.append( node.name.value )
        return True

    def visit_FunctionDef(self, node: cst.FunctionDef) -> Optional[bool]:
        # search for all arguments with type annotation
        self.full_name_stack.append( node.name.value )


    def leave_FunctionDef(self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef) -> None:
        fqn_name = self.fqn_name()
        self.full_name_stack.pop()

        for i, param in enumerate(updated_node.params.params):
            fqn_param = '%s().%s' % (fqn_name, param.name.value)
            fqn_annotation = ''
            if param.annotation:
                fqn_annotation = resolve_cst_attr(param.annotation.annotation)
            if (fqn_annotation == 'PySide2.QtGui.QCursor'):
                self.d['collected'][fqn_param] = 'QCursor'
                # print('Node before: ', updated_node)
                print('Fixing: ', fqn_param, fqn_annotation)
                updated_node = updated_node.with_changes(
                                    params=updated_node.params.with_changes(
                                            params=updated_node.params.params[:i]
                                            + (updated_node.params.params[i].with_changes(annotation=cst.Annotation(annotation=cst.parse_expression('Union[PySide2.QtGui.QCursor, PySide2.QtCore.Qt.CursorShape]'))),)
                                            + updated_node.params.params[i+1:]
                    )
                )
                # print('Node after: ', updated_node)
                self.d['fixed'][fqn_param] = 'QCursor'

        return updated_node



    def leave_ClassDef(self, original_node: cst.ClassDef, updated_node: cst.ClassDef) \
            -> Union[cst.BaseStatement, cst.FlattenSentinel[cst.BaseStatement], cst.RemovalSentinel,]:
        """Remove a class from the stack and return the updated node."""
        self.full_name_stack.pop()
        return updated_node




def main():
    # from PySide2 import Qt3DCore
    # OneFlagClass = Qt3DCore.Qt3DCore.ChangeFlag
    # MultiFlagClass = Qt3DCore.Qt3DCore.ChangeFlags
    # check_qflag_behavior(OneFlagClass, MultiFlagClass)

    d = {
        'collected' : {},
        'fixed': {}
    }
    for fpath in (pathlib.Path(__file__).parent.parent / 'PySide2-stubs').glob('*.pyi'):
        fix_args_qcursor_for_module(fpath, d)

    with open(JSON_OUTPUT_FNAME, 'w') as f:
        json.dump(d, f, indent=4)



if __name__ == '__main__':
    # self_test()
    main()
