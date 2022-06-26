import pathlib, json

from scripts.utils import fix_auto_conversion_for_module

JSON_OUTPUT_FNAME = pathlib.Path(__file__).parent / 'auto-conversion-qcursor.json'


def main():

    d = {
        'collected' : {},
        'fixed': {}
    }
    target_annotation = 'PySide2.QtGui.QCursor'
    replacement_annotation = 'Union[PySide2.QtGui.QCursor, PySide2.QtCore.Qt.CursorShape]'
    for fpath in (pathlib.Path(__file__).parent.parent / 'PySide2-stubs').glob('*.pyi'):
        fix_auto_conversion_for_module(fpath, d, target_annotation, replacement_annotation)

    with open(JSON_OUTPUT_FNAME, 'w') as f:
        json.dump(d, f, indent=4)



if __name__ == '__main__':
    # self_test()
    main()
