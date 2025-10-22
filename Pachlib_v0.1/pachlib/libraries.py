def install(module, pipname=None):
    """
    Install a module if it is not already installed. Compatible with pip.
    If a module is not found, it will be installed using pip.
    If module's name is not the same as the pip name, use pipname to specify pip's name.
    If pip is not installed, it will be installed using get-pip.py.
    """
    import importlib, subprocess
    try:
        importlib.import_module(module)
    except ImportError:
        subprocess.run(['pip', 'install', module if pipname is None else pipname], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        print(f"ERROR: Could not load module '{module}'")
        return
    mod = importlib.import_module(module)
    globals()[module] = mod

def updatepip():
    """
    Install or update pip to the latest version.
    If pip is not installed, pip 25.2 will be installed (Included locally) and then updated online.
    """
    import os, subprocess, sys
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "--version"], capture_output=True, text=True)
        pip_installed = result.returncode == 0

        if pip_installed:
            upgrade_check = subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip", "--dry-run"], capture_output=True, text=True)
            if "Would install" not in upgrade_check.stdout:
                return
            else:
                install_pip = True
        else:
            install_pip = True

        if install_pip:
            pip_path = os.path.join(os.path.dirname(__file__), "get-pip.py")
            try:
                install("requests")
                response = requests.get("https://bootstrap.pypa.io/get-pip.py")
                if response is None or response.status_code != 200:
                    raise Exception()
                with open(pip_path, "w", encoding="utf-8") as f:
                    f.write(response.text)
            except Exception or requests.exceptions.RequestException:
                with open(pip_path, "w", encoding="utf-8") as f:
                    f.write(os.path.join(os.path.dirname(__file__), "get-pip.py"))

            subprocess.run([sys.executable, pip_path], check=True)
            if os.path.exists(pip_path):
                os.remove(pip_path)

    except Exception as e:
        raise ValueError(f"ERROR: Could not update or install pip: {e}")

def pipstatus():
    """
    Check if pip is installed or requires an update.
    Returns True if is installed, None if can be updated and False if it's not installed.
    """
    import subprocess, sys
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            return True
        elif "Would install" not in upgrade_check.stdout:
            return None
        else:
            return False
