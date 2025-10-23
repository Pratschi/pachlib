# Pachlib
A Python library full of useful tools, such as SSH, loading bars, and dynamic library importing (with pip).

# How to add it to your project?
**Download and run get_pachlib.py / Download and import get-pachlib.py and execute get_pachlib.get() (See docstring for available args)**

Instead of donwloading get_pachlib.py, you can also copy this code that installs both the installer and pachlib:
<br>`import urllib.request`
<br>`with open("get_pachlib.py", "w") as openfile:`
<br>`    with urllib.request.urlopen('https://raw.githubusercontent.com/Pratschi/pachlib/refs/heads/main/get_pachlib.py') as data:`
<br>`        openfile.write(str(data.read().decode("utf-8")))`
<br>`import get_pachlib`
<br>` lobals()["pachlib"] = get_pachlib.get()`

<br>**In the future, it will be available to download with `pip install pachlib`**
