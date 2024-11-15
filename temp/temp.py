@app.command()
def testprogram():
    # Ruta del archivo .log
    log_file = "1A626AY00_ICT_GDL_BAH_AF118-05_1A626AY00804AC0XY_202411131719_FAILED.log"

    # Ejecutar la función
    failed_parts = extract_failed_parts(log_file)
    if failed_parts:
        print(f"IDs de partes que fallaron: {failed_parts}")
    else:
        print("No se encontraron partes con 'HAS FAILED' en el archivo.")

def extract_failed_parts(file_path):
    failed_parts = []
    with open(file_path, 'r') as file:
        for line in file:
            matches = re.findall(r"(\S+?) HAS FAILED", line)
            if matches:
                failed_parts.extend(matches)
    return failed_parts