package com.signature.hdlobf;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.HashMap;

import com.signature.hdlobf.generated.IDMapLexer;
import com.signature.hdlobf.generated.IDMapLoader;
import com.signature.hdlobf.systemverilog.SystemVerilogLexer;

import org.antlr.v4.runtime.CharStreams;
import org.antlr.v4.runtime.CommonTokenStream;

public class SystemVerilogObfuscatorv4 {
    public static SystemVerilogObfuscatorv4 create(final String mapFile, final String inFile, final String outFile)
            throws ObfuscatorException {
        try {

            final var maplexer = new IDMapLexer(new DataInputStream(new FileInputStream(mapFile)));
            final var mapLoader = new IDMapLoader(maplexer);
            mapLoader.source_text();
            IDMapLoader.DebugTrue = true;
            final var obfHMap = IDMapLoader.idHMap;

            final var mapFileOutputStream = new DataOutputStream(new FileOutputStream(mapFile, true));

            final var inFileStream = new FileInputStream(inFile);

            final var outputfile = new File(outFile);
            if (outputfile.exists()) {
                outputfile.delete();
            }
            outputfile.createNewFile();
            final var outFileStream = new FileOutputStream(outFile);

            return new SystemVerilogObfuscatorv4(obfHMap, mapFileOutputStream, inFileStream, outFileStream);

        } catch (Exception exception) {
            throw new ObfuscatorException(
                    "Unable to initialize SystemVerilogObfuscatorv4: " + exception.getMessage());
        }
    }

    private SystemVerilogObfuscatorv4(final HashMap<String, String> mapFile, final DataOutputStream mapfileOutputStream,
            final FileInputStream inFileStream,
            final FileOutputStream outFileStream) {
        this.mapFile = mapFile;
        this.mapfileOutputStream = mapfileOutputStream;
        this.inFileStream = inFileStream;
        this.outFileStream = outFileStream;
    }

    public void generateObfuscatedFile() throws ObfuscatorException {
        try {
            final var lexer = getLexerFromStream(this.inFileStream);
            var token = lexer.nextToken();

            do {
                switch (token.getType()) {
                    case SystemVerilogLexer.SIMPLE_IDENTIFIER: {
                        final var outputString = processSimpleIndentifier(token.getText());
                        this.outFileStream.write(outputString.getBytes());
                        break;
                    }

                    case SystemVerilogLexer.SOURCE_TEXT: {
                        final var subLexer = getLexerFromString(token.getText());
                        final var tokenStream = new CommonTokenStream(subLexer);
                        tokenStream.fill();
                        for (final var subToken : tokenStream.getTokens()) {
                            String outputString = subToken.getText();
                            if (SystemVerilogLexer.EOF == subToken.getType()) {
                                break;
                            }

                            if (SystemVerilogLexer.SIMPLE_IDENTIFIER == subToken.getType()) {
                                outputString = processSimpleIndentifier(outputString);
                            }
                            this.outFileStream.write(outputString.getBytes());
                        }
                        break;
                    }

                    case SystemVerilogLexer.BLOCK_COMMENT:
                    case SystemVerilogLexer.LINE_COMMENT: {
                        final var outputString = "";
                        this.outFileStream.write(outputString.getBytes());
                        break;
                    }

                    case SystemVerilogLexer.PRAGMA_DIRECTIVE: {
                        final var outputString = "\n" + token.getText() + "\n";
                        this.outFileStream.write(outputString.getBytes());
                        break;
                    }

                    default: {
                        this.outFileStream.write(token.getText().getBytes());
                        break;
                    }
                }

                token = lexer.nextToken();
            } while (SystemVerilogLexer.EOF != token.getType());

            this.mapfileOutputStream.close();
            this.outFileStream.close();

        } catch (Exception exception) {
            exception.printStackTrace();
            throw new ObfuscatorException(
                    "Unable to execute SystemVerilogObfuscatorv4: " + exception.getMessage());
        }
    }

    private SystemVerilogLexer getLexerFromStream(final FileInputStream instream) throws IOException {
        final var charStream = CharStreams.fromStream(instream);
        final var lexer = new SystemVerilogLexer(charStream);
        return lexer;
    }

    private SystemVerilogLexer getLexerFromString(final String string) throws IOException {
        final var charStream = CharStreams.fromString(string);
        final var lexer = new SystemVerilogLexer(charStream);
        return lexer;
    }

    private final String processSimpleIndentifier(final String tokenText) throws IOException {
        if (this.mapFile.containsKey(tokenText)) {
            final var newOutputString = this.mapFile.get(tokenText);
            return newOutputString;

        } else {
            final var hashString = "ID_S_" + HashFunctions.hash1(tokenText) + "_"
                    + HashFunctions.hash2(tokenText) + "_E";
            this.mapFile.put(tokenText, hashString);
            this.mapfileOutputStream.writeBytes(tokenText + "=" + hashString + "\n");
            return hashString;
        }
    }

    private final HashMap<String, String> mapFile;
    private final DataOutputStream mapfileOutputStream;
    private final FileInputStream inFileStream;
    private final FileOutputStream outFileStream;
}
