from typing import Dict, Type

import importlib, json, pathlib

JSON_OUTPUT_FNAME = 'qflags-types.json'

def collect_qflags_types_for_module(module_name: str, d: Dict[str, str]) -> None:
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

        collect_qflags_types_for_class(f'{module_name}.{class_name}', class_type, d)

def collect_qflags_types_for_class(class_fqn: str, class_type: Type, d: Dict[str, str]) -> None:
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
        if str(class_type.__class__) == "<class 'Shiboken.EnumType'>":
            attr_fqn = f'{class_fqn}.{class_attr_name}'
            class_type_name = str(class_type).split("'")[1]
            d[attr_fqn] = class_type_name
            # print(attr_fqn, class_type)
        else:
            collect_qflags_types_for_class(f'{class_fqn}.{class_attr_name}', class_attr_value, d)


def main():
    d = {}
    for fpath in (pathlib.Path(__file__).parent.parent / 'PySide2-stubs').glob('*.pyi'):
        module_name = fpath.stem
        collect_qflags_types_for_module(module_name, d)

    with open(JSON_OUTPUT_FNAME, 'w') as f:
        json.dump(d, f, indent=4)



if __name__ == '__main__':
    main()