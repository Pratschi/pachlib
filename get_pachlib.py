message = """
Pachlib Installer © Pratschi 2025 (github.com/Pratschi)

Program under BSD 3-Clause LICENSE (github.com/Pratschi/pachlib/LICENSE)
Part of Pachlib Repository, see more in github.com/Pratschi/pachlib
"""


def get(hidden: bool = False, installed_ok=False, version=None):
    """
    Install or update Pachlib, by returning the library.
    To install it, there are 2 options:
        globals["pachlib"] = get-pachlib.get()
        get-pachlib.get(), and then import pachlib (Recommended to use file_dir if in diferent directory)
    Arguments:
        hidden (bool): Shows install progress. Defaults to False. Version selection activates anyways if version was not given.
        installed_ok (bool): Skip installation if pachlib is already installed. Defaults to False.
        version (string): The version of Pachlib to install. Defaults to ask the user to pick one.
    Returns:
        None: If pachlib is already installed and installed_ok is True.
        pachlib: The Pachlib library.
    Raises:
        Exception: If wrong version was given or could not access pachlib Github Repository.
    """
    print("\n" +  message + "\n")
    import urllib.request, os, json
    try:
        os.mkdir("pachlib")
    except OSError:
        if os.path.isdir("pachlib"):
            if installed_ok or not input("It seems pachlib is already installed, do you want to reinstall it (y/n)? ").lower() == "y":
                return None
        else:
            raise Exception("Could not create pachlib directory!")

    versions = {}
    # Get all files in the pachlib repository
    try:
        receivedversions = json.loads(
            urllib.request.urlopen("https://api.github.com/repos/Pratschi/pachlib/contents").read().decode("utf-8"))
    except Exception as e:
        return Exception(f"Could not access pachlib Github Repository! {e}")
    number = 0

    if version is None:
        if not hidden:
            print("\nInstalling a new version of pachlib will overwrite the current one!")
        print("\nSelect version to download:")
        number = 0
        # Check for all files in the pachlib repository, and add them to the versions dictionary
        # Excluding the LICENSE, README.md and get_pachlib.py files
        for i in receivedversions:
            if i["name"] not in ["LICENSE", "README.md", "get_pachlib.py"]:
                number += 1
                versions[str(number)] = i["name"]
                print(f"[{number}] {i['name']}")

        # Ask user to select one version by number, and check the input
        selectedversion = input("\nEnter version number > ")
        if selectedversion.isdigit():
            if int(selectedversion) > number or int(selectedversion) < 0:
                print(f"Please enter a number between 1 and {number}!")
                return get(hidden, installed_ok, version)
        else:
            raise Exception("Please enter a number!")

        # Get the files in the selected version
        toinstall = json.loads(urllib.request.urlopen(next(i for i in receivedversions if i["name"] == versions[selectedversion])["_links"]["git"]).read().decode("utf-8"))
        # Get the files from the pachlib folder from the selected version
        for i in toinstall["tree"]:
            if i["path"] == "pachlib":
                toinstall = json.loads(urllib.request.urlopen(i["url"]).read().decode("utf-8"))
                break

    else:
        # If version was given, check if it exists in the pachlib repository
        selectedversion = None
        for i in receivedversions:
            if version in ["LICENSE", "README.md", "get_pachlib.py"]:
                # If file is not a version, raise an error
                raise Exception(f"Unknown Pachlib version to install '{version}'")
            elif version == i["name"]:
                # Versions exists, break loop
                selectedversion = version
                break
        if selectedversion is None:
            # Version does not exist, raise an error
            raise Exception(f"Unknown Pachlib version to install '{version}'")
        # Get the files in the selected version
        toinstall = json.loads(urllib.request.urlopen(receivedversions[version]["_links"]["git"].read().decode("utf-8")))

    # Get the files from the selected version
    for i in toinstall["tree"]:
        if i["path"] == "pachlib":
            toinstall = json.loads(
                urllib.request.urlopen(i["url"]).read().decode("utf-8"))
            break

    # Install version files + README, version README and LICENSE
    if not hidden:
        print("\nDownloading files...\n-------------------------------------------")
    number = 3
    with open("pachlib/LICENSE", "w") as openfile:
        openfile.write(
            urllib.request.urlopen("https://raw.githubusercontent.com/Pratschi/pachlib/refs/heads/main/LICENSE").read().decode("utf-8"))
    if not hidden:
        print(f"Downloaded LICENSE (1/{len(toinstall['tree']) + 3})")
    with open("pachlib/README.md", "w") as openfile:
        openfile.write(
            urllib.request.urlopen("https://raw.githubusercontent.com/Pratschi/pachlib/refs/heads/main/README.md").read().decode("utf-8"))
    if not hidden:
        print(f"Downloaded README (2/{len(toinstall['tree']) + 3})")
    with open("pachlib/VERSION_README.md", "w") as openfile:
        openfile.write(
            urllib.request.urlopen(f"https://raw.githubusercontent.com/Pratschi/pachlib/refs/heads/main/{versions[selectedversion]}/README.md").read().decode("utf-8"))
    if not hidden:
        print(f"Downloaded version README (3/{len(toinstall['tree']) + 3})")

    for i in toinstall["tree"]:
        number += 1
        with open(f"pachlib/{i['path']}", "w") as openfile:
            openfile.write(urllib.request.urlopen(f"https://raw.githubusercontent.com/Pratschi/pachlib/refs/heads/main/{versions[selectedversion]}/pachlib/{i['path']}").read().decode("utf-8"))
        if not hidden:
            print(f"Downloaded {i['path']} ({number}/{len(toinstall['tree']) + 3})")
    if not hidden:
        print("-------------------------------------------\n")
    import pachlib
    return pachlib


if __name__ == "__main__":
    print(message)
    input("\n< Press ENTER to continue SETUP >")
    get()
