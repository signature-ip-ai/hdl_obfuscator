package com.signature.hdlobf;

import java.util.List;

public enum Language {
    SYSTEM_VERILOG(0, "SystemVerilog"),
    VHDL(1, "VHDL"),
    SYSTEM_C(2, "SystemC");

    private final int id;
    private final String name;

    private Language(final int id, final String name) {
        this.id = id;
        this.name = name;
    }

    private static List<Language> getElements() {
        return List.of(
                Language.SYSTEM_VERILOG,
                Language.VHDL,
                Language.SYSTEM_C);
    }

    public int getId() {
        return this.id;
    }

    public String getName() {
        return this.name;
    }

    public static Language getElementByName(final String name) {
        for (var language : getElements()) {
            if (language.getName().equalsIgnoreCase(name)) {
                return language;
            }
        }

        return Language.SYSTEM_VERILOG;
    }
}
