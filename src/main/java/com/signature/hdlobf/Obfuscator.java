//*************************************************************************
// DESCRIPTION: HDLObf: Identifier Obfuscate Module
//
// Code available from: http://sourceforge.net/projects/hdlobf/
//
// AUTHORS: Vispi Cassod
//
//*************************************************************************
//
// This program is free software; you can redistribute it and/or modify
// it under the terms of either the GNU General Public License or the
// Perl Artistic License.
//
// Verilator is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with Verilator; see the file COPYING.  If not, write to
// the Free Software Foundation, Inc., 59 Temple Place - Suite 330,
// Boston, MA 02111-1307, USA.
//
//*************************************************************************
package com.signature.hdlobf;

import net.sourceforge.argparse4j.ArgumentParsers;
import net.sourceforge.argparse4j.inf.ArgumentParser;
import net.sourceforge.argparse4j.inf.ArgumentParserException;
import net.sourceforge.argparse4j.inf.Namespace;

class Obfuscator {
    public static void main(String[] args) {
        ArgumentParser parser = ArgumentParsers.newFor("obfuscate").build().defaultHelp(true)
                .description("Obfuscate: command line obfuscate module");

        parser.addArgument("-l", "--language")
                .setDefault("SystemVerilog")
                .required(false)
                .dest("language")
                .choices("SystemVerilog", "VHDL")
                .help("Language of the source file");

        parser.addArgument("mapfile")
                .help("Map file to be used");

        parser.addArgument("inputfile")
                .help("Source file");

        parser.addArgument("outputfile")
                .help("Source file");

        try {
            Namespace namespace = parser.parseArgs(args);
            final var language = namespace.getString("language");
            final var mapfile = namespace.getString("mapfile");
            final var inputfile = namespace.getString("inputfile");
            final var outputfile = namespace.getString("outputfile");

            Obfuscator obfuscate = new Obfuscator();
            obfuscate.processFile(Language.getElementByName(language), mapfile, inputfile, outputfile);

        } catch (ArgumentParserException exception) {
            parser.printHelp();
            System.exit(127);
        }
    }

    public void processFile(final Language language, final String mapFile, final String inFile, final String outFile) {
        switch (language) {
            default:
            case SYSTEM_VERILOG:
                this.sysVeriObfuscate(mapFile, inFile, outFile);
                break;

            case VHDL:
                this.vhdlObfuscate(mapFile, inFile, outFile);
                break;
        }
        ;
    }

    public void sysVeriObfuscate(String mapFile, String inFile, String outFile) {
        try {
            final var sysVeriObfuscator = SystemVerilogObfuscator.create(mapFile, inFile, outFile);
            sysVeriObfuscator.generateObfuscatedFile();

        } catch (ObfuscatorException exception) {
            System.out.println(exception.getMessage());
        }
    }

    public void vhdlObfuscate(String mapFile, String inFile, String outFile) {
        try {
            final var vhdlObfuscator = VhdlObfuscator.create(mapFile, inFile, outFile);
            vhdlObfuscator.generateObfuscatedFile();

        } catch (ObfuscatorException exception) {
            System.out.println(exception.getMessage());
        }
    }
}
