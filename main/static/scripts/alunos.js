document.addEventListener("DOMContentLoaded", function () {
    const tbody = document.querySelector('#tabelaLista tbody');
    alunos.forEach(value => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${value.id}</td>
            <td>${value.nome}</td>
            <td>${value.idade}</td>
            <td>${value.data_nascimento}</td>
            <td>${value.nota1}</td>
            <td>${value.nota2}</td>
            <td>${value.media}</td> <!-- Exibindo a média -->
            <td><input type="button" value="Atualizar" onclick="atualizarAluno(${value.id})"></td>
            <td><input type="button" value="Deletar" onclick="deletarAluno(${value.id})"></td>
        `;
        tbody.appendChild(tr);
    });
});

// Função para calcular a média aritmética
function calcularMedia(nota1, nota2) {
    return ((parseFloat(nota1) + parseFloat(nota2)) / 2).toFixed(2); // Média com duas casas decimais
}

function adicionarAluno() {
    let id = prompt("Digite o valor ID ou apenas aperte OK para pular a etapa.", "");
    if (alunos.some(aluno => aluno.id == id) || isNaN(id)) {
        alert("Este ID está inválido. Por favor, forneça um ID único.");
        return;
    }

    // Garantindo que o ID seja numérico
    id = parseInt(id, 10);

    let nome = prompt("Digite o NOME ou apenas aperte OK para pular a etapa.", "");
    if (!nome) {
        alert("Algum dado não foi fornecido.");
        return;
    }

    let dataNascimento = prompt("Digite a DATA DE NASCIMENTO ou apenas aperte OK para pular a etapa.", "");
    if (!dataNascimento) {
        alert("Algum dado não foi fornecido.");
        return;
    }

    let nota1 = prompt("Insira a Nota do 1º Semestre.", "");
    if (isNaN(nota1) || nota1 === "") {
        alert("Nota 1º Semestre inválida.");
        return;
    }

    let nota2 = prompt("Insira a Nota do 2º Semestre.", "");
    if (isNaN(nota2) || nota2 === "") {
        alert("Nota 2º Semestre inválida.");
        return;
    }

    // Calculando a média final
    let media = calcularMedia(nota1, nota2);

    // Criando o novo aluno com as notas e a média calculada
    let novosDados = {
        id: id,
        nome: nome,
        data_nascimento: dataNascimento,
        nota1: parseFloat(nota1),
        nota2: parseFloat(nota2),
        media: media // Média calculada aqui
    };

    fetch("/alunos", {
        method: "POST",  
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(novosDados)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Erro ao adicionar aluno.");
        }
        return response.json();
    })
    .then(data => {
        alunos.push(data); // Adiciona o novo aluno à lista local
        atualizarTabela(); // Atualiza a tabela localmente
        alert("Aluno(a) adicionado com sucesso!");
    })
    .catch(error => {
        console.error("Erro:", error);
        alert("Ocorreu um erro ao adicionar o(a) aluno(a).");
    });
}

function atualizarAluno(id) {
    let aluno = alunos.find(value => value.id == id);
    let nome = prompt("Digite o novo NOME ou apenas aperte OK para pular a etapa.", aluno.nome);
    let idade = prompt("Digite a nova IDADE apenas aperte OK para pular a etapa.", aluno.idade);
    let dataNascimento = prompt("Digite a nova DATA DE NASCIMENTO ou apenas aperte OK para pular a etapa.", aluno.data_nascimento);
    let nota1 = prompt("Digite a nova Nota do 1º Semestre.", aluno.nota1);
    let nota2 = prompt("Digite a nova Nota do 2º Semestre.", aluno.nota2);

    if (isNaN(nota1) || isNaN(nota2)) {
        alert("Notas inválidas.");
        return;
    }

    // Calculando a média final novamente
    let media = calcularMedia(nota1, nota2);

    let dadosAtualizados = {id : aluno.id};

    if (nome && nome !== aluno.nome) dadosAtualizados.nome = nome;
    if (idade && idade !== aluno.idade) dadosAtualizados.idade = idade;
    if (dataNascimento && dataNascimento !== aluno.data_nascimento) dadosAtualizados.data_nascimento = dataNascimento;
    if (nota1 && parseFloat(nota1) !== aluno.nota1) dadosAtualizados.nota1 = parseFloat(nota1);
    if (nota2 && parseFloat(nota2) !== aluno.nota2) dadosAtualizados.nota2 = parseFloat(nota2);

    // Atualiza a média final
    dadosAtualizados.media = media;

    // Se nenhum dado foi alterado, não faz nada
    if (Object.keys(dadosAtualizados).length === 1) {
        alert("Nenhuma alteração feita.");
        return;
    }

    // Envia a atualização para o backend via requisição PUT
    fetch(`/alunos/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(dadosAtualizados)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Erro ao atualizar aluno.");
        }
        return response.json();
    })
    .then(data => {
        // Atualiza os dados na lista local
        Object.assign(aluno, dadosAtualizados);
        atualizarTabela();  // Atualiza a tabela
        alert("Aluno atualizado com sucesso!");
    })
    .catch(error => {
        console.error("Erro:", error);
        alert("Erro ao atualizar aluno.");
    });
}

function atualizarTabela() {
    const tbody = document.querySelector("#tabelaLista tbody");
    tbody.innerHTML = ""; // Limpa a tabela

    alunos.forEach(value => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${value.id}</td>
            <td>${value.nome}</td>
            <td>${value.idade}</td>
            <td>${value.data_nascimento}</td>
            <td>${value.nota1}</td>
            <td>${value.nota2}</td>
            <td>${value.media}</td> <!-- Exibindo a média -->
            <td><input type="button" value="Atualizar" onclick="atualizarAluno(${value.id})"></td>
            <td><input type="button" value="Deletar" onclick="deletarAluno(${value.id})"></td>
        `;
        tbody.appendChild(tr);
    });
    
}


function deletarAluno(id) {
    if (!confirm("Tem certeza que deseja deletar este aluno(a)?")) return;

    fetch(`/alunos/${id}`, {
        method: "DELETE",
        headers: { "Content-Type": "application/json" }
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => {
                throw new Error(text || "Erro ao deletar aluno(a)!");
            });
        }
        return response.json();
    })
    .then(() => {
        alunos = alunos.filter(aluno => aluno.id !== id);
        atualizarTabela();
        alert("Aluno(a) deletado com sucesso!");
    })
    .catch(error => {
        window.location.reload();
    });
}