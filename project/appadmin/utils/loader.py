from typing import Text, Dict

import yaml


def load_yaml_file(yaml_file: Text) -> Dict:
    with open(yaml_file, mode='rb') as fp:
        yaml_content = yaml.load(fp, Loader=yaml.FullLoader)
        return yaml_content
