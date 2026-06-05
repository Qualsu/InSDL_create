import argparse

from create.create import create_project

def main():
    parser = argparse.ArgumentParser(description="Create an InSDL project")
    parser.add_argument("project_name", nargs="?", help="Project name")
    args = parser.parse_args()

    project_name = args.project_name or input("Project name: ").strip()
    if not project_name:
        print("Project name is required.")
        return

    create_project(project_name)


if __name__ == "__main__":
    main()
