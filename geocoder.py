#
# Arquivo: src/geocoder.py
#
# Este módulo contém a lógica de geocodificação em cascata, usando múltiplas
# APIs para garantir a melhor taxa de sucesso na conversão de endereços
# em coordenadas geográficas.
#

# --- 1. Importação de Bibliotecas ---
# Importa a biblioteca 'geopy' para usar os geocodificadores
# do Google Maps e Nominatim.
from geopy.geocoders import GoogleV3, Nominatim
# Importa o módulo 'requests' para fazer a chamada à API da Distancematrix.ai.
import requests
# Importa o 'time' para fazer pequenas pausas.
import time

# --- 2. Variáveis de Configuração ---
# Chave da API do Google Maps. Se não for fornecida, esta etapa será ignorada.
API_KEY_GOOGLE = "68a76c53ea234238714621ujka7bee3"
# Chave da API da Distancematrix.ai. Insira sua chave aqui.

# Constrói o User-Agent necessário para o Nominatim.
USER_AGENT_NOMINATIM = "geocodificacao-script"

# Inicializa os geocodificadores com as chaves e o User-Agent.
geolocator_google = GoogleV3(api_key=API_KEY_GOOGLE)
geolocator_nominatim = Nominatim(user_agent=USER_AGENT_NOMINATIM)

# --- 3. Função de Limpeza do Endereço ---
def limpar_endereco(endereco):
    """
    Remove caracteres desnecessários e espaços extras do endereço.
    """
    if isinstance(endereco, str):
        return endereco.strip().replace('\n', ', ').replace('\r', '')
    return None

# --- 4. Função Principal de Geocodificação em Cascata ---
def geocodificar_endereco(endereco_original):
    """
    Tenta geocodificar um endereço usando uma estratégia em cascata:
    1. Google Maps
    2. Nominatim
    """
    # Limpa o endereço de entrada para um formato padronizado.
    endereco_limpo = limpar_endereco(endereco_original)
    
    # Se o endereço for nulo ou vazio, retorna sem tentar a geocodificação.
    if not endereco_limpo:
        print(f"Endereço inválido. Pulando a linha.")
        return None, None

    # Tenta obter a localização usando o Google Maps (Etapa 1).
    if API_KEY_GOOGLE:
        try:
            print(f"Buscando '{endereco_limpo}' com a API do Google...")
            localizacao_google = geolocator_google.geocode(endereco_limpo, timeout=5)
            if localizacao_google:
                print(f"  --> SUCESSO! Coordenadas encontradas pelo Google.")
                return localizacao_google.latitude, localizacao_google.longitude
        except Exception as e:
            print(f"  --> Erro na API do Google: {e}. Tentando próxima API...")
    
    
    # Tenta obter a localização usando o Nominatim (Etapa 3 - Fallback).
    try:
        print(f"Buscando '{endereco_limpo}' com a API do Nominatim...")
        localizacao_nominatim = geolocator_nominatim.geocode(endereco_limpo, timeout=5)
        if localizacao_nominatim:
            print(f"  --> SUCESSO! Coordenadas encontradas pelo Nominatim.")
            return localizacao_nominatim.latitude, localizacao_nominatim.longitude
    except Exception as e:
        print(f"  --> Erro na API do Nominatim: {e}")

    # Se todas as tentativas falharem.
    print(f"  --> FALHA! Nenhuma coordenada encontrada para o endereço '{endereco_limpo}'.")
    return None, None

