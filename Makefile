GRAMMAR_DIR := $(shell realpath grammar)
TARGET_DIR := $(shell realpath src/systemverilog)

all: generate
	@pip3 install pyinstaller --user
	@pyinstaller obfuscator.spec

clean:
	@rm -rf build/obfuscator build/systemverilog_obfuscator.egg-info dist

generate:
	@pip3 install -r requirements.txt --user
	@echo "Generating ANTLR4 files..."
	@for file in $(GRAMMAR_DIR)/*.g4; do \
		echo "Generating ANTLR4.13.1 grammar files for: $$file at $(TARGET_DIR)"; \
		antlr4 -Dlanguage=Python3 $$file -o $(TARGET_DIR); \
	done
	@echo "Generation complete."

package: clean
	@pip3 install sdist
	@pip3 install wheel
	@python setup.py sdist bdist_wheel
