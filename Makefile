all:
	@pip3 install pyinstaller --user
	@pip3 install -r requirements.txt --user
	@pyinstaller obfuscator.spec

clean:
	@rm -rf build/obfuscator dist
