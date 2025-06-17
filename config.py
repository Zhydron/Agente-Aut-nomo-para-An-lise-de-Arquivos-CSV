# config.py

# config.py

import os
from dotenv import load_dotenv


class Config:
    """
    Carrega e valida as variáveis de ambiente necessárias para o agente.
    Compatível com Gemini (Google) e OpenAI.
    """
    def __init__(self):
        load_dotenv()

        # Chaves de API
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

        # Caminhos dos arquivos CSV
        self.header_path = os.getenv("HEADER_PATH", "./202401_NFs_Cabecalho.csv")
        self.items_path = os.getenv("ITEMS_PATH", "./202401_NFs_Itens.csv")

        # Configurações diversas
        self.verbose = os.getenv("VERBOSE", "False").lower() == "true"
        self.log_level = os.getenv("LOG_LEVEL", "INFO").upper()

        # Validar todas as configurações críticas
        self._validate()

    def _validate(self):
        # Pelo menos uma API key deve estar presente
        if not self.google_api_key and not self.openai_api_key:
            raise ValueError("É necessário definir GOOGLE_API_KEY ou OPENAI_API_KEY no .env")

        for path in [self.header_path, self.items_path]:
            if not os.path.exists(path):
                raise FileNotFoundError(f"Arquivo CSV não encontrado: {path}")


def load_config():
    return Config()

