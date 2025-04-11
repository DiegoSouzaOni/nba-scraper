import os


def exportar_df_para_csv(df, nome_arquivo, pasta="outputs"):
    if df.empty:
        print("⚠️ DataFrame vazio, nada foi exportado.")
        return

    os.makedirs(pasta, exist_ok=True)
    caminho_completo = os.path.join(pasta, f"{nome_arquivo}.csv")
    
    df.to_csv(caminho_completo, index=False, encoding='utf-8-sig')
    print(f"✅ Arquivo CSV exportado com sucesso: {caminho_completo}")
