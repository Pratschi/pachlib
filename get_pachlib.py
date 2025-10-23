message = """
Pachlib Installer © Pratschi 2025 (github.com/Pratschi)

Program under BSD-3-Clause LICENSE (github.com/Pratschi/pachlib/LICENSE)
Part of Pachlib Repository, see more in github.com/Pratschi/pachlib
"""

def get(showprogress:bool=True, installed_ok=False, file_dir=None, version=None):
    """
    Install or update Pachlib, by returning the library.
    To install it, there are 2 options:
        globals["pachlib"] = get-pachlib.get()
        get-pachlib.get(), and then import pachlib (Recommended to use file_dir if in diferent directory)
    Arguments:
        showprogress (bool): Shows wich files are being downloaded. Defaults to True.
        installed_ok (bool): Skip installation if pachlib is already installed. Defaults to False.
        file_dir (string): The path to install pachlib to. Defaults to the same path as the get-pachlib library file (This file).
        version (string): The version of Pachlib to install. Defaults to ask the user to pick one.
    Returns:
        None: If pachlib is already installed and installed_ok is True.
        Exception: If wrong version was given.
        pachlib: The Pachlib library.
    """
    import urllib.requests, os, json
    try:
        os.mkdir("pachlib")
    except OSError:
        if os.path.isdir("pachlib"):
            if installed_ok or not input("It seems pachlib is already installed, do you want to reinstall it (y/n)?").lower() == "y":
                return None
        else:
            raise Exception("Could not create pachlib directory!")

    versions = {}
    finalversions = {}
    receivedversions = urllib.request.urlopen("https://api.github.com/repos/Pratschi/pachlib/contents").read().decode("utf-8").json()
    number = 0

    if version is not None:
        print("Installing a new version of pachlib will overwrite the current one!")
        print("Select version to download:")
        number = 0
        for i in receivedversions:
            if i["name"] not in ["LICENSE", "README.md", "get-pachlib.py"]:
                number += 1
                versions[str(number)] = i["name"]
                print(f"[{number}] {i['name']}")
                
        for i in versions:
            finalversions[str(number)] = versions[i]
            print(f"[{number}] {finalversions[str(number)]}")
            
        selectedversion = input("\nEnter version number > ")
        if selectedversion.isdigit():
            if int(selectedversion) > number or int(selectedversion) < 0:
                raise Exception("Please select a correct version!")
        else:
            raise Exception("Please enter a number!")
        toinstall = urllib.request.urlopen(receivedversions[finalversions[selectedversion][selectedversion]]["_links"]["git"]).read().decode("utf-8").json()
        
    else:
        for i in receivedversions:
            if version in ["LICENSE", "README.md"]:
                raise Exception(f"Unknown Pachlib version to install '{version}'")
            elif version == i["name"]:
                selectedversion = version
                break
        if not selectedversion:
            raise Exception(f"Unknown Pachlib version to install '{version}'")
        toinstall = urllib.request.urlopen(receivedversions[version]["_links"]["git"].read().decode("utf-8").json())

    for i in toinstall:
        if i["name"] == "pachlib":
            toinstall = urllib.request.urlopen(i["url"]).read().decode("utf-8").json()
            break

    print("\nDownloading files...")
    number = 0
    with open("pachlib/LICENSE", "w") as openfile:
        openfile.write(urllib.request.urlopen("https://raw.githubusercontent.com/Pratschi/pachlib/refs/heads/main/LICENSE").read().decode("utf-8"))
    print(f"Downloaded LICENSE (1/{len(toinstall) + 3})")
    with open("pachlib/README.md", "w") as openfile:
        openfile.write(urllib.request.urlopen(f"https://raw.githubusercontent.com/Pratschi/pachlib/refs/heads/main/README.md").read().decode("utf-8"))
    print(f"Downloaded README (2/{len(toinstall) + 3})")
    with open("pachlib/VERSION_README.md", "w") as openfile:
        openfile.write(urllib.request.urlopen(f"https://raw.githubusercontent.com/Pratschi/pachlib/refs/heads/main/{versions[selectedversion]}/pachlib/README.md").read().decode("utf-8"))
    print(f"Downloaded version README (3/{len(toinstall) + 3})")
    for i in toinstall:
        number += 1
        with open(f"pachlib/{i['name']}", "w") as openfile:
            openfile.write(urllib.request.urlopen(f"https://raw.githubusercontent.com/Pratschi/pachlib/refs/heads/main/{versions[selectedversion]}/pachlib/{i['name']}").read().decode("utf-8"))
        print(f"Downloaded {i['name']} ({number + 3}/{len(toinstall) + 3})")
    import pachlib
    return pachlib

if __name__ == "__main__":
    print("message")
    input("\n< Press ENTER to continue SETUP >")
    get()
