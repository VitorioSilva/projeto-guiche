const clients = [
    { nome: "Ana Souza de Oliveira", idade: 65, prioridade: true },
    { nome: "Carlos Pereira da Cruz", idade: 34, prioridade: false },
    { nome: "Joana Silva do Nascimento", idade: 28, prioridade: true },
    { nome: "José Ferreira Cruz", idade: 75, prioridade: true },
];

function displayClients() {
    const clientList = document.getElementById("client-list");
    clientList.innerHTML = "";
    const sortedClients = clients.sort((a, b) => b.prioridade - a.prioridade);
    sortedClients.forEach((client, index) => {
        const clientItem = document.createElement("div");
        clientItem.classList.add("client-item");
        if (client.prioridade) {
            clientItem.classList.add("priority");
        }
        clientItem.innerHTML = `
            <p><strong>${index + 1}. Nome:</strong> ${client.nome}</p>
            <p><strong>Idade:</strong> ${client.idade}</p>
            <p><strong>Prioridade:</strong> ${client.prioridade ? "Sim" : "Não"}</p>
        `;
        clientList.appendChild(clientItem);
    });
}

function adicionarCliente() {
    const nome = prompt("Nome do cliente:");
    const idade = prompt("Idade do cliente:");
    const prioridade = confirm("O cliente se encaixa no padrão de prioridade? (+60 anos, gestante ou deficiente)");
    if (nome && idade) {
        clients.push({ nome, idade: parseInt(idade), prioridade });
        displayClients();
    }
}

displayClients();