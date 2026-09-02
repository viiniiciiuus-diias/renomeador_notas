# Renomeador de Notas

Automação em Python para identificação, padronização e organização de documentos fiscais.

## 📌 Sobre o projeto

O **Renomeador de Notas** foi desenvolvido para automatizar uma etapa operacional do processo de faturamento: a identificação e padronização de arquivos fiscais recebidos em uma pasta.

A aplicação monitora continuamente uma pasta definida e, ao identificar novos documentos, analisa seu conteúdo para determinar o tipo de arquivo e aplicar automaticamente uma nomenclatura padronizada.

O objetivo é reduzir tarefas manuais, melhorar a organização dos documentos e diminuir erros de identificação e renomeação.

## ⚙️ Funcionalidades

Atualmente, o sistema trabalha com os seguintes tipos de documentos:

### DANFE / Nota Fiscal

Identifica o número da nota fiscal diretamente no PDF e renomeia o arquivo seguindo o padrão:

```text
NF 280614.pdf
```

O sistema também possui regras específicas de nomenclatura para determinados modelos de DANFE.

### Boleto

Identifica boletos a partir do conteúdo do documento, extraindo informações como:

* Razão social do pagador
* Número da nota fiscal
* Quantidade de páginas

O arquivo é renomeado seguindo um padrão semelhante a:

```text
Empresa NF 280614 2B.pdf
```

Além disso, as informações processadas são registradas em um arquivo histórico.

### Carta de Correção Eletrônica (CC-e)

Identifica documentos de Carta de Correção Eletrônica e extrai o número correspondente.

Exemplo:

```text
CCE 123456789.pdf
```

### XML

Identifica a chave de acesso da NF-e e utiliza a numeração da nota fiscal presente na chave para padronizar o nome:

```text
XML 280614.xml
```

## 🔄 Funcionamento

O fluxo básico da aplicação é:

```text
Arquivo recebido
       ↓
Pasta monitorada
       ↓
Identificação do tipo de documento
       ↓
Leitura do conteúdo
       ↓
Extração das informações
       ↓
Aplicação das regras de nomenclatura
       ↓
Arquivo renomeado
       ↓
Registro no log / histórico
```

A aplicação utiliza o `watchdog` para detectar automaticamente novos arquivos adicionados à pasta monitorada.

Também existe um processamento inicial dos arquivos que já estavam presentes na pasta quando o sistema é iniciado.

## 🛠️ Tecnologias utilizadas

* **Python**
* **PyMuPDF (fitz)** — leitura e extração de texto de arquivos PDF
* **Watchdog** — monitoramento da pasta em tempo real
* **Pandas** — utilizado no tratamento/registro de dados do histórico
* **Git** — controle de versão
* **GitHub** — hospedagem e versionamento do projeto

## 📁 Estrutura atual

```text
renomeador_notas/
│
├── renomear_notas.py
├── iniciar_renomeador.bat
├── RenomearAutomatico.vbs
├── .gitignore
└── venv/
```

### `renomear_notas.py`

Arquivo principal da aplicação. Contém as regras de identificação, extração das informações, renomeação e monitoramento da pasta.

### `iniciar_renomeador.bat`

Script utilizado para iniciar a aplicação utilizando o Python do ambiente virtual do projeto.

### `RenomearAutomatico.vbs`

Utilizado para iniciar o processo automaticamente no Windows, sem a necessidade de abrir manualmente o terminal.

## ▶️ Como executar

### Pré-requisitos

* Windows
* Python instalado
* Ambiente virtual configurado
* Dependências instaladas

### Execução manual

Com o ambiente virtual configurado, execute:

```cmd
venv\Scripts\python.exe renomear_notas.py
```

Ou utilize:

```cmd
iniciar_renomeador.bat
```

## 📂 Pasta monitorada

Por padrão, a aplicação monitora:

```text
C:\TEMP
```

Os arquivos encontrados nessa pasta são analisados e processados conforme as regras implementadas.

## 📝 Logs

A aplicação mantém um arquivo de log em:

```text
C:\TEMP\renomeador.log
```

O log permite acompanhar a inicialização e o processamento dos documentos.

## 🔐 Dados

Este repositório não contém documentos fiscais reais, PDFs, XMLs ou dados operacionais utilizados no ambiente de trabalho.

Os identificadores presentes no código são utilizados exclusivamente para representar regras necessárias ao funcionamento da automação.

## 🚀 Possíveis evoluções

Algumas melhorias consideradas para versões futuras:

* Organização automática dos documentos em pastas de destino;
* Configuração das regras sem necessidade de alterar o código;
* Histórico mais completo dos documentos processados;
* Banco de dados para armazenamento das informações;
* Interface para acompanhamento dos arquivos processados;
* Associação entre NF, XML, boleto e CC-e;
* Modo de diagnóstico/teste;
* Maior cobertura de testes automatizados.

## 🎯 Objetivo profissional

Este projeto faz parte do meu portfólio de desenvolvimento voltado para **Análise de Dados, automação de processos e aplicação de tecnologia em problemas reais de negócio**.

A proposta é utilizar programação não apenas para desenvolver sistemas, mas principalmente para identificar tarefas repetitivas e criar soluções que tragam mais padronização, produtividade e confiabilidade aos processos.

---

**Projeto:** Renomeador de Notas
**Linguagem:** Python
**Plataforma:** Windows
