import argparse
import ctypes
import ctypes.util
import sys
from pathlib import Path

from codegen import genera_ir
from parser import ErroreSintattico, parse_file
from semantica import analizza
from symbol_table import ErroreSemantico


def compila(percorso):
    return genera_ir(analizza(parse_file(percorso)))


def svuota_buffer_c():
    try:
        libc = ctypes.CDLL(ctypes.util.find_library("c"))
        libc.fflush(None)
    except (OSError, TypeError):
        pass


def esegui(codice_ir):
    import llvmlite.binding as llvm

    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()
    modulo = llvm.parse_assembly(codice_ir)
    modulo.verify()
    macchina = llvm.Target.from_default_triple().create_target_machine()
    motore = llvm.create_mcjit_compiler(modulo, macchina)
    motore.finalize_object()
    indirizzo = motore.get_function_address("main")
    ctypes.CFUNCTYPE(ctypes.c_int)(indirizzo)()
    svuota_buffer_c()


def main(argomenti=None):
    parser = argparse.ArgumentParser(description="Compilatore per il linguaggio .al")
    parser.add_argument("sorgente", help="file .al da compilare")
    parser.add_argument("-o", "--output", help="file .ll da generare")
    parser.add_argument(
        "--run", action="store_true", help="esegue il programma dopo la compilazione"
    )
    args = parser.parse_args(argomenti)

    try:
        codice_ir = compila(args.sorgente)
    except (ErroreSintattico, ErroreSemantico) as errore:
        print(f"Errore: {errore}", file=sys.stderr)
        return 1

    uscita = Path(args.output) if args.output else Path(args.sorgente).with_suffix(".ll")
    uscita.write_text(codice_ir, encoding="utf-8")

    if args.run:
        esegui(codice_ir)
    else:
        print(f"Generato {uscita}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
