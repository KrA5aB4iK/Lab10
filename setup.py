# setup.py

import sys
import subprocess

def install_packages():
    packages = ['numpy', 'scipy', 'matplotlib']
    print("🚀 Установка библиотек:", ", ".join(packages))
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--no-cache-dir'] + packages)
    print("✅ Установка завершена!")

if __name__ == '__main__':
    install_packages()