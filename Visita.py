import streamlit as st
from fpdf import FPDF
import datetime

st.set_page_config(page_title="Roteiro de Visita PJ", layout="wide")

st.title("📋 Roteiro de Visita Consultiva - Cliente PJ")
cliente = st.text_input("Nome do cliente:")
data_visita = st.date_input("Data da visita:", value=datetime.date.today())

st.markdown("### 1. Abertura e Quebra de Gelo")
st.text_area("Introdução / Impressão inicial", height=100)

st.markdown("### 2. Diagnóstico do Negócio")
socio = st.checkbox("Tem sócios?")
funcionarios = st.checkbox("Possui funcionários?")
faturamento = st.text_input("Faturamento médio mensal")
usa_app = st.checkbox("Usa o app BB Empresas?")

st.markdown("### 3. Recebimentos e Vendas")
pagamentos = st.multiselect(
    "Meios de pagamento aceitos:",
    ["Dinheiro", "Débito", "Crédito", "Pix", "Link de pagamento"]
)
maquininha = st.text_input("Maquininha usada (se houver)")

st.markdown("### 4. Fluxo de Caixa e Controles")
controle = st.selectbox("Como controla o fluxo de caixa?", ["Planilha", "Sistema", "Caderno", "Outro"])
precisa_giro = st.checkbox("Precisa de capital de giro?")
antecipacao = st.checkbox("Usa antecipação de recebíveis?")

st.markdown("### 5. Investimentos e Segurança")
tem_reserva = st.checkbox("Tem reserva de emergência da empresa?")
usa_seguros = st.checkbox("Possui seguros empresariais?")

st.markdown("### 6. Proposta de Valor")
st.text_area("Soluções sugeridas", height=150)

st.markdown("### 7. Checklist de Encerramento")
checklist = {
    "Planilha de fluxo enviada": st.checkbox("Planilha enviada"),
    "Simulação de maquininha": st.checkbox("Simulação enviada"),
    "QR/Pix liberado": st.checkbox("Pix/QR liberado"),
    "Proposta de crédito enviada": st.checkbox("Proposta enviada"),
    "Nova visita agendada": st.checkbox("Nova visita agendada")
}

# Exportar PDF (opcional)
if st.button("📄 Gerar Relatório da Visita (PDF)"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Roteiro de Visita - {cliente}", ln=True)
    pdf.cell(200, 10, txt=f"Data: {data_visita}", ln=True)
    pdf.ln(10)

    for sec in ["Abertura e Quebra de Gelo", "Diagnóstico do Negócio", "Recebimentos e Vendas",
                "Fluxo de Caixa e Controles", "Investimentos e Segurança", "Proposta de Valor"]:
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt=sec, ln=True)
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 8, txt=st.session_state.get(sec.lower().replace(" ", "_"), ""))
        pdf.ln(5)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Checklist", ln=True)
    pdf.set_font("Arial", size=10)
    for item, marcado in checklist.items():
        pdf.cell(200, 8, txt=f"[{'X' if marcado else ' '}] {item}", ln=True)

    file_path = "/mnt/data/visita_cliente.pdf"
    pdf.output(file_path)
    with open(file_path, "rb") as file:
        st.download_button("📥 Baixar PDF", file, file_name="visita_cliente.pdf")
