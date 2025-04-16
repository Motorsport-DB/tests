import os
import shutil
import subprocess

def print_errors(errors):
    if errors:
        print("❌ clone-repo-motorsportdb")
        for err in errors:
            print("-", err)
        exit(1)
    else:
        print("✅ clone-repo-motorsportdb passed successfully!")

def run_command(command):
    """Execute a shell command and print its output."""
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        return e

def clone_repositories():
    """Clone the repositories into the specified directories."""
    errors = []
    # Define repositories
    repositories = [
        "https://github.com/Motorsport-DB/website",
        "https://github.com/Motorsport-DB/races",
        "https://github.com/Motorsport-DB/teams",
        "https://github.com/Motorsport-DB/drivers"
    ]

    # Clone the first repository (website) into ~/clone-motorsportdb
    base_clone_dir = os.path.expanduser("~/clone-motorsportdb")
    if os.path.exists(base_clone_dir):
        print(f"Removing existing directory: {base_clone_dir}")
        shutil.rmtree(base_clone_dir)
    os.makedirs(base_clone_dir)

    print(f"Cloning {repositories[0]} into {base_clone_dir}")
    ret = run_command(f"git clone {repositories[0]} {base_clone_dir}")
    if (ret != None):
        print_errors([ret])

    # Change directory to ~/clone-motorsportdb
    os.chdir(base_clone_dir)

    # Clone the remaining repositories into the current directory
    for repo in repositories[1:]:
        target_dir = os.path.basename(repo)
        print(f"Cloning {repo} into {target_dir}")
        ret = run_command(f"git clone {repo} {target_dir}")
        if (ret != None):
            errors.append(ret)
    return errors

if __name__ == "__main__":
    errors = clone_repositories()
    print_errors(errors)
