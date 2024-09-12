#!/bin/env python3

class ObfuscatorException(Exception):
    def __init__(self, message: str = ""):
        self.message = message

    def __str__(self):
        return f"Obfuscator Exception: {self.message}"
