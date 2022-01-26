from re import findall
from typing import Dict, List, Tuple
from string import punctuation

TAB = "\x20\x20\x20\x20"

names_used = []


def clear_key(key: str) -> str:
    for p in punctuation:
        key = key.replace(p, ' ')
    string = ''.join(k[0].upper() + k[1:] for k in key.split(' '))
    return string[0].lower() + string[1:]


def get_normal_name(name: str, name_base_class: str) -> str:
    name_new_class: str = name.capitalize()
    while True:
        if name_new_class in names_used:
            name_new_class = name_base_class + name_new_class
        else:
            break
    names_used.append(name_new_class)
    return name_new_class


def parse_json_to_model(json_object: Dict, name_base_class: str) -> str:
    classes: str = ''
    string: str = f'class {name_base_class}(BaseModel):\n'
    for key, value in json_object.items():
        field: str = clear_key(key)
        if field == key:
            field = ''
        else:
            _s: str = field
            field = f' = Field(None, alias="{key}")'
            key = _s
        if isinstance(value, Dict):
            name_new_class: str = get_normal_name(key, name_base_class)
            string += f'{TAB}{key}: Optional[{name_new_class}]{field}\n'
            classes += parse_json_to_model(value, name_new_class)
        elif isinstance(value, List) or isinstance(value, Tuple):
            name_new_class: str = get_normal_name(key, name_base_class)
            if all(isinstance(vl, Dict) for vl in value) and len(
                    {str(val.keys()) for val in value if isinstance(val, Dict)}) == 1:
                string += f'{TAB}{key}: Optional[Tuple[{name_new_class}, ...]]{field}\n'
                classes += parse_json_to_model(value[0], name_new_class)
            else:
                string += f'{TAB}{key}: Optional[Tuple[{", ".join(type(v).__name__ for v in value)}]]{field}\n'
        else:
            string += f'{TAB}{key}: Optional[{type(value).__name__}]{field}\n'
    string += '\n\n'
    return classes + string


def parse(json_dict: Dict, name_base_class: str, add_import_string: bool = True, clear_list_named_used: bool = True,
          class_list: str = '') -> str:
    global names_used
    names_used += [name.split(' ')[1].split('(')[0].replace(':', '') for name in findall(r'class .*', class_list)]
    name_base_class = get_normal_name(name_base_class, name_base_class)
    string = ''
    if add_import_string is True:
        string += 'from pydantic import BaseModel, Field\nfrom typing import Optional, Tuple, List, Dict\n\n\n'
    string += parse_json_to_model(json_dict, name_base_class)
    if clear_list_named_used is True:
        names_used.clear()
    return string.replace('list', 'List').replace('tuple', 'Tuple').replace('dict', 'Dict')
