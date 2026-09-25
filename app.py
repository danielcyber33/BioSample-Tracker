import sqlite3


def cadastrar_amostra():
    print("\n=== CADASTRAR NOVA AMOSTRA ===")

    sample_id = input("ID da amostra: ")
    organism = input("Organismo/espécie: ")
    sample_type = input("Tipo de amostra: ")
    experiment = input("Experimento: ")
    storage = input("Condição de armazenamento: ")
    status = input("Status da amostra: ")

    connection = sqlite3.connect("biosamples.db")
    cursor = connection.cursor()

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

    print("\nAmostra cadastrada com sucesso!")


def listar_amostras():
    print("\n=== AMOSTRAS CADASTRADAS ===")

    connection = sqlite3.connect("biosamples.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM samples")
    samples = cursor.fetchall()

    connection.close()

    for sample in samples:
        print(sample)

def buscar_amostra():
    print("\n=== BUSCAR AMOSTRA ===")

    sample_id = input("Digite o ID da amostra: ")

    connection = sqlite3.connect("biosamples.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM samples WHERE sample_id = ?",
        (sample_id,)
    )

    sample = cursor.fetchone()

    connection.close()

    if sample:
        print("\n=== AMOSTRA ENCONTRADA ===")
        print("ID interno:", sample[0])
        print("ID da amostra:", sample[1])
        print("Organismo:", sample[2])
        print("Tipo:", sample[3])
        print("Experimento:", sample[4])
        print("Armazenamento:", sample[5])
        print("Status:", sample[6])

    else:
        print("\nAmostra não encontrada.")

def atualizar_amostra():
    print("\n=== ATUALIZAR AMOSTRA ===")

    sample_id = input("Digite o ID da amostra: ")

    connection = sqlite3.connect("biosamples.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM samples WHERE sample_id = ?",
        (sample_id,)
    )

    sample = cursor.fetchone()

    if not sample:
        print("\nAmostra não encontrada.")
        connection.close()
        return

    print("\nAmostra encontrada.")
    print("Pressione ENTER para manter o valor atual.\n")

    organism = input(f"Organismo [{sample[2]}]: ")
    sample_type = input(f"Tipo [{sample[3]}]: ")
    experiment = input(f"Experimento [{sample[4]}]: ")
    storage = input(f"Armazenamento [{sample[5]}]: ")
    status = input(f"Status [{sample[6]}]: ")

    if organism == "":
        organism = sample[2]

    if sample_type == "":
        sample_type = sample[3]

    if experiment == "":
        experiment = sample[4]

    if storage == "":
        storage = sample[5]

    if status == "":
        status = sample[6]

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
        sample_id
    ))

    connection.commit()
    connection.close()

    print("\nAmostra atualizada com sucesso!")

def excluir_amostra():
    print("\n=== EXCLUIR AMOSTRA ===")

    sample_id = input("Digite o ID da amostra: ")

    connection = sqlite3.connect("biosamples.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM samples WHERE sample_id = ?",
        (sample_id,)
    )

    sample = cursor.fetchone()

    if not sample:
        print("\nAmostra não encontrada.")
        connection.close()
        return

    print("\n=== AMOSTRA ENCONTRADA ===")
    print("ID da amostra:", sample[1])
    print("Organismo:", sample[2])
    print("Tipo:", sample[3])
    print("Experimento:", sample[4])
    print("Armazenamento:", sample[5])
    print("Status:", sample[6])

    confirmacao = input(
        "\nTem certeza que deseja excluir esta amostra? (s/n): "
    )

    if confirmacao.lower() == "s":

        cursor.execute(
            "DELETE FROM samples WHERE sample_id = ?",
            (sample_id,)
        )

        connection.commit()

        print("\nAmostra excluída com sucesso!")

    else:
        print("\nExclusão cancelada.")

    connection.close()

while True:

    print("\n========== BioSample Tracker ==========")
    print("1 - Cadastrar nova amostra")
    print("2 - Listar amostras")
    print("3 - Buscar amostra")
    print("4 - Atualizar amostra")
    print("5 - Excluir amostra")
    print("0 - Sair")

    opcao = input("\nEscolha uma opção: ")

    if opcao == "1":
        cadastrar_amostra()
        
    elif opcao == "2":
        listar_amostras()

    elif opcao == "3":
        buscar_amostra()

    elif opcao == "4":
        atualizar_amostra()

    elif opcao == "5":
        excluir_amostra()

    elif opcao == "0":
        print("\nEncerrando BioSample Tracker...")
        break

    else:
        print("\nOpção inválida.")