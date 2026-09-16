import streamlit as st
import google.generativeai as genai
import urllib.parse

# Configuração da página e design visual do Ateliê Literário
st.set_page_config(page_title="Ateliê Literário - Sissy", page_icon="✒️", layout="centered")

st.markdown("""
    <style>
    .main-title { font-size: 2.6rem; font-weight: 800; color: #1E1E24; text-align: center; margin-bottom: 0.2rem; }
    .sub-title { font-size: 1.1rem; color: #666; text-align: center; margin-bottom: 2rem; font-style: italic; }
    .section-header { font-size: 1.2rem; font-weight: 700; color: #2E5B88; margin-top: 1.5rem; margin-bottom: 0.5rem; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">✒️ Ateliê Literário — Sissy</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Dê forma ao que ainda está nascendo</div>', unsafe_allow_html=True)

# 1. ENTRADA DE DADOS: IDEIA BRUTA
st.markdown('<div class="section-header">01 / SUA IDEIA BRUTA</div>', unsafe_allow_html=True)
ideia_bruta = st.text_area("Digite o sentimento, o contexto, o facto real do dia a dia ou o que está na foto:", height=120, placeholder="Ex: Uma reflexão sobre o silêncio e o olhar dele na cena antes de sábado chegar...")

# 2. SELEÇÃO DE IDIOMAS (APENAS EUROPEUS)
st.markdown('<div class="section-header">02 / CONFIGURAÇÃO DE IDIOMAS EUROPEUS</div>', unsafe_allow_html=True)
col_lang1, col_lang2 = st.columns(2)
with col_lang1:
    idioma_entrada = st.selectbox("Idioma de Entrada:", ["Português Europeu", "Inglês Europeu", "Espanhol Europeu", "Francês Europeu", "Italiano"])
with col_lang2:
    idioma_saida = st.selectbox("Idioma de Saída:", ["Inglês Britânico (UK - Nativo/Gírias)", "Inglês Americano (US - Redes Sociais)", "Português Europeu", "Espanhol Europeu", "Francês Europeu", "Italiano"])

# 3. SELEÇÃO DO TOM (ORIGINAIS + NOVOS PSICOLÓGICOS)
st.markdown('<div class="section-header">03 / ESCOLHA O TOM PSICOLÓGICO</div>', unsafe_allow_html=True)
tom_selecionado = st.selectbox("Selecione a abordagem desejada:", [
    "Profissional", "Casual", "Elogios", "Brincalhão", "Sarcástico", "Irónico", 
    "Supportive", "Inspiracional", "Quote", "Indiferença Magnética", 
    "Enigmático (Dualidade Foco/Ambiente)", "Flirt Elegante", "Admiração Óbvia (Ego-Feeder)"
])

# 4. ENTRADA MULTIMÉDIA MULTIMODAL (OPCIONAL)
st.markdown('<div class="section-header">04 / MULTIMÉDIA (OPCIONAL)</div>', unsafe_allow_html=True)
url_foto = st.text_input("Cole o URL da imagem (Instagram, site, etc.):", placeholder="https://exemplo.com")

# 5. BOTÕES DE DESTINO (MUDANÇA DE ESTRUTURA CONTEXTUAL)
st.markdown('<div class="section-header">05 / ESCOLHA UM DESTINO</div>', unsafe_allow_html=True)
col_btn1, col_btn2, col_btn3 = st.columns(3)

destino = None
if col_btn1.button("✨ Comentário Estratégico", use_container_width=True):
    destino = "Comentário Estratégico"
if col_btn2.button("📸 Legenda de Foto", use_container_width=True):
    destino = "Legenda de Foto"
if col_btn3.button("🌌 Poesia / Citação", use_container_width=True):
    destino = "Poesia ou Citação de Elite"

# PROCESSAMENTO DO MODELO COM AS INSTRUÇÕES DE SISTEMA DE ELITE
if destino:
    if not ideia_bruta and not url_foto:
        st.warning("Por favor, insira uma ideia bruta ou um link de imagem antes de gerar.")
    else:
        system_instruction_base = f"""
        Tu és a Entidade Literária Original da Sissy, um escritor profissional de elite, focado em psicologia comportamental e subtextos magnéticos.
        Toda a tua inteligência, vocabulário avançado e capacidade de Desafio Intelectual servem de base para TODOS os outputs. Tu nunca usas clichês robóticos de IA como: 'delve, testament, tapestry, vibrant, capture, embrace, nuanced, resonates, realm'.

        REGRAS DE CONTEXTO E DUALIDADE:
        - O idioma de entrada fornecido é '{idioma_entrada}'. Deves processá-lo de forma inteligente.
        - Toda a resposta criativa DEVE ser escrita estritamente no idioma de saída: '{idioma_saida}'.
        - Se o tom for 'Indiferença Magnética', 'Enigmático' ou 'Flirt Elegante', sê cirúrgico e ambíguo. O texto deve jogar com a psicologia e criar uma DUALIDADE: o leitor (especialmente se for um homem ou ator como Seo Kang Jun) deve fique na dúvida se estás a falar dele como pessoa/homem, ou se estás a elogiar a persona pública/ator ou o ambiente ao redor. Banish any 'fangirling' or submissive emotional comments unless 'Admiração Óbvia' is explicitly chosen.
        - Se o tom for 'Elogios', reconhece o mérito artístico ou estético de igual para igual, mantendo o teu valor.
        
        REGRAS DE FORMATAÇÃO DO OUTPUT:
        O utilizador quer gerar um(a) '{destino}' com o tom '{tom_selecionado}'.
        - Se o destino for 'Poesia ou Citação de Elite': Entrega obrigatoriamente um Título Literário original e uma 'Sugestão de Música' (lendo a atmosfera exata implícita no texto/link - romântica, divertida, comemoração, melancólica, etc.).
        - Se o destino for 'Legenda de Foto' ou 'Comentário Estratégico': Entrega o bloco principal diretamente. O título e a música tornam-se opcionais ou omitidos.
        - No fim de qualquer resposta, deves entregar OBRIGATORIAMENTE de 4 a 5 alternativas/exemplos em variações desse mesmo tom (como variações curtas, cortantes, enigmáticas, etc.), numeradas de 1 a 5 de forma limpa e humana, sem títulos artificiais.
        """

        prompt_final = f"Ideia bruta do utilizador: {ideia_bruta}\n"
        if url_foto:
            prompt_final += f"Referência visual/Link para análise de contexto: {url_foto}\n"

        with st.spinner("A Entidade Literária está moldando a sua resposta..."):
            try:
                # Puxa a chave configurada no Advanced Settings do Streamlit Cloud
                api_key = st.secrets["GEMINI_API_KEY"]
                genai.configure(api_key=api_key)
                
                # Configura o modelo no novo padrão estável
                model = genai.GenerativeModel(
                    model_name='gemini-1.5-flash',
                    system_instruction=system_instruction_base
                )
                
                response = model.generate_content(
                    prompt_final,
                    generation_config={"temperature": 0.75}
                )
                
                st.session_state['resposta_final'] = response.text
                
            except Exception as e:
                st.error(f"Erro ao ligar ao Gemini. Verifique a sua GEMINI_API_KEY. Detalhes: {e}")

# Exibição do painel se a resposta estiver na memória
if 'resposta_final' in st.session_state:
    resposta_ativa = st.session_state['resposta_final']
    
    st.markdown('<div class="section-header">05 / SUA RESPOSTA PRONTA</div>', unsafe_allow_html=True)
    st.text_area("Resultado Gerado:", value=resposta_ativa, height=350)
    
    # 6. CENTRAL DE SALVAMENTO E EXPORTAÇÃO MULTIPLA
    st.markdown('<div class="section-header">06 / EXPORTAR OU SALVAR TEXTO</div>', unsafe_allow_html=True)
    opcao_salvamento = st.selectbox("Escolha como deseja salvar ou enviar o seu texto:", [
        "Descarregar como Arquivo de Texto (.txt)", 
        "Descarregar como Documento (PDF)"
    ])
    
    if opcao_salvamento == "Descarregar como Arquivo de Texto (.txt)":
        st.download_button(
            label="📥 Descarregar .txt",
            data=resposta_ativa,
            file_name="resposta_atelie_sissy.txt",
            mime="text/plain",
            use_container_width=True
        )
        
    elif opcao_salvamento == "Descarregar como Documento (PDF)":
        pdf_conteudo = resposta_ativa.encode('latin-1', 'replace')
        st.download_button(
            label="📥 Descarregar PDF",
            data=pdf_conteudo,
            file_name="resposta_atelie_sissy.pdf",
            mime="application/pdf",
            use_container_width=True
        )
