# Projeto de Georreferenciamento de Endereços

Este projeto em Python é um script para georreferenciar endereços a partir de uma planilha Excel (`.ods`). Ele utiliza a API do Google Maps (com chave) e o serviço gratuito Nominatim em um sistema de "cascata" para garantir a maior taxa de sucesso possível na busca por coordenadas de latitude e longitude.

### Como Usar

1.  **Instale as dependências:**
    Certifique-se de ter o Python 3 instalado. Em seguida, instale as bibliotecas necessárias usando o arquivo `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure sua Chave da API do Google Maps:**
    Abra o arquivo `src/geocoder.py` e substitua `"SUA_CHAVE_VALIDA_AQUI"` pela sua chave de API válida do Google. Lembre-se que o serviço do Google exige a configuração de faturamento.

3.  **Coloque o arquivo de entrada:**
    Adicione sua planilha de endereços (`Uniformes.ods`) na pasta `data/input/`.

4.  **Execute o script:**
    No terminal, a partir da pasta raiz do projeto, execute o script principal:
    ```bash
    python src/main.py
    ```
    O arquivo de saída `enderecos_geocodificados_cascata.xlsx` será salvo na pasta `data/output/`.
5.  **Ambiente virtual:**
  
    
    rm -rf venv    remove maq virtual antiga se der problema
    python3 -m venv venv      cria o ambiente virtual
    source venv/bin/activate   ativa o ambiente vitual
    deactivate                 desativa o ambiente virtual
    Executar:     python main.py 
    
