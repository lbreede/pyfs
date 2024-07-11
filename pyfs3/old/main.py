import pickle
import logging as log
from getpass import getuser
from datetime import datetime
from pprint import pprint

HOME = f"/home/{getuser()}"


def load_fs():
    try:
        with open("pyfs", "rb") as fp:
            fs = pickle.load(fp)
            if HOME not in fs:
                fs[HOME] = {"type": "dir", "created": now(), "modified": now()}
            return fs
    except FileNotFoundError:
        return init_fs()


def init_fs():
    return {
        "": {"type": "dir", "created": now(), "modified": now()},
        "/usr": {"type": "dir", "created": now(), "modified": now()},
        "/bin": {"type": "dir", "created": now(), "modified": now()},
        "/home": {"type": "dir", "created": now(), "modified": now()},
        "/lib": {"type": "dir", "created": now(), "modified": now()},
        "/tmp": {"type": "dir", "created": now(), "modified": now()},
        "/etc": {"type": "dir", "created": now(), "modified": now()},
        HOME: {"type": "dir", "created": now(), "modified": now()},
    }


def now() -> str:
    return datetime.now().isoformat()


def dump_fs(fs):
    with open("pyfs", "wb") as fp:
        pickle.dump(fs, fp)


def dump_json(fs):
    import json

    with open("pyfs.json", "w") as fp:
        json.dump(fs, fp, indent=4)


def _ls(src: str, fs: dict) -> set:
    return {
        x
        for x in fs.keys()
        if x.count("/") == src.count("/") + 1 and x.startswith(src)
    }


def handle_ls(src: str, fs: dict) -> None:
    directories = _ls(src, fs)
    if len(directories):
        print("\n".join(sorted([x.split("/")[-1] for x in directories])))


def handle_touch(names: str, src: str, fs: set) -> set:
    for name in names:
        path = src + "/" + name
        if path not in _ls(src, fs):
            fs[path] = {"type": "file", "created": now(), "modified": now()}
            log.debug(f"touch: created file '{name}' at '{src}'")
        else:
            log.debug(f"touch: cannot create file '{name}': File exists")
    return fs


def handle_mkdir(names: str, src: str, fs: set) -> set:
    for name in names:
        path = src + "/" + name
        if path not in _ls(src, fs):
            fs[path] = {"type": "dir", "created": now(), "modified": now()}
            log.debug(f"mkdir: created directory '{name}' at '{src}'")
        else:
            log.info(f"mkdir: cannot create directory '{name}': File exists")
    return fs


def prompt(src):
    if src == "":
        return "/ $ "
    if src == HOME:
        return "~ $ "
    return src + " $ "


def handle_cd(src, dst, fs):
    if dst == "/":
        dst = ""

    elif dst == "~":
        dst = HOME

    elif dst.startswith("/") and dst in fs:
        dst = dst

    elif dst.startswith(".."):
        print(dst.count(".."))
        print("src", "dst")
        pass

    elif dst.startswith("./"):
        dst = src + "/" + dst[2:]
    else:
        dst = src + "/" + dst

    if dst in fs and fs[dst]["type"] == "dir":
        return dst
    else:
        print(f"cd: '{dst}': No such file or directory")
        return src


def handle_echo(args, fs, src):
    if ">" in args:
        return fs

    if ">>" in args:
        idx = args.index(">>")
        text, dst = (
            " ".join(args[:idx] + args[idx + 2 :]),
            src + "/" + args[idx + 1],
        )

        # TODO: Fix all this

        if dst not in fs:
            fs = handle_touch(dst, fs)
        # if dst in fs:
        #     print(dst, text)

        return fs

    log.info(" ".join(args))
    return fs


def main():
    level = log.DEBUG
    format = "%(asctime)s - [%(levelname)s] - %(message)s"
    log.basicConfig(level=level, format=format)

    log.debug("Starting file system...")

    fs = load_fs()
    if fs is None:
        fs = init_fs()

    src = HOME
    while True:
        user_input = input(prompt(src))
        parts = user_input.split()
        cmd = parts[0]
        args = parts[1:]

        if cmd in ("exit", "e", "x"):
            break
        elif cmd in ("debug", "d"):
            pprint(fs)
        elif cmd in ("ls", "ll"):
            handle_ls(src, fs)
        elif cmd == "mkdir":
            fs = handle_mkdir(args, src, fs)
        elif cmd == "cd":
            src = handle_cd(src, args[0], fs)
        elif cmd == "touch":
            fs = handle_touch(args, src, fs)
        elif cmd == "echo":
            fs = handle_echo(args, fs, src)
        else:
            log.debug(f"{cmd}: command not found")

    dump_fs(fs)
    dump_json(fs)

    log.debug("Exiting file system. Good night sweet prince.")


if __name__ == "__main__":
    main()
