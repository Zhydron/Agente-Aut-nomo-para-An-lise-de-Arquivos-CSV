#!/usr/bin/env python3
"""
Arquivo: agente.py
Implementação do script principal que carrega configurações, dados e interage com o usuário via CLI,
utilizando LangChain para criar um agente capaz de consultar o DataFrame resultante.
"""
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Agora você pode acessar as variáveis de ambiente
api_key = os.getenv("GOOGLE_API_KEY")
app_debug = os.getenv("APP_DEBUG")

import logging
import sys
import pandas as pd

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents import create_pandas_dataframe_agent

from config import load_config
from data_loader import load_header, load_items, merge_data


def main():
    # Carregamento de configurações
    config = load_config()

    # Configuração de logging
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        level=config.log_level
    )
    logger = logging.getLogger(__name__)

    logger.info("Iniciando agente de análise de CSV com LangChain e Gemini")

    # Leitura e preparação de dados
    try:
        logger.debug("Carregando arquivo de cabeçalho: %s", config.header_path)
        df_head = load_header(config.header_path)

        logger.debug("Carregando arquivo de itens: %s", config.items_path)
        df_items = load_items(config.items_path)

        logger.debug("Realizando merge dos DataFrames")
        df = merge_data(df_head, df_items)

        logger.info("Dados carregados com sucesso: %d registros", len(df))
    except Exception as e:
        logger.error("Falha ao carregar dados: %s", e, exc_info=True)
        sys.exit(1)

    # Instanciação do LLM e criação do agente com Gemini
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash-latest",
            temperature=0,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        logger.debug("Criando agente Pandas DataFrame Agent com Gemini")
        agent = create_pandas_dataframe_agent(
            llm=llm,
            df=df,
            verbose=config.verbose,
            allow_dangerous_code=True
        )
        logger.info("Agente criado com sucesso com Gemini")
    except Exception as e:
        logger.error("Falha ao criar agente LangChain com Gemini: %s", e, exc_info=True)
        sys.exit(1)

    # Loop de interação com o usuário
    try:
        while True:
            query = input("Pergunta (ou 'sair' para encerrar): ").strip()
            if query.lower() in {"sair", "exit"}:
                logger.info("Encerrando sessão a pedido do usuário")
                break

            try:
                # agent.run retorna output direto para Pandas agents
                output = agent.run(query)
                print(output)
            except Exception as inner_e:
                logger.error("Erro na execução da query '%s': %s", query, inner_e, exc_info=True)
                print("Ocorreu um erro ao processar sua pergunta. Tente novamente.")
    except KeyboardInterrupt:
        logger.info("Interação interrompida pelo usuário")
    finally:
        logger.info("Aplicação finalizada")


if __name__ == "__main__":
    main()
