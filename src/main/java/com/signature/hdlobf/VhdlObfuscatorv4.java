package com.signature.hdlobf;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.util.HashMap;
import java.util.List;

import org.antlr.v4.runtime.CharStreams;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.Token;

import com.signature.hdlobf.generated.IDMapLexer;
import com.signature.hdlobf.generated.IDMapLoader;
import com.signature.hdlobf.vhdl.vhdlLexer;

public class VhdlObfuscatorv4 {
    public static VhdlObfuscatorv4 create(final String mapFile, final String inFile, final String outFile)
            throws ObfuscatorException {
        try {
            final var maplexer = new IDMapLexer(new DataInputStream(new FileInputStream(mapFile)));
            final var mapLoader = new IDMapLoader(maplexer);
            mapLoader.source_text();
            IDMapLoader.DebugTrue = true;
            final var obfHMap = IDMapLoader.idHMap;

            final var mapFileOutputStream = new DataOutputStream(new FileOutputStream(mapFile, true));

            final var inputFileCharStream = CharStreams.fromStream(new FileInputStream(inFile));
            final var lexer = new vhdlLexer(inputFileCharStream);

            final var outputfile = new File(outFile);
            if (outputfile.exists()) {
                outputfile.delete();
            }
            outputfile.createNewFile();
            final var outFileStream = new FileOutputStream(outFile);

            return new VhdlObfuscatorv4(obfHMap, mapFileOutputStream, lexer, outFileStream);

        } catch (Exception exception) {
            throw new ObfuscatorException(
                    "Unable to initialize VhdlObfuscatorv4: " + exception.getMessage());
        }
    }

    private VhdlObfuscatorv4(final HashMap<String, String> mapFile, final DataOutputStream mapfileOutputStream,
            final vhdlLexer lexer,
            final FileOutputStream outFileStream) {
        this.mapFile = mapFile;
        this.mapfileOutputStream = mapfileOutputStream;
        this.lexer = lexer;
        this.outFileStream = outFileStream;
    }

    public void generateObfuscatedFile() throws ObfuscatorException {
        try {
            final var tokenStream = new CommonTokenStream(this.lexer);
            tokenStream.fill();
            final List<Token> tokens = tokenStream.getTokens();

            for (final var token : tokens) {
                var outputString = token.getText();
                if (vhdlLexer.BASIC_IDENTIFIER == token.getType()) {
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

                else if (vhdlLexer.COMMENT == token.getType()) {
                    outputString = " ";
                }

                else if (vhdlLexer.EOF == token.getType()) {
                    break;
                }

                this.outFileStream.write(outputString.getBytes());
            }

            this.mapfileOutputStream.close();
            this.outFileStream.close();

        } catch (Exception exception) {
            throw new ObfuscatorException(
                    "Unable to execute VhdlObfuscatorv4: " + exception.getMessage());
        }
    }

    private final HashMap<String, String> mapFile;
    private final DataOutputStream mapfileOutputStream;
    private final vhdlLexer lexer;
    private final FileOutputStream outFileStream;
}
