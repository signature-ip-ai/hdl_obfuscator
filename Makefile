GRAMMAR_DIR := $(shell realpath grammar)
TARGET_DIR := $(shell realpath src/hdl_obfuscator/mangler/systemverilog)

build:
	@pip3 install --upgrade build
	@python3 -m build


install: build
	@pip3 install dist/*.whl


generate:
	@pip3 install -r requirements.txt
	@echo "Generating ANTLR4 files..."
	@for file in $(GRAMMAR_DIR)/*.g4; do \
		echo "Generating ANTLR4.13.1 grammar files for: $$file at $(TARGET_DIR)"; \
		antlr4 -Dlanguage=Python3 $$file -o $(TARGET_DIR); \
	done
	@echo "Generation complete."


clean:
	@pip3 uninstall hdl_obfuscator -y
	@rm -rf src/hdl_obfuscator.egg-info dist
