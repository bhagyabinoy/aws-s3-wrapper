import os
import re
import subprocess


def detect_platform():
    """Detect the current operating system using subprocess."""
    try:
        result = subprocess.run(
            ["uname"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        if result.returncode == 0 and "Darwin" in result.stdout:
            return "darwin"
        elif result.returncode == 0 and "Linux" in result.stdout:
            return "linux"
    except FileNotFoundError:
        pass
    return "win32"  # Assume Windows if `uname` is not found


def parse_chrome_version_from_registry(output):
    """Parses the Chrome version from the Windows registry query output."""
    try:
        version_key = "DisplayVersion    REG_SZ"
        if version_key in output:
            start_idx = output.rindex(version_key) + len(version_key)
            version = output[start_idx:].split("\n", 1)[0].strip()
            return version
    except (TypeError, ValueError):
        pass
    return None


def find_chrome_version_in_folder():
    """Finds the Chrome version by scanning installation folders on Windows."""
    program_paths = [
        r"C:\Program Files\Google\Chrome\Application",
        r"C:\Program Files (x86)\Google\Chrome\Application",
    ]
    version_pattern = r"\d+\.\d+\.\d+\.\d+"

    for path in program_paths:
        if os.path.isdir(path):
            for entry in os.scandir(path):
                if entry.is_dir() and re.match(version_pattern, entry.name):
                    return entry.name
    return None


def get_chrome_installation_path(platform):
    """Returns the default installation path for Chrome based on the platform."""
    if platform == "linux":
        return "/usr/bin/google-chrome"
    elif platform == "darwin":
        return r"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    elif platform == "win32":
        return None  # Windows uses registry or folder lookup
    return None


def fetch_version_from_executable(path):
    """Fetches the Chrome version by executing the binary with the --version flag."""
    try:
        version_output = subprocess.run(
            [path, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        if version_output.returncode == 0 and "Google Chrome" in version_output.stdout:
            return version_output.stdout.split("Google Chrome")[-1].strip()
    except Exception as ex:
        print(f"Failed to fetch version from {path}: {ex}")
    return None


def retrieve_chrome_version():
    """Main function to determine the installed Chrome version."""
    current_platform = detect_platform()

    if current_platform == "win32":
        # On Windows, try retrieving the version from the registry
        try:
            reg_query = (
                'reg query "HKLM\\SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Google Chrome"'
            )
            registry_output = subprocess.run(
                reg_query, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            if registry_output.returncode == 0:
                version = parse_chrome_version_from_registry(registry_output.stdout)
                if version:
                    return version
        except Exception:
            pass

        # If registry lookup fails, check the installation folder
        return find_chrome_version_in_folder()

    # For Linux and macOS, use the executable path
    install_path = get_chrome_installation_path(current_platform)
    if install_path:
        return fetch_version_from_executable(install_path)

    return None


if __name__ == "__main__":
    chrome_version = retrieve_chrome_version()
    if chrome_version:
        print(f"Chrome Version: {chrome_version}")
    else:
        print("Chrome is not installed or the version could not be determined.")
