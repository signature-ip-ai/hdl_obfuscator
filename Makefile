GRAMMAR_DIR := $(shell realpath grammar)
TARGET_DIR := $(shell realpath src/hdl_obfuscator/mangler/systemverilog)
VENV_DIR := .pyvenv
ACTIVATE_VENV = source $(VENV_DIR)/bin/activate


.ONESHELL:


build: generate
	@ pip3 install --upgrade build
	@ python3 -m build


install: uninstall build
	@ pip3 install dist/*.whl


uninstall:
	@ pip3 uninstall -y hdl_obfuscator


generate:
	@ pip3 install -r requirements.txt
	@ echo "Generating ANTLR4 files..."
	@ for file in $(GRAMMAR_DIR)/*.g4; do \
		echo "Generating ANTLR4.13.1 grammar files for: $$file at $(TARGET_DIR)"; \
		antlr4 -Dlanguage=Python3 $$file -o $(TARGET_DIR); \
	done
	@ echo "Generation complete."


$(VENV_DIR):
	@ echo "Creating a virtual environment ..."
	@ python3 -m venv $(VENV_DIR)


clean:
	@ rm -rf src/hdl_obfuscator.egg-info dist
