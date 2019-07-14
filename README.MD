# Dados públicos CNPJ - Auxiliador para download dos zips

Software desenvolvido para auxiliar no download dos CNPJ do site da receita http://receita.economia.gov.br/orientacao/tributaria/cadastros/cadastro-nacional-de-pessoas-juridicas-cnpj/dados-publicos-cnpj

## Motivação

O download dos arquivos zips do site da receita federal estão disponibilizados em arquivos zips separados por partes.
O download através do site é lento e os dados são atualizado apenas de 3 em 3 meses.
A ideia é ter um software que possa fazer o download desses arquivos sem a necessidade de abrir o site e baixar um por um.
Também é possível agendar um scheduler para rodar de tempo em tempo através de linha de comando para baixar os zips sem necessidade de intervenção.

Os dados podem ser usados com auxílio da ferramenta [CNPJ-FULL](https://github.com/fabioserpa/CNPJ-full) 

### Pré requisitos

- Python

    O software é desenvolvido em python 3.3, é necessário que ele esteja instalado para rodar.
- Pip
  É necessário ter o pip instalado:
  ````
  python3 -m pip install --upgrade pip
  ````

### Preparação ambiente

Baixe o arquivo `dadosAbertos.py` e o arquivo `requirements.txt` para qualquer pasta do seu computador execute o comando:

Instale as dependências:
```
python3 install requirements.txt -r
```

### Utilização

Executar com parâmetros padrão:
````
  python3 dadosAbertos.py
````
Os dados serão salvo na pasta local\dados


Ver as opções para execução:
```
python dadosAbertos.py -h
```

Será exibido o help:
```
- Parametros opcionais:
-d diretório onde serão salvos os arquivos, padrão é ./dados
  Exemplo: 
  python dadosAbertos.py -d c:\cnpj

-t Quantidade de thread que será executada para fazer download simultaneamente, o padrão é 1
  Exemplo:
  python dadosAbertos.py -t 3
  Isso limitará o donwload em 3 por vez
```

#### Exemplos
  ````
  python3 dadosAbertos.py
  ````
  ````
  python3 dadosAbertos.py -t 3 -d c:\cnpj
  ````
  ````
  python3 dadosAbertos.py -d c:\cnpj
  ````
  ````
  python3 dadosAbertos.py -t 2
  ````

#### TODO
  - Verificador de arquivo corrompido
  - Resume de arquivo em caso de falha
