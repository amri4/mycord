from setuptools import setup
from setuptools.command.install import install
import sys

class CustomInstallCommand(install):
    def run(self):
        # Run the standard installation process first
        super().run()
        
        # Print your custom success message directly to the terminal!
        sys.stdout.write("\n\033[92m✅ mycord installed\033[0m\n\n")
        sys.stdout.flush()

setup(
    cmdclass={
        'install': CustomInstallCommand,
    },
)

