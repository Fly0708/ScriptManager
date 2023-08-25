import yaml


class Script:
    def __init__(self, alias, name, bat_path, description):
        self.alias = alias
        self.name = name
        self.bat_path = bat_path
        self.description = description

    def __str__(self):
        return f'{self.alias} {self.name} {self.bat_path} {self.description}'


def load_script_alias_dict_from_yml(config_path: str) -> dict:
    with open(config_path, 'r') as f:
        scripts_config: dict = yaml.load(f, Loader=yaml.FullLoader)
    if len(scripts_config) == 0:
        raise Exception('scripts.yml is empty')
    script_list = []
    for alias, item in scripts_config.items():
        script_list.append(Script(alias=alias, name=item.get('name'), bat_path=item.get('batPath'),
                                  description=item.get('description')))
    return {obj.alias: obj for obj in script_list}
