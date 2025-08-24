#
# Arquivo: src/main.py
#
# Este é o arquivo principal que orquestra o processo de leitura e escrita
# da planilha.
#

# --- 1. Importação de Bibliotecas e Módulos Locais ---
import pandas as pd
import time
# Importa a função `geocodificar_endereco` do módulo `geocoder.py`.
# Isso torna seu código mais organizado e modular.
from geocoder import geocodificar_endereco

# --- 2. Função de Processamento do Arquivo Excel ---
def processar_excel(caminho_arquivo_entrada, nome_coluna_endereco, caminho_arquivo_saida):
    """
    Processa um arquivo Excel, geocodifica endereços e adiciona coordenadas.
    """
    try:
        print("Lendo o arquivo Excel...")
        # Usa pandas para ler o arquivo Excel. O `engine="odf"` é necessário para arquivos .ods.
        df = pd.read_excel(caminho_arquivo_entrada, engine="odf")
        
        # Cria listas vazias para armazenar as coordenadas. É mais eficiente
        # do que adicionar diretamente ao DataFrame em cada iteração.
        latitudes = []
        longitudes = []

        print("Iniciando a geocodificação em cascata...")
        # O `for` loop itera sobre cada linha do DataFrame.
        for index, row in df.iterrows():
            # Pega o endereço da coluna especificada.
            endereco = row[nome_coluna_endereco]
            # Chama a função de geocodificação do arquivo `geocoder.py`.
            latitude, longitude = geocodificar_endereco(endereco)
            # Adiciona as coordenadas encontradas (ou None) nas listas.
            latitudes.append(latitude)
            longitudes.append(longitude)

            # O `time.sleep(1)` pausa o script por 1 segundo.
            # Isso é fundamental para evitar sobrecarregar os servidores das APIs,
            # que podem te bloquear temporariamente (rate-limiting).
            time.sleep(4)

        # Após o loop, adiciona as listas completas como novas colunas no DataFrame.
        df['Latitude'] = latitudes
        df['Longitude'] = longitudes

        print(f"\nSalvando o arquivo modificado como '{caminho_arquivo_saida}'...")
        # Salva o DataFrame em um novo arquivo Excel.
        # `index=False` evita que o pandas salve o índice do DataFrame como uma coluna.
        df.to_excel(caminho_arquivo_saida, index=False)
        print("Processo concluído com sucesso!")

    # --- 3. Tratamento de Exceções (Erros) ---
    # `try...except` é a maneira de Python de lidar com erros previsíveis.
    # Se o código dentro do `try` falhar, ele executa o bloco `except` correspondente.
    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_arquivo_entrada}' não foi encontrado.")
    except KeyError:
        # Erro que acontece se o nome da coluna de endereços estiver incorreto.
        print(f"Erro: A coluna '{nome_coluna_endereco}' não foi encontrada no arquivo Excel.")
    except Exception as e:
        # Uma exceção mais genérica para qualquer outro erro inesperado.
        print(f"Ocorreu um erro: {e}")

# --- 4. Ponto de Entrada do Script ---
# O bloco `if __name__ == "__main__":` é uma convenção Python para indicar que
# o código dentro dele só deve ser executado quando o script é chamado diretamente.
# Se o arquivo for importado por outro script, este bloco não será executado.
if __name__ == "__main__":
    # Define as variáveis de configuração em um único lugar.
    ARQUIVO_ENTRADA = 'data/input/Uniformes.ods'
    COLUNA_ENDERECO = 'ENDEREÇOS'
    ARQUIVO_SAIDA = './data/output/enderecos_uniformes.xlsx'

    # Chama a função principal para iniciar o processo.
    processar_excel(ARQUIVO_ENTRADA, COLUNA_ENDERECO, ARQUIVO_SAIDA)

  