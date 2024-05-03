package com.signature.hdlobf;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.util.HashMap;

import com.signature.hdlobf.generated.IDMapLexer;
import com.signature.hdlobf.generated.IDMapLoader;
import com.signature.hdlobf.generated.VhdlNoSkipLexer;

import antlr.Token;

public class VhdlObfuscator {
    public static VhdlObfuscator create(final String mapFile, final String inFile, final String outFile)
            throws ObfuscatorException {
        try {
            final var maplexer = new IDMapLexer(new DataInputStream(new FileInputStream(mapFile)));
            final var mapLoader = new IDMapLoader(maplexer);
            mapLoader.source_text();
            IDMapLoader.DebugTrue = true;
            final var obfHMap = IDMapLoader.idHMap;

            final var mapFileOutputStream = new DataOutputStream(new FileOutputStream(mapFile, true));

            final var lexer = new VhdlNoSkipLexer(
                    new DataInputStream(new FileInputStream(inFile)));

            final var outputfile = new File(outFile);
            if (outputfile.exists()) {
                outputfile.delete();
            }
            outputfile.createNewFile();
            final var outFileStream = new FileOutputStream(outFile);

            return new VhdlObfuscator(obfHMap, mapFileOutputStream, lexer, outFileStream);

        } catch (Exception exception) {
            throw new ObfuscatorException(
                    "Unable to initialize VhdlObfuscator: " + exception.getMessage());
        }
    }

    private VhdlObfuscator(final HashMap<String, String> mapFile, final DataOutputStream mapfileOutputStream,
            final VhdlNoSkipLexer lexer,
            final FileOutputStream outFileStream) {
        this.mapFile = mapFile;
        this.mapfileOutputStream = mapfileOutputStream;
        this.lexer = lexer;
        this.outFileStream = outFileStream;
    }

    public void generateObfuscatedFile() throws ObfuscatorException {
        try {
            Token token = lexer.nextToken();
            do {
                var outputString = token.getText();
                if (VhdlNoSkipLexer.SIMPLE_IDENTIFIER == token.getType()) {
                    if (this.mapFile.containsKey(outputString)) {
                        final var newOutputString = this.mapFile.get(outputString);
                        System.out.print("Value of ID: " + outputString + "\t\trenamed to: " + newOutputString);
                        outputString = newOutputString;

                    } else {
                        final var hashString = "ID_S_" + HashFunctions.hash1(outputString) + "_"
                                + HashFunctions.hash2(outputString) + "_E";
                        this.mapFile.put(outputString, hashString);
                        this.mapfileOutputStream.writeBytes(outputString + "=" + hashString + "\n");
                        System.out.print("Value of ID: " + outputString + "\t\trenamed to : " + hashString
                                + " added in hash map");
                        outputString = hashString;
                    }
                }

                else if (VhdlNoSkipLexer.COMMENT == token.getType()) {
                    outputString = " ";
                }

                this.outFileStream.write(outputString.getBytes());
                token = lexer.nextToken();

            } while (Token.EOF_TYPE != token.getType());

            this.mapfileOutputStream.close();
            this.outFileStream.close();

        } catch (Exception exception) {
            throw new ObfuscatorException(
                    "Unable to execute VhdlObfuscator: " + exception.getMessage());
        }
    }

    private final HashMap<String, String> mapFile;
    private final DataOutputStream mapfileOutputStream;
    private final VhdlNoSkipLexer lexer;
    private final FileOutputStream outFileStream;
}
