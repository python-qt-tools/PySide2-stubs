from typing import Union

import libcst as cst


def resolve_cst_attr(node: Union[cst.Name, cst.Attribute, cst.Subscript, cst.SubscriptElement, cst.Index]) -> str:
    '''Return a string from an annotation node'''
    if isinstance(node, cst.Name):
        return node.value

    if isinstance(node, cst.Attribute):
        return f'{resolve_cst_attr(node.value)}.{resolve_cst_attr(node.attr)}'

    if isinstance(node, cst.Subscript):
        return f'{resolve_cst_attr(node.value)}[{", ".join(resolve_cst_attr(el) for el in node.slice)}]'

    if isinstance(node, cst.SubscriptElement):
        return resolve_cst_attr(node.slice)

    if isinstance(node, cst.Index):
        return resolve_cst_attr(node.value)

    if isinstance(node, cst.SimpleString):
        return node.value

    if isinstance(node, cst.Call):
        return f'{resolve_cst_attr(node.func)}({", ".join(resolve_cst_attr(arg) for arg in node.args)})'

    if isinstance(node, cst.Arg):
        return resolve_cst_attr(node.value)

    raise ValueError('Unknown type: ', type(node))