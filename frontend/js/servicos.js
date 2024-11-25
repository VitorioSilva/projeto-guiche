// Função para buscar serviços protegidos
function carregarServicos() {
    const token = localStorage.getItem('token'); // Pega o token salvo

    fetch('/servicos', {
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ${token}', // Inclui o token no cabeçalho
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.status === 401) {
            alert('Token inválido ou expirado. Faça login novamente.');
            window.location.href = '/login';
        } else if (!response.ok) {
            throw new Error('Erro ao carregar serviços.');
        }
        return response.json();
    })
    .then(data => {
        console.log(data); // Exibe os serviços no console
        // Renderize os serviços na página (ajuste conforme necessário)
        const listaServicos = document.getElementById('listaServicos');
        listaServicos.innerHTML = data.map(servico => <li>${servico.nome}</li>).join('');
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao carregar serviços.');
    });
}

// Carrega os serviços ao abrir a página
document.addEventListener('DOMContentLoaded', carregarServicos);