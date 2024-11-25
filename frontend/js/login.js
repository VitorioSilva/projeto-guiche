// Função para realizar o login e salvar o token
function login(email, senha) {
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, senha }) // Envia os dados do login
    })
    .then(response => response.json())
    .then(data => {
        if (data.token) {
            // Salva o token no localStorage
            localStorage.setItem('token', data.token); 
            alert('Login bem-sucedido!');
            // Redireciona para a página de serviços após o login
            window.location.href = '/servicos'; // Aqui ocorre o redirecionamento
        } else {
            alert(data.msg || 'Erro no login');
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao conectar ao servidor.');
    });
}

// Exemplo: Chamando a função quando o formulário de login é enviado
document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault(); // Evita o reload da página
    const email = document.getElementById('email').value;
    const senha = document.getElementById('senha').value;
    login(email, senha);
});