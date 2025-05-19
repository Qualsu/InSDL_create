import argparse
from create.create import create_project
from create.delete import delete_project
from create.compile import compile_project

def main():
    parser = argparse.ArgumentParser(description="InSDL project manager")
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    create_parser = subparsers.add_parser('create', help='Create new project')
    create_parser.add_argument('project_name', help='Project name')
    create_parser.add_argument('-vsc', action='store_true', help='Add folder .vscode')
    create_parser.add_argument('-bat', action='store_true', help='Add compile.bat')
    
    del_parser = subparsers.add_parser('del', help='Delete project')
    del_parser.add_argument('project_name', help='Project name')
    
    compile_parser = subparsers.add_parser('compile', help='Compiled project')
    compile_parser.add_argument('project_name', help='Project name')
    
    args = parser.parse_args()
    
    if args.command == 'create':
        create_project(args.project_name, vsc_keep=args.vsc)
    elif args.command == 'del':
        delete_project(args.project_name)
    elif args.command == 'compile':
        compile_project(args.project_name)