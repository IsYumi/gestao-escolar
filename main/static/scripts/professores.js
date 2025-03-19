document.addEventListener("DOMContentLoaded", function () {
    const tbody = document.querySelector('#tabelaLista tbody');
    professores.forEach(value => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${value.id}</td>
            <td>${value.nome}</td>
            <td>${value.data_nascimento}</td>
            <td>${value.disciplina}</td>
            <td>${value.salario}</td>
            <td><input type="button" value="Atualizar" onclick="atualizarProfessor(${value.id})"></td> 
            <td><input type="button" value="Deletar" onclick="deletarProfessor(${value.id})"></td> 
        `;
        tbody.appendChild(tr);
    });
});

function adicionarProfessor() {
    let id = prompt("Digite o valor ID ou apenas aperte OK para pular a etapa", "");
    if (professores.some(professor => professor.id == id)) {
        alert("Este ID já está em uso. Por favor, forneça um ID único.");
        return;
    }
 
    // Garanta que o ID seja numérico
    id = parseInt(id, 10);
 
    let nome = prompt("Digite o valor NOME ou apenas aperte OK para pular a etapa", "");
    let data_nascimento = prompt("Digite o valor DATA DE NASCIMENTO ou apenas aperte OK para pular a etapa", "");
    let disciplina = prompt("Digite o valor DISCIPLINA ou apenas aperte OK para pular a etapa", "");
    let salario = prompt("Digite o valor SALARIO ou apenas aperte OK para pular a etapa", "");
 
    if (!nome || !data_nascimento || !disciplina || !salario) {
        alert("Algum dado não foi fornecido.");
        return;
    }
    
    let novosDados = {
        id: id,
        nome: nome,
        data_nascimento: data_nascimento,
        disciplina: disciplina,
        salario: salario
    };
 
    fetch("/professores", {
        method: "POST",  
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(novosDados)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Erro ao adicionar professor.");
        }
        return response.json();
    })
    .then(data => {
        professores.push(data); // Adiciona o novo professor à lista local
        atualizarTabela(); // Atualiza a tabela localmente
        alert("Professor adicionado com sucesso!");
 
        // Agora fazemos uma nova requisição GET para obter a lista atualizada de professores
        fetch("/professores")
            .then(response => response.json())
            .then(data => {
                professores = data; // Atualiza a lista de professores com os dados mais recentes
                atualizarTabela(); // Atualiza a tabela com a nova lista
            })
            .catch(error => {
                console.error("Erro ao carregar os professores:", error);
            });
    })
    .catch(error => {
        console.error("Erro:", error);
        alert("Ocorreu um erro ao adicionar o(a) professor(a).");
    });
 }

 function atualizarProfessor(id) {
    let professor = professores.find(value => value.id == id);
    let nome = prompt("Digite o novo NOME ou apenas aperte OK para pular a etapa", professor.nome);
    let data_nascimento = prompt("Digite a nova DATA DE NASCIMENTO ou apenas aperte OK para pular a etapa", professor.data_nascimento);
    let disciplina = prompt("Digite a nova DISCIPLINA ou apenas aperte OK para pular a etapa", professor.disciplina);
    let salario = prompt("Digite o novo SALARIO ou apenas aperte OK para pular a etapa", professor.salario);
    
    let dadosAtualizados = {id : professor.id};
    if (nome && nome !== professor.nome) dadosAtualizados.nome = nome;
    if (data_nascimento && data_nascimento !== professor.data_nascimento) dadosAtualizados.data_nascimento = data_nascimento;
    if (disciplina && disciplina !== professor.disciplina) dadosAtualizados.disciplina = disciplina;
    if (salario && salario !== professor.salario) dadosAtualizados.salario = salario;

    // Se nenhum dado foi alterado, não faz nada
    if (Object.keys(dadosAtualizados).length === 0) {
        alert("Nenhuma alteração feita.");
        return;
    }

    // Envia a atualização para o backend via requisição PUT
    fetch(`/professores/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(dadosAtualizados)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Erro ao atualizar professor.");
        }
        return response.json();
    })
    .then(data => {
        // Atualiza os dados na lista local
        Object.assign(professor, dadosAtualizados);
        atualizarTabela();  // Atualiza a tabela
        alert("Professor(a) atualizado com sucesso!");
    })
    .catch(error => {
        console.error("Erro:", error);
        alert("Erro ao atualizar professor(a).");
    });
}

function deletarProfessor(id) {
    if (!confirm("Tem certeza que deseja deletar este(a) professor(a)?")) return;

    fetch(`/professores/${id}`, {
        method: "DELETE",
        headers: { "Content-Type": "application/json" }
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => {
                throw new Error(text || "Erro ao deletar professor(a).");
            });
        }
        return response.json();
    })
    .then(() => {
        professores = professores.filter(professor => professor.id !== id);
        atualizarTabela();
        alert("Professor(a) deletado com sucesso!");
    })
    .catch(error => {
        window.location.reload();
    });
}

function atualizarTabela() {
    const tbody = document.querySelector("#tabelaLista tbody");
    tbody.innerHTML = ""; // Limpa a tabela

    professores.forEach(value => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${value.id}</td>
            <td>${value.nome}</td>
            <td>${value.data_nascimento || 'N/A'}</td>
            <td>${value.disciplina || 'N/A'}</td>
            <td>${value.salario || 'N/A'}</td>
            <td><input type="button" value="Atualizar" onclick="atualizarProfessor(${value.id})"></td> 
            <td><input type="button" value="Deletar" onclick="deletarProfessor(${value.id})"></td> 
        `;
        tbody.appendChild(tr);
    });
}