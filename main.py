import os
import argparse
import subprocess
import script_config

arg_parser = argparse.ArgumentParser(description="script manager")

arg_parser.add_argument('-c', '--config', type=str, help='config file path')
arg_parser.add_argument('-r', '--run', nargs='+', type=str, help='script number to run and args')
arg_parser.add_argument('--register', nargs=2, type=str, help='register script')
arg_parser.add_argument('-l', '--list', action='store_true', help='list all scripts')

args = vars(arg_parser.parse_args())

config_file_path = args.get('config')
if config_file_path is None:
    raise Exception('config file path not configured')

# load scripts from scripts.yml
script_alias_dict = script_config.load_script_alias_dict_from_yml(config_file_path)

if args.get('register') is not None:
    script_path = args.get('register')[0]
    script_description = args.get('register')[1]

    with open('scripts.properties', 'a') as f:
        f.write(f'{script_path}={script_description}\n')
    exit(0)

list_flag = args.get('list')
if list_flag is not None and list_flag:
    for alias, script in script_alias_dict.items():
        print(alias)
        print(f'\t{script.name}\t{script.description}')
    exit(0)

run = args.get('run')
if run is not None:
    target_script_alias = run[0]
    target_script: script_config.Script = script_alias_dict.get(target_script_alias)

    if target_script is None:
        raise Exception(f'no such script: {target_script_alias}')
    command = [target_script.bat_path] + run[1:]
    print(f'run command: {command}')
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print('错误信息:')
        print(result.stderr)
    exit(0)