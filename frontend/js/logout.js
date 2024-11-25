function logout() {
    localStorage.removeItem('token'); // Remove o token
    alert('Você foi deslogado.');
    window.location.href = '/login'; // Redireciona para a página de login
}

// Exemplo: Vinculando a função a um botão
document.getElementById('logoutBtn').addEventListener('click', logout);