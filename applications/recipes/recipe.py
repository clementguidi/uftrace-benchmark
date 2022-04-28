import os
import subprocess
import mimetypes


def identify_file_type(url):
    return mimetypes.guess_type(url)

def extract_archive(path):
    file_type, _ = identify_file_type(path)
    outdir = os.path.dirname(path)
    # print(f"EXTRACT {path} in {outdir}")
    if file_type == "application/zip":
        subprocess.run(["unzip", path, "-d", outdir])
    elif file_type == "application/x-tar":
        subprocess.run(["tar", "xf", path, "--directory", outdir])

def strip_ext(url):
    file_type, encoding = identify_file_type(url)
    if file_type == "application/zip":
        return url.removesuffix(".zip")
    elif file_type == "application/x-tar":
        if encoding == "gzip":
            url = url.removesuffix(".gz")
        elif encoding == "xz":
            url = url.removesuffix(".xz")
        url = url.removesuffix(".tar")
        return url
    elif file_type == None:
        print("File type not recognized")
        return url
    else:
        print("Unsupported file type")
        return url


class BaseRecipe:
    path_prefix_trim = ""
    path_prefix_add  = ""
    path_suffix_trim = ""
    path_suffix_add  = ""
    requirements  = []
    build_dir    = ""
    config_dir   = ""
    preconf_prog = ""
    preconf_args = []
    config_prog  = ""
    config_args  = []
    build_prog   = ""
    build_args   = []
    cflags  = []
    ldflags = []

    def __init__(self, name, archive_path):
        self.name = name
        self.archive_path = archive_path
        self.path = strip_ext(archive_path)
        self.fix_path()

    def fix_path(self):
        basename = os.path.dirname(self.path)
        dirname = os.path.basename(self.path)
        dirname = dirname.removeprefix(self.path_prefix_trim)
        dirname = dirname.removesuffix(self.path_suffix_trim)
        dirname = self.path_prefix_add + dirname + self.path_suffix_add
        self.path = f"{basename}/{dirname}"

    def unpack(self, safe=True):
        if safe:
            if os.path.exists(self.path):
                return
        print(f"UNPACK {self.archive_path} -> {self.path}")
        if not os.path.exists(self.path):
            print(f"ERROR {self.archive_path} -/> {self.path}")
        extract_archive(self.archive_path)

    def patch(self):
        pass

    def preconfigure(self):
        root_directory = os.getcwd()
        preconf_path = f"{self.path}/{self.config_dir}"
        if not os.path.exists(preconf_path):
            os.mkdir(preconf_path)
        os.chdir(preconf_path)
        print(f"PRECONF {self.name} in {os.getcwd()}")
        subprocess.run([self.preconf_prog]
                       + self.preconf_args)
        os.chdir(root_directory)

    def configure(self):
        root_directory = os.getcwd()
        config_path = f"{self.path}/{self.build_dir}"
        if not os.path.exists(config_path):
            os.mkdir(config_path)
        os.chdir(config_path)
        print(f"CONFIG {self.name} in {os.getcwd()}")
        subprocess.run([self.config_prog]
                       + self.config_args)
        os.chdir(root_directory)

    def build(self):
        root_directory = os.getcwd()
        build_path = f"{self.path}/{self.build_dir}"
        if not os.path.exists(build_path):
            os.mkdir(build_path)
        os.chdir(build_path)
        print(f"BUILD {self.name} in {os.getcwd()}")
        subprocess.run([self.build_prog]
                       + self.build_args)
        os.chdir(root_directory)

    def clean(self):
        pass

    def clean(self):
        pass

    def install(self):
        pass

    def uninstall(self):
        pass
