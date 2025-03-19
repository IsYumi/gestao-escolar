document.addEventListener("DOMContentLoaded", function () {
    const tbody = document.querySelector('#tabelaLista tbody');
    turmas.forEach(value => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${value.id}</td>
            <td>${value.descricao}</td>
            <td>${value.professor_id}</td>
            <td>${value.ativo}</td>
            <td><input type="button" value="Atualizar" onclick="atualizarTurma(${value.id})"></td> 
            <td><input type="button" value="Deletar" onclick="deletarTurma(${value.id})"></td> 
        `;
        tbody.appendChild(tr);
    });
});


function adicionarTurma() {
    let id = prompt("Digite o valor ID ou apenas aperte OK para pular a etapa.", "");
    if (turmas.some(turma => turma.id == id) || isNaN(id)) {
        alert("Este ID está inválido. Por favor, forneça um ID único.");
        return;
    }

    // Garantindo que o ID seja numérico
    id = parseInt(id, 10);

    let descricao = prompt("Digite a DESCRIÇÃO da turma ou apenas aperte OK para pular a etapa.", "");
    if (!descricao) {
        alert("Algum dado não foi fornecido.");
        return;
    }

    let professor = prompt("Digite o nome do PROFESSOR da turma ou apenas aperte OK para pular a etapa.", "");
    if (!professor) {
        alert("Algum dado não foi fornecido.");
        return;
    }

    let status = prompt("Digite o STATUS da turma (ex: true, false):", "");
    if (!status) {
        alert("Algum dado não foi fornecido.");
        return;
    }

    let novaTurma = {
        id: id,
        descricao: descricao,
        professor_id: professor,
        ativo: status
    };

    fetch("/turmas", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(novaTurma)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Erro ao adicionar turma.");
        }
        return response.json();
    })
    .then(data => {
        turmas.push(data); // Adiciona a nova turma à lista local
        atualizarTabelaTurmas(); // Atualiza a tabela localmente
        alert("Turma adicionada com sucesso!");
    })
    .catch(error => {
        console.error("Erro:", error);
        alert("Ocorreu um erro ao adicionar a turma.");
    });
}

function atualizarTurma(id) {
    let turma = turmas.find(value => value.id == id);
    let descricao = prompt("Digite a nova DESCRIÇÃO ou apenas aperte OK para pular a etapa.", turma.descricao);
    let professor = prompt("Digite a novo PROFESSOR ID apenas aperte OK para pular a etapa.", turma.professor_id);
    let status = prompt("Digite a nova STATUS ou apenas aperte OK para pular a etapa.", turma.status);

    let dadosAtualizados = {id : turma.id};
    if (descricao && descricao !== turma.descricao) dadosAtualizados.descricao = descricao;
    if (professor && professor !== turma.professor) dadosAtualizados.professor_id = professor;
    if (status && status !== turma.status) dadosAtualizados.ativo = status;

    // Se nenhum dado foi alterado, não faz nada
    if (Object.keys(dadosAtualizados).length === 1) {
        alert("Nenhuma alteração feita.");
        return;
    }

    // Envia a atualização para o backend via requisição PUT
    fetch(`/turmas/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(dadosAtualizados)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Erro ao atualizar turma.");
        }
        return response.json();
    })
    .then(data => {
        // Atualiza os dados na lista local
        Object.assign(turma, dadosAtualizados);
        atualizarTabelaTurmas();  // Atualiza a tabela
        alert("Turma atualizada com sucesso!");
    })
    .catch(error => {
        console.error("Erro:", error);
        alert("Erro ao atualizar turma.");
    });
}

function atualizarTabelaTurmas() {
    const tbody = document.querySelector("#tabelaLista tbody");
    tbody.innerHTML = ""; // Limpa a tabela

    turmas.forEach(value => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
           <td>${value.id}</td>
            <td>${value.descricao}</td>
            <td>${value.professor_id}</td>
            <td>${value.ativo}</td>
            <td><input type="button" value="Atualizar" onclick="atualizarTurma(${value.id})"></td> 
            <td><input type="button" value="Deletar" onclick="deletarTurma(${value.id})"></td> 
        `;
        tbody.appendChild(tr);
    });
    
}

function deletarTurma(id) {
    if (!confirm("Tem certeza que deseja deletar este Turma?")) return;

    fetch(`/turmas/${id}`, {
        method: "DELETE",
        headers: { "Content-Type": "application/json" }
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => {
                throw new Error(text || "Erro ao deletar turma!");
            });
        }
        return response.json();
    })
    .then(() => {
        turmas = turmas.filter(turma => turma.id !== id);
        atualizarTabelaTurmas();
        alert("Turma deletado com sucesso!");
    })
    .catch(error => {
        window.location.reload();
    });
}