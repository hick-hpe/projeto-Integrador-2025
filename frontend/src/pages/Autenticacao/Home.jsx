import styled from "styled-components";
import { useNavigate, Link as RouterLink } from "react-router-dom";
import { useState } from "react";

const TelaStyled = styled.div`
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: #f3f3f3;
`;

const Card = styled.div`
    background-color: white;
    padding: 40px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    width: 350px;
`;

const Title = styled.h2`
    text-align: center;
    color: #007bff;
    margin-bottom: 20px;
`;

const Label = styled.label`
    display: block;
    margin-top: 10px;
    margin-bottom: 5px;
    font-size: 14px;
`;

const Input = styled.input`
    width: 100%;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #ccc;
    margin-bottom: 10px;
    font-size: 14px;
`;

const Button = styled.button`
    width: 100%;
    padding: 12px;
    background-color: #28a745;
    color: white;
    font-weight: bold;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;

    &:hover {
        background-color: #218838;
    }
`;

const StyledLink = styled(RouterLink)`
    display: block;
    text-align: right;
    font-size: 12px;
    color: #007bff;
    text-decoration: none;
    margin-bottom: 15px;

    &:hover {
        text-decoration: underline;
    }
`;

const FooterText = styled.p`
    text-align: center;
    font-size: 14px;

    a {
        color: #007bff;
        text-decoration: none;

        &:hover {
            text-decoration: underline;
        }
    }
`;

export default function Home() {
    const navigate = useNavigate();
    const [username, setUsername] = useState('');
    const [senha, setSenha] = useState('');

    const handleLogin = async () => {
        const URL_LOGIN = 'http://localhost:8000/auth/login/';
        const dadosLogin = {
            username: username,
            password: senha,
        };

        try {
            const response = await fetch(URL_LOGIN, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(dadosLogin),
                credentials: 'include'
            });

            const data = await response.json();
            console.log(data);

            // Redireciona se o login for bem-sucedido
            if (response.ok) {
                navigate("/home/Tela");
            } else {
                alert("Login falhou: " + (data.detail || "Erro desconhecido"));
            }
        } catch (err) {
            console.error('Erro: ', err);
        }
    };

    return (
        <TelaStyled>
            <Card>
                <Title>Login</Title>

                <Label>Username</Label>
                <Input
                    type="email"
                    placeholder="Digite seu username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />

                <Label>Senha</Label>
                <Input
                    type="password"
                    placeholder="Digite sua senha"
                    value={senha}
                    onChange={(e) => setSenha(e.target.value)}
                />

                <StyledLink to="/Esqueceu_senha">Esqueceu a senha?</StyledLink>

                <Button onClick={handleLogin}>Entrar</Button>

                <FooterText>
                    Não tem conta? <StyledLink to="/Criar_Conta">Cadastre-se</StyledLink>
                </FooterText>
            </Card>
        </TelaStyled>
    );
}
