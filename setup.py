from setuptools import setup
setup(
    name="systemverilog-obfuscator",
    version="1.0",
    author="Signature IP",
    description="Tool for Obfuscating HDL files",
    package_dir={"":"src"},
    url="http://gitlab.marqueesemi.com:8081/signature-ip-sw-tools/HDLObf",
    install_requires=[
        "antlr4-python3-runtime==4.13.1",
        "antlr4-tools==0.2.1"
    ],
    options={
        'egg_info': {
            'egg_base': 'build'
        }
    }
)
