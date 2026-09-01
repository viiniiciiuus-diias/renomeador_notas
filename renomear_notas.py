import fitz
import os
import re
import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

PASTA = r"C:\TEMP"
LOG = r"C:\TEMP\renomeador.log"

def log(mensagem):

    texto = f"{datetime.now():%d/%m/%Y %H:%M:%S} - {mensagem}"

    try:
        print(texto)

        with open(LOG, "a", encoding="utf-8") as f:
            f.write(texto + "\n")

    except Exception:
        pass

def limpar_nome(nome):
    nome = re.sub(r'[\\/:*?"<>|&]', ' ', nome)
    nome = re.sub(r'\s+', ' ', nome)
    return nome.strip()


def arquivo_ja_processado(nome):

    nome_upper = nome.upper().strip()

    if nome_upper.startswith("NF "):
        return True

    if nome_upper.startswith("XML "):
        return True

    if nome_upper.startswith("CCE "):
        return True

    if " NF " in nome_upper and nome_upper.endswith("B.PDF"):
        return True

    return False


def ler_pdf(caminho):

    texto = ""

    try:

        with fitz.open(caminho) as pdf:

            texto = ""

            for pagina in pdf:
                texto += pagina.get_text()

            paginas = len(pdf)

        return texto, paginas

    except Exception as erro:

        print(f"Erro ao ler PDF: {caminho}")
        print(erro)

        log(f"Erro ao ler PDF: {caminho}")
        log(str(erro))

        return "", 0


def extrair_nf_danfe(texto):

    match = re.search(r'N\.\s*(\d+)', texto)

    if match:
        return match.group(1)

    return None


def extrair_chave(texto):

    chave = re.search(r'(\d{44})', re.sub(r'\D', '', texto))

    if chave:
        return chave.group(1)

    return None


def eh_boleto(texto):
    return "RECIBO DO PAGADOR" in texto.upper()


def eh_modelo2(texto):

    cnpjs_modelo2 = [
        "40.965.172",
        "48.626.594",
        "63.517.439" 
    ]

    return any(cnpj in texto for cnpj in cnpjs_modelo2)


def eh_cce(texto):

    texto = texto.upper()

    return (
        "CARTA DE CORREÇÃO ELETRÔNICA" in texto
        or
        "CARTA DE CORRECAO ELETRONICA" in texto
    )


def extrair_nf_cce(texto):

    match = re.search(
        r'Número\s*(\d{6,9})',
        texto,
        re.IGNORECASE
    )

    if match:
        return match.group(1).zfill(9)

    return None


def extrair_razao_boleto(texto):

    linhas = [linha.strip() for linha in texto.splitlines()]

    for i, linha in enumerate(linhas):

        if "PAGADOR" in linha.upper():

            for j in range(i + 1, min(i + 5, len(linhas))):

                if "CNPJ" in linhas[j].upper():

                    razao = linhas[j].split("- CNPJ")[0].strip()

                    return limpar_nome(razao)

    return "CLIENTE"


def extrair_nf_boleto(texto):

    match = re.search(r'000(\d{6})01\s*DM', texto)

    if match:
        return match.group(1)

    return "SEMNF"

def registrar_boleto(razao, nf, paginas):

    arquivo_csv = r"C:\TEMP\historico_boletos.csv"   

    with open(arquivo_csv, "a", encoding="utf-8") as f:

        f.write(
            f"{datetime.now():%d/%m/%Y};{razao};{nf};{paginas}B\n"
        )


def processar_pdf(caminho):

    if not os.path.exists(caminho):
        return

    texto = ""
    paginas = 0

    for _ in range(5):

        try:

            texto, paginas = ler_pdf(caminho)

            if texto:
                break

        except:
            pass

        time.sleep(1)

    else:
        return

    nome_original = os.path.basename(caminho)

    if arquivo_ja_processado(nome_original):
        return

    # CCE
    if eh_cce(texto):

        nf = extrair_nf_cce(texto)

        if not nf:
            log(f"CCE sem número: {nome_original}")
            return

        novo_nome = f"CCE {nf}.pdf"

        destino = os.path.join(PASTA, novo_nome)

        if os.path.exists(destino):
            log(f"Já existe: {novo_nome}")
            return

        os.rename(caminho, destino)

        log(f"CCE -> {novo_nome}")
        return

    # BOLETO
    if eh_boleto(texto):

        razao = extrair_razao_boleto(texto)
        nf = extrair_nf_boleto(texto)

        novo_nome = f"{razao} NF {nf} {paginas}B.pdf"

        destino = os.path.join(PASTA, novo_nome)

        if os.path.exists(destino):
            log(f"Já existe: {novo_nome}")
            return

        os.rename(caminho, destino)

        registrar_boleto(
            razao,
            nf,
            paginas
        )

        log(f"BOLETO -> {novo_nome}")
        return

    # DANFE
    nf = extrair_nf_danfe(texto)

    if not nf:
        log(f"NF não encontrada em {nome_original}")
        return

    if eh_modelo2(texto):

        nf_sem_zero = str(int(nf))
        novo_nome = f"NF {nf_sem_zero}.pdf"

    else:

        nf_formatada = nf.zfill(9)
        novo_nome = f"NF {nf_formatada}.pdf"

    destino = os.path.join(PASTA, novo_nome)

    if os.path.exists(destino):
        log(f"Já existe: {novo_nome}")
        return

    os.rename(caminho, destino)
    log(f"PDF -> {novo_nome}")


def processar_xml(caminho):

    if not os.path.exists(caminho):
        return

    nome = os.path.basename(caminho)

    nome_upper = nome.upper().strip()

    if nome_upper.startswith("XML"):
        return

    match = re.search(r'(\d{44})', nome)

    if not match:
        return

    chave = match.group(1)

    # NF = posições 26 a 34 da chave
    nf = chave[25:34]

    novo_nome = f"XML {nf}.xml"

    destino = os.path.join(PASTA, novo_nome)

    try:

        os.rename(caminho, destino)
        log(f"XML -> {novo_nome}")

    except Exception as erro:

        log(f"Erro ao renomear {nome}: {erro}")


# Primeiro PDFs
for arquivo in os.listdir(PASTA):

    if arquivo.lower().endswith(".pdf"):

        processar_pdf(os.path.join(PASTA, arquivo))

# Depois XMLs
for arquivo in os.listdir(PASTA):

    if arquivo.lower().endswith(".xml"):

        processar_xml(os.path.join(PASTA, arquivo))

log("")
log("=" * 60)
log("RENOMEADOR INICIADO")
log(f"Pasta monitorada: {PASTA}")
log("=" * 60)

class MonitorPasta(FileSystemEventHandler):

    def on_created(self, event):

        if event.is_directory:
            return

        caminho = event.src_path

        time.sleep(3)

        if not os.path.exists(caminho):
            return

        try:

            if caminho.lower().endswith(".pdf"):
                processar_pdf(caminho)

            elif caminho.lower().endswith(".xml"):
                processar_xml(caminho)

        except Exception as erro:
            log(f"ERRO: {caminho} - {erro}")


    def on_moved(self, event):

        if event.is_directory:
            return

        caminho = event.dest_path

        time.sleep(1)

        if not os.path.exists(caminho):
            return

        try:

            if caminho.lower().endswith(".pdf"):
                processar_pdf(caminho)

            elif caminho.lower().endswith(".xml"):
                processar_xml(caminho)

        except Exception as erro:
            log(f"Erro ao processar {caminho}: {erro}")


observer = Observer()
observer.schedule(
    MonitorPasta(),
    PASTA,
    recursive=False
)

observer.start()

try:

    while True:
        time.sleep(1)

except KeyboardInterrupt:

    observer.stop()

observer.join()