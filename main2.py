import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

def obter_data_atual():
    data_atual = datetime.now()
    return data_atual.strftime("%Y-%m-%d %H:%M:%S")


def calcular_custo_total_leasing(valor_equipamento, taxa_leasing, prazo_leasing, outras_despesas_leasing):
    custo_total_leasing = valor_equipamento + (valor_equipamento * taxa_leasing * prazo_leasing) + outras_despesas_leasing
    return custo_total_leasing

def calcular_custo_total_financiamento(valor_equipamento, taxa_financiamento, prazo_financiamento, outras_despesas_financiamento):
    custo_total_financiamento = valor_equipamento + (valor_equipamento * taxa_financiamento * prazo_financiamento) + outras_despesas_financiamento
    return custo_total_financiamento



def motivo(custo_leasing, custo_financiamento, taxa_leasing, taxa_financiamento, prazo_leasing, prazo_financiamento, outras_despesas_leasing, outras_despesas_financiamento):
    motivo = ""

    if custo_leasing < custo_financiamento:
        motivo += "Leasing é a melhor opção porque:\n"
    else:
        motivo += "Financiamento é a melhor opção porque:\n"

    if custo_leasing < custo_financiamento:
        motivo += f"  - O custo total do leasing ({custo_leasing:.2f}) é menor do que o custo total do financiamento ({custo_financiamento:.2f}).\n"
    else:
        motivo += f"  - O custo total do financiamento ({custo_financiamento:.2f}) é menor do que o custo total do leasing ({custo_leasing:.2f}).\n"

    if taxa_leasing > taxa_financiamento:
        motivo += f"  - A taxa de leasing ({taxa_leasing:.2%}) é maior do que a taxa de financiamento ({taxa_financiamento:.2%}).\n"
    elif taxa_leasing < taxa_financiamento:
        motivo += f"  - A taxa de leasing ({taxa_leasing:.2%}) é menor do que a taxa de financiamento ({taxa_financiamento:.2%}).\n"
    else:
        motivo += "  - As taxas de leasing e financiamento são iguais.\n"

    if prazo_leasing > prazo_financiamento:
        motivo += f"  - O prazo de leasing ({prazo_leasing} meses) é maior do que o prazo de financiamento ({prazo_financiamento} meses).\n"
    elif prazo_leasing < prazo_financiamento:
        motivo += f"  - O prazo de leasing ({prazo_leasing} meses) é menor do que o prazo de financiamento ({prazo_financiamento} meses).\n"
    else:
        motivo += "  - Os prazos de leasing e financiamento são iguais.\n"

    if outras_despesas_leasing > outras_despesas_financiamento:
        motivo += f"  - As outras despesas associadas ao leasing ({outras_despesas_leasing:.2f}) são maiores do que as do financiamento ({outras_despesas_financiamento:.2f}).\n"
    elif outras_despesas_leasing < outras_despesas_financiamento:
        motivo += f"  - As outras despesas associadas ao leasing ({outras_despesas_leasing:.2f}) são menores do que as do financiamento ({outras_despesas_financiamento:.2f}).\n"
    else:
        motivo += "  - As outras despesas associadas ao leasing e ao financiamento são iguais.\n"

    return motivo



# Função para calcular custo total
def calcular_custo_total(valor, taxa, prazo, outras_despesas):
    return valor * (1 + taxa) + outras_despesas

# Função para calcular valor da parcela
def calcular_valor_parcela(custo_total, prazo):
    if custo_total>0:
        return custo_total / prazo

def main():
    st.title("Comparação entre Leasing e Financiamento")

    valor_equipamento = st.number_input("Digite o valor do equipamento:")

    st.sidebar.subheader("Taxas de Leasing:")
    taxa_leasing = st.sidebar.slider("Taxa de leasing (%)", min_value=0.0, max_value=50.0, step=0.1, value=2.0) / 100
    prazo_leasing = st.sidebar.number_input("Digite o prazo de leasing em meses:")
    outras_despesas_leasing = st.sidebar.number_input("Digite outras despesas associadas ao leasing:")

    st.sidebar.subheader("Taxas de Financiamento:")
    taxa_financiamento = st.sidebar.slider("Taxa de financiamento (%)", min_value=0.0, max_value=50.0, step=0.1, value=2.0) / 100
    prazo_financiamento = st.sidebar.number_input("Digite o prazo de financiamento em meses:")
    outras_despesas_financiamento = st.sidebar.number_input("Digite outras despesas associadas ao financiamento:")

    # Inicializando resultados
    resultado_leasing = None
    resultado_financiamento = None

    # Calculando custo e parcela para leasing se todos os campos estiverem preenchidos
    if valor_equipamento and taxa_leasing and prazo_leasing:
        custo_leasing = calcular_custo_total(valor_equipamento, taxa_leasing, prazo_leasing, outras_despesas_leasing)
        valor_parcela_leasing = calcular_valor_parcela(custo_leasing, prazo_leasing)
        diferenca_valor_total_leasing = abs(valor_equipamento - custo_leasing)
        resultado_leasing = {
            "Tipo": "Leasing",
            "Valor Inicial": valor_equipamento,
            "Custo Total": custo_leasing,
            "Diferença Valor Total": diferenca_valor_total_leasing,
            "Valor da Parcela": valor_parcela_leasing
        }

    # Calculando custo e parcela para financiamento se todos os campos estiverem preenchidos
    if valor_equipamento and taxa_financiamento and prazo_financiamento:
        custo_financiamento = calcular_custo_total(valor_equipamento, taxa_financiamento, prazo_financiamento, outras_despesas_financiamento)
        valor_parcela_financiamento = calcular_valor_parcela(custo_financiamento, prazo_financiamento)
        diferenca_valor_total_financiamento = abs(valor_equipamento - custo_financiamento)
        resultado_financiamento = {
            "Tipo": "Financiamento",
            "Valor Inicial": valor_equipamento,
            "Custo Total": custo_financiamento,
            "Diferença Valor Total": diferenca_valor_total_financiamento,
            "Valor da Parcela": valor_parcela_financiamento
        }

    # Se ambos os resultados estão disponíveis, compare-os
    if resultado_leasing and resultado_financiamento:
        resultados_comparados = [resultado_leasing, resultado_financiamento]
        # Adicionando a diferença entre parcelas à tabela
        st.subheader("Resultados Comparados:")
        st.table(resultados_comparados)

        
    else:
        # Se apenas um resultado está disponível, mostre-o
        resultado_disponivel = resultado_leasing or resultado_financiamento
        if resultado_disponivel:
            st.subheader(f"Resultado para {resultado_disponivel['Tipo']}:")
            st.markdown(f"**Valor Inicial:** R$ {resultado_disponivel['Valor Inicial']:.2f}")
            st.markdown(f"**Custo Total:** R$ {resultado_disponivel['Custo Total']:.2f}")
            st.markdown(f"**Diferença Valor Total:** R$ {resultado_disponivel['Diferença Valor Total']:.2f}")
            st.markdown(f"**Valor da Parcela:** R$ {resultado_disponivel['Valor da Parcela']:.2f}")

    if resultado_leasing and resultado_financiamento:
        resultados_comparados = [resultado_leasing, resultado_financiamento]
        
        # Adicionando a diferença entre parcelas à tabela
        for resultado in resultados_comparados:
            resultado["Valor Pago em Juros"] = resultado.get("Diferença Valor Total", None)

        # Criando a tabela de diferença entre valores totais
        df_diferenca_valores_totais = pd.DataFrame(resultados_comparados)[["Tipo", "Valor Pago em Juros"]]
        st.subheader("Valor Pago em Juros:")
        st.table(df_diferenca_valores_totais)

        # Chamando a função motivo para exibir a explicação detalhada
        motivo_detalhado = motivo(custo_leasing, custo_financiamento, taxa_leasing, taxa_financiamento, prazo_leasing, prazo_financiamento, outras_despesas_leasing, outras_despesas_financiamento)
        st.subheader("Motivo Detalhado:")
        st.text(motivo_detalhado)
    
    
    


if __name__ == "__main__":
    main()