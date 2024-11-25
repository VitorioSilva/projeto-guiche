// Função para salvar dados no cookie
function setCookie(name, value, days) {
    const date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    const expires = `expires=${date.toUTCString()}`;
    document.cookie = `${name}=${value}; ${expires}; path=/`;
}

// Função para recuperar dados do cookie
function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith(`${name}=`)) {
            return cookie.substring(name.length + 1);
        }
    }
    return null;
}

// Função para deletar um cookie
function deleteCookie(name) {
    document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
}

document.addEventListener("DOMContentLoaded", () => {
    const generateButton = document.getElementById("generateButton");
    const clientNameInput = document.getElementById("clientName");
    const clientPassword = document.getElementById("clientPassword");
    const currentPassword = document.getElementById("currentPassword");
    const callNextButton = document.getElementById("callNextButton");

    // Recupera os dados dos cookies
    let senhasGeradas = JSON.parse(getCookie("senhasGeradas") || "[]");
    let senhaAtualIndex = parseInt(getCookie("senhaAtualIndex") || "0");

    // Atualiza a senha atual na interface
    function atualizarSenhaAtual() {
        if (senhaAtualIndex > 0 && senhaAtualIndex <= senhasGeradas.length) {
            currentPassword.textContent = senhasGeradas[senhaAtualIndex - 1];
        } else {
            currentPassword.textContent = "---";
        }
    }

    atualizarSenhaAtual();

    // Função para formatar as senhas com base no nome
    function gerarSenhaComNome(nome) {
        const initials = nome
            .split(' ')
            .map(word => word.charAt(0).toUpperCase())
            .join('');
        const numero = (senhasGeradas.length + 1).toString().padStart(3, '0');
        return `${initials}${numero}`;
    }

    // Gerar uma nova senha
    generateButton.addEventListener("click", () => {
        const nome = clientNameInput.value.trim();
        if (!nome) {
            alert("Por favor, insira seu nome.");
            return;
        }

        const novaSenha = gerarSenhaComNome(nome);
        senhasGeradas.push(novaSenha);
        setCookie("senhasGeradas", JSON.stringify(senhasGeradas), 1); // Armazena as senhas no cookie
        clientPassword.textContent = novaSenha;
        alert(`Sua senha é: ${novaSenha}`);
        clientNameInput.value = "";
    });

    // Chamar a próxima senha
    callNextButton.addEventListener("click", () => {
        if (senhaAtualIndex < senhasGeradas.length) {
            senhaAtualIndex++;
            setCookie("senhaAtualIndex", senhaAtualIndex, 1); // Armazena o índice da senha atual no cookie
            atualizarSenhaAtual();
        } else {
            alert("Não há mais senhas para chamar.");
        }
    });
});
