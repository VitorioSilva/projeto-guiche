document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('login-form');

    form.addEventListener('submit', async (event) => {
        event.preventDefault(); 

        const email = document.getElementById('email').value;
        const senha = document.getElementById('senha').value;

        try {
            
            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, senha })
            });

            if (!response.ok) {
                throw new Error('Erro no login. Verifique suas credenciais.');
            }

            const data = await response.json();

            
            if (data.token) {
                
                document.cookie = `jwt=${data.token}; path=/; Secure; HttpOnly`;
                alert('Login bem-sucedido!');

                
                window.location.href = '/dashboard';
            } else {
                throw new Error('Token não recebido.');
            }
        } catch (error) {
            alert(error.message);
        }
    });
});
