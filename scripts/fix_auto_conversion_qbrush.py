import pathlib, json

from scripts.utils import fix_auto_conversion_for_module

JSON_OUTPUT_FNAME = pathlib.Path(__file__).parent / 'auto-conversion-qbrush.json'


def main():

    d = {
        'collected' : {},
        'fixed': {}
    }
    target_annotation = 'PySide2.QtGui.QBrush'
    replacement_annotation = 'Union[PySide2.QtGui.QBrush, PySide2.QtGui.QColor]'
    for fpath in (pathlib.Path(__file__).parent.parent / 'PySide2-stubs').glob('*.pyi'):
        fix_auto_conversion_for_module(fpath, d, target_annotation, replacement_annotation)

    with open(JSON_OUTPUT_FNAME, 'w') as f:
        json.dump(d, f, indent=4)



if __name__ == '__main__':
    main()
