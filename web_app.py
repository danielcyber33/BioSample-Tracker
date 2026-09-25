import streamlit as st
import sqlite3
import pandas as pd


# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================

st.set_page_config(
    page_title="BioSample Tracker",
    page_icon="🧬",
    layout="wide"
)


# ==========================================
# FUNÇÃO PARA CARREGAR AS AMOSTRAS
# ==========================================

def carregar_amostras():

    connection = sqlite3.connect("biosamples.db")

    query = """
    SELECT
        id,
        sample_id,
        organism,
        sample_type,
        experiment,
        storage,
        status
    FROM samples
    """

    df = pd.read_sql_query(query, connection)

    connection.close()

    return df


# ==========================================
# MENU LATERAL
# ==========================================

st.sidebar.title("🧬 BioSample Tracker")

pagina = st.sidebar.radio(
    "Navegação",
    [
        "📊 Dashboard",
        "➕ Cadastrar amostra",
        "🧪 Amostras",
        "⚙️ Gerenciar"
    ]
)


# ==========================================
# DASHBOARD
# ==========================================

if pagina == "📊 Dashboard":

    st.title("📊 Dashboard")

    st.write(
        "Visão geral das amostras cadastradas no BioSample Tracker."
    )

    df = carregar_amostras()

    total_amostras = len(df)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total de amostras",
        total_amostras
    )

    col2.metric(
        "Organismos",
        df["organism"].nunique()
    )

    col3.metric(
        "Status diferentes",
        df["status"].nunique()
    )

    st.divider()

    st.subheader("🧪 Amostras recentes")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


# ==========================================
# CADASTRAR
# ==========================================

elif pagina == "➕ Cadastrar amostra":

    st.title("➕ Cadastrar nova amostra")

    st.write(
        "Preencha os dados abaixo para registrar uma nova amostra biológica."
    )

    with st.form("form_cadastro"):

        sample_id = st.text_input(
            "ID da amostra",
            placeholder="Ex.: BIO004"
        )

        organism = st.text_input(
            "Organismo / espécie",
            placeholder="Ex.: Chlorella vulgaris"
        )

        sample_type = st.selectbox(
            "Tipo de amostra",
            [
                "Biomassa",
                "DNA",
                "RNA",
                "Proteína",
                "Extrato",
                "Tecido",
                "Células",
                "Outro"
            ]
        )

        experiment = st.text_input(
            "Experimento",
            placeholder="Ex.: Extração de lipídios"
        )

        storage = st.text_input(
            "Condição de armazenamento",
            placeholder="Ex.: -20 °C"
        )

        status = st.selectbox(
            "Status",
            [
                "Disponível",
                "Em análise",
                "Em processamento",
                "Utilizada",
                "Descartada"
            ]
        )

        cadastrar = st.form_submit_button(
            "🧬 Cadastrar amostra"
        )

    if cadastrar:

        sample_id = sample_id.strip()
        organism = organism.strip()

        if sample_id == "" or organism == "":

            st.error(
                "ID da amostra e organismo são campos obrigatórios."
            )

        else:

            connection = sqlite3.connect("biosamples.db")
            cursor = connection.cursor()

            # Verifica se o código já existe
            cursor.execute(
                "SELECT sample_id FROM samples WHERE sample_id = ?",
                (sample_id,)
            )

            amostra_existente = cursor.fetchone()

            if amostra_existente:

                st.error(
                    f"Já existe uma amostra cadastrada com o ID {sample_id}."
                )

                connection.close()

            else:

                cursor.execute("""
                    INSERT INTO samples (
                        sample_id,
                        organism,
                        sample_type,
                        experiment,
                        storage,
                        status
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    sample_id,
                    organism,
                    sample_type,
                    experiment,
                    storage,
                    status
                ))

                connection.commit()
                connection.close()

                st.success(
                    f"Amostra {sample_id} cadastrada com sucesso!"
                )


# ==========================================
# AMOSTRAS
# ==========================================

elif pagina == "🧪 Amostras":

    st.title("🧪 Amostras cadastradas")

    st.write(
        "Consulte e filtre as amostras registradas no sistema."
    )

    df = carregar_amostras()

    # ------------------------------
    # CAMPO DE BUSCA
    # ------------------------------

    busca = st.text_input(
        "🔎 Buscar amostra",
        placeholder="Digite o ID ou o nome do organismo"
    )

    # ------------------------------
    # FILTROS
    # ------------------------------

    col1, col2 = st.columns(2)

    tipos = ["Todos"] + sorted(
        df["sample_type"].dropna().unique().tolist()
    )

    status_opcoes = ["Todos"] + sorted(
        df["status"].dropna().unique().tolist()
    )

    with col1:
        filtro_tipo = st.selectbox(
            "Tipo de amostra",
            tipos
        )

    with col2:
        filtro_status = st.selectbox(
            "Status",
            status_opcoes
        )

    # Criamos uma cópia para aplicar os filtros
    df_filtrado = df.copy()

    # Busca por ID ou organismo
    if busca:

        busca = busca.strip()

        df_filtrado = df_filtrado[
            df_filtrado["sample_id"].str.contains(
                busca,
                case=False,
                na=False
            )
            |
            df_filtrado["organism"].str.contains(
                busca,
                case=False,
                na=False
            )
        ]

    # Filtro por tipo
    if filtro_tipo != "Todos":

        df_filtrado = df_filtrado[
            df_filtrado["sample_type"] == filtro_tipo
        ]

    # Filtro por status
    if filtro_status != "Todos":

        df_filtrado = df_filtrado[
            df_filtrado["status"] == filtro_status
        ]

    st.divider()

    st.write(
        f"**{len(df_filtrado)} amostra(s) encontrada(s)**"
    )

    st.dataframe(
        df_filtrado,
        use_container_width=True,
        hide_index=True
    )


# ==========================================
# GERENCIAR
# ==========================================

elif pagina == "⚙️ Gerenciar":

    st.title("⚙️ Gerenciar amostras")

    st.write(
        "Selecione uma amostra para visualizar ou editar suas informações."
    )

    df = carregar_amostras()

    if df.empty:

        st.warning("Nenhuma amostra cadastrada.")

    else:

        # Lista de IDs disponíveis
        ids_amostras = df["sample_id"].tolist()

        sample_id_selecionado = st.selectbox(
            "Selecione a amostra",
            ids_amostras
        )

        # Recupera a amostra selecionada
        sample = df[
            df["sample_id"] == sample_id_selecionado
        ].iloc[0]

        st.divider()

        st.subheader(
            f"🧬 Editar {sample_id_selecionado}"
        )

        with st.form("form_edicao"):

            organism = st.text_input(
                "Organismo / espécie",
                value=sample["organism"]
            )

            tipos_amostra = [
                "Biomassa",
                "DNA",
                "RNA",
                "Proteína",
                "Extrato",
                "Tecido",
                "Células",
                "Outro"
            ]

            # Descobre a posição atual do tipo
            if sample["sample_type"] in tipos_amostra:
                indice_tipo = tipos_amostra.index(
                    sample["sample_type"]
                )
            else:
                indice_tipo = 0

            sample_type = st.selectbox(
                "Tipo de amostra",
                tipos_amostra,
                index=indice_tipo
            )

            experiment = st.text_input(
                "Experimento",
                value=sample["experiment"]
            )

            storage = st.text_input(
                "Condição de armazenamento",
                value=sample["storage"]
            )

            status_opcoes = [
                "Disponível",
                "Em análise",
                "Em processamento",
                "Utilizada",
                "Descartada"
            ]

            if sample["status"] in status_opcoes:
                indice_status = status_opcoes.index(
                    sample["status"]
                )
            else:
                indice_status = 0

            status = st.selectbox(
                "Status",
                status_opcoes,
                index=indice_status
            )

            atualizar = st.form_submit_button(
                "💾 Salvar alterações"
            )

        if atualizar:

            organism = organism.strip()

            if organism == "":

                st.error(
                    "O organismo/espécie não pode ficar vazio."
                )

            else:

                connection = sqlite3.connect(
                    "biosamples.db"
                )

                cursor = connection.cursor()

                cursor.execute("""
                    UPDATE samples
                    SET organism = ?,
                        sample_type = ?,
                        experiment = ?,
                        storage = ?,
                        status = ?
                    WHERE sample_id = ?
                """, (
                    organism,
                    sample_type,
                    experiment,
                    storage,
                    status,
                    sample_id_selecionado
                ))

                connection.commit()
                connection.close()

                st.success(
                    f"Amostra {sample_id_selecionado} "
                    "atualizada com sucesso!"
                )

                st.rerun()

        st.divider()

        st.subheader("🗑️ Excluir amostra")

        st.warning(
            "A exclusão é permanente e removerá a amostra do banco de dados."
        )

        confirmar_exclusao = st.checkbox(
            f"Confirmo que desejo excluir a amostra "
            f"{sample_id_selecionado}"
        )

        excluir = st.button(
            "🗑️ Excluir amostra",
            type="primary",
            disabled=not confirmar_exclusao
        )

        if excluir:

            connection = sqlite3.connect(
                "biosamples.db"
            )

            cursor = connection.cursor()

            cursor.execute(
                "DELETE FROM samples WHERE sample_id = ?",
                (sample_id_selecionado,)
            )

            connection.commit()
            connection.close()

            st.success(
                f"Amostra {sample_id_selecionado} "
                "excluída com sucesso!"
            )

            st.rerun()