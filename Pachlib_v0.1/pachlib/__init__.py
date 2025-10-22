from . import libraries

def animation(text: dict):
  import sys, time
  """
  Must be a dictionary with the following structure:
    Items that represent a part of the text must be a dictionary with the following structure:
      type: The type of animation (normal, rotate)
      text: The text to display (for normal) or a dictionary of texts to rotate (for rotate, strucutre in example below)
      speed: The speed of the rotation (for rotate)
      status: The current status of the rotation (for rotate) (if negative, skipped)

  Example:
  {"loading": {"type": "normal", "text": "Loading: "}, "percent": {"type": "rotate", "text": {1: "25%", 2: "50%", 3: "75%", 4: "100%"}, "speed": 0.5, "status": 0}}
  """
  for item in text.values():
    timer = time.time()
    try:
      item["time"]
    except Exception:
      item["time"] = 0

    if item["type"] == "normal":
      sys.stdout.write(str(item["text"]))
      sys.stdout.flush()
    elif item["type"] == "rotate":
      if item["time"] - timer >= item["speed"] and not item["status"] < 0:
        item["status"] += 1
        if item["status"] >= len(item["text"]):
          item["status"] = -1
        else:
          sys.stdout.write(str(item["text"][item["status"]]))
          sys.stdout.flush()

def giveerror(type, cmd, args=None, handler=False):
  """
  Give a full error message. Used for python programs that use commands with arguments.
  
  type: The type of error, wich can be: args (missing arguments), arg (unknown argument)
  cmd: The command that caused the error
  args: A dictionary with the arguments and their description (for args error type)
  """
  if type == "args" or type == "arg":
    if args is None:
      raise ValueError("ERROR: 'args' variable missing for giveerror function")
    print(f"""\nERROR: {'Missing argument' if type == "args" else 'Unknown argument'} for command '{cmd}'""")
    print("Available arguments:")
    for arg in args:
      print(f"   - {arg} > {args[arg]}")

def loadbar(action: str, name: str, value=0.0):
  global _loadbars
  try:
    _loadbars
  except Exception:
    _loadbars = {}
  try:
    value = float(value)
  except ValueError:
    raise ValueError(f"LoadBars: Value must be a number ({value})")

  if action == "create":
    if name in _loadbars:
      print(f"LoadBars: Bar already exists ({name})")
    _loadbars[name] = value
    printbar(name, value)

  elif action == "set":
    if name not in _loadbars:
      print(f"LoadBars: Bar does not exist ({name})")
      return
    _loadbars[name] = value
    printbar(name, value)

  elif action == "add":
    if name not in _loadbars:
      print(f"LoadBars: Bar doesn't exist ({name})")
      return
    value = _loadbars[name] + value
    if value > 100:
      value = 100
      del _loadbars[name]
    else:
      _loadbars[name] = value
    printbar(name, value)
  else:
    raise ValueError(
        f"LoadBars: Unknown action for bar {name}: {action} > {value}")

def printbar(nombre, value):
  import sys
  bar_size = 20
  bar_fill = int(bar_size * value // 100)
  bar_empty = bar_size - bar_fill
  bar = "[" + "=" * bar_fill + " " * bar_empty + "]"
  sys.stdout.write(f"\r{nombre}: {bar} {value}%")
  sys.stdout.flush()
  if value == 100:
    print()

def ssh(args):
  """
  Establish a SSH Connection to a host.
  args: user@host:port -p port -pp password -t timeout
  NOTE: Put port once (either -p or user@host:port)
  NOTE: Has a default timeout of 10 seconds.

  Also includes directory handler (cd command).
  Use sshconn_quit to exit the SSH connection.
  """
  try:
    libraries.install("paramiko")
  except ImportError:
    raise ImportError("ERROR: paramiko module not found")
  args = args.split(" ")
  HOST = args[0].split("@")[1].split(":")[0]
  if "-p" in args and len(args[0].split("@")[1].split(":")) > 1:
    raise ValueError("ERROR: Port specified twice: -p and user@host:port")
  else:
    PORT = 22 if len(args[0].split("@")[1].split(":")) == 1 else int(args[0].split("@")[1].split(":")[1] if "-p" not in args else int(args[args.index("-p") + 1]))
  USER = args[0].split("@")[0]
  PASSWORD = input(f"Password for {USER}@{HOST}:{PORT}: ") if "-pp" not in args else args[args.index("-pp") + 1]
  TIMEOUT = 10 if "-t" not in args else int(args[args.index("-t") + 1])

  ssh = paramiko.SSHClient()
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  try:
    ssh.connect(HOST, username=USER, password=PASSWORD, port=PORT, timeout=TIMEOUT)
    stdin, stdout, stderr = ssh.exec_command('pwd')
    current_dir = stdout.read().decode().strip()
    while True:
      try:
        command = input(f"\n{ssh.get_transport().sock.getpeername()[0]}@{ssh.get_transport().sock.getpeername()[1]} {current_dir}$ ")
        if command == "sshconn_quit":
          break
        elif command.startswith("cd "):
          new_dir = command[1:].strip()
          stdin, stdout, stderr = ssh.exec_command(
              f'cd {current_dir} && cd {new_dir} && pwd')
          new_path = stdout.read().decode().strip()
          err = stderr.read().decode().strip()
          if err:
            print(f"ERROR: Could not access directory: {err}")
          else:
            current_dir = new_path
        stdin, stdout, stderr = ssh.exec_command(command)
        print(stdout.read().decode())
      except KeyboardInterrupt:
        print("\nSSH > Ctrl+C Detected > Use 'sshconn_quit' command to leave the SSH session.\n")
  except paramiko.AuthenticationException:
    raise paramiko.AuthenticationException(
        "Authentication failed, please verify your credentials")
  except paramiko.SSHException as sshException:
    raise paramiko.SSHException(
        f"Unable to establish SSH connection: {sshException}")
  except Exception as e:
    print(f"Unable to start SSH connection: {e}")

def system():
  import platform
  system = {}
  system["processor"] = platform.processor()
  system["machine"] = platform.machine()
  system["system"] = platform.system()
  system["system_alias"] = platform.system_alias(system=platform.system(), release=platform.release(), version=platform.version())
  system["node"] = platform.node()
  system["release"] = platform.release()
  system["python_version"] = platform.python_version()
  system["python_compiler"] = platform.python_compiler()
  system["python_branch"] = platform.python_branch()
  system["python_revision"] = platform.python_revision()
  system["python_build"] = platform.python_build()
  system["python_implementation"] = platform.python_implementation()
  system["python_version_tuple"] = platform.python_version_tuple()
  system["python_compiler"] = platform.python_compiler()
  system["python_build"] = platform.python_build()
  system["architecture"] = platform.architecture()
  system["uname"] = platform.uname()
  if platform.system() == "Linux":
    system["base_os"] = "Linux"
    try:
      libraries.install("distro")
      try:
        linuxdata = platform.freedesktop_os_release()
        system["os"] = linuxdata["NAME"]
        system["version"] = linuxdata["VERSION"]
        system["codename"] = linuxdata["VERSION_CODENAME"]
        system["id"] = linuxdata["ID"]
      except Exception:
        try:
          with open("/etc/os-release") as f:
            for line in f:
              if line.startswith("PRETTY_NAME="):
                system["version"] = line.strip().split("=")[1].strip('"')
        except Exception:
          system["version"] = distro.version()
        system["os"] = distro.id()
        system["codename"] = distro.codename()
    except ImportError:
      print("ERROR: Unable to detect Linux distribution")
  elif platform.system() == "Windows":
    system["base_os"] = "Windows"
    system["os"] = "Windows"
    system["version"] = platform.version()
    try:
      system["win_edition"] = platform.win32_edition()
    except AttributeError:
      system["win_edition"] = "Unknown"
    system["win32_ver"] = platform.win32_ver()
  elif platform.system() == "Darwin":
    system["base_os"] = "MacOS"
    system["os"] = "MacOS"
    system["version"] = platform.mac_ver()[0]
  else:
    system = platform.system()
    system["version"] = platform.version()
    system["base_os"] = "Unknown"

return system
