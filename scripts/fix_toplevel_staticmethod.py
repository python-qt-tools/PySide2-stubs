import pathlib, re

def fix_toplevel_staticmethod(fpath: pathlib.Path, target_decorator: str, replacement: str) -> None:
    print(f'Processing {fpath}')

    with open(fpath) as f:
        flines = f.readlines()

    target_re = re.compile(target_decorator)

    for i in range(len(flines)):
        if target_re.match(flines[i]):
            print(f'- line {i}, replacing {target_decorator}')
            flines[i] = replacement

    with open(fpath, 'w') as f:
        f.writelines(flines)


def main():
    target_decorator = r'^@staticmethod\s*$'
    replacement = '\n'
    for fpath in (pathlib.Path(__file__).parent.parent / 'PySide2-stubs').glob('*.pyi'):
        fix_toplevel_staticmethod(fpath, target_decorator, replacement)


if __name__ == '__main__':
    main()
