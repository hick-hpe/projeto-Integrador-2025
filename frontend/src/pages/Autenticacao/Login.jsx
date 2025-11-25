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
    font-size: 24px;
`;

const Label = styled.label`
    display: block;
    margin-top: 15px;
    margin-bottom: 5px;
    font-size: 14px; /* mínimo 14px */
`;

const Input = styled.input`
    width: 100%;
    padding: 12px;
    border-radius: 5px;
    border: 1px solid #ccc;
    margin-bottom: 12px;
    font-size: 14px; /* mínimo 14px */
`;

const Button = styled.button`
    width: 100%;
    padding: 14px;
    background-color: #28a745;
    color: white;
    font-weight: bold;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 18px; /* confortável e acima de 14px */

    &:hover {
        background-color: #218838;
    }
`;

const StyledLink = styled(RouterLink)`
    display: block;
    text-align: right;
    font-size: 14px; /* mínimo 14px */
    color: #007bff;
    text-decoration: none;
    margin-bottom: 15px;
    margin-top: 12px;

    &:hover {
        text-decoration: underline;
    }
`;

const FooterText = styled.p`
    text-align: center;
    font-size: 14px; /* mínimo 14px */

    a {
        color: #007bff;
        text-decoration: none;

        &:hover {
            text-decoration: underline;
        }
    }
`;


export default function Login() {
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
            // const response = await fetch(URL_LOGIN, {
            //     method: 'POST',
            //     headers: {
            //         'Content-Type': 'application/json',
            //     },
            //     body: JSON.stringify(dadosLogin),
            //     credentials: 'include'
            // });

            // const data = await response.json();
            // console.log(data);

            // if (response.ok) {
                navigate("/dashboard");
            // } else {
            //     alert("Login falhou: " + (data.detail || "Erro desconhecido"));
            // }
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

                <StyledLink to="/esqueceu-senha">Esqueceu a senha?</StyledLink>

                <Button onClick={handleLogin}>Entrar</Button>

                <FooterText>
                    <StyledLink to="/cadastro">Não tem conta? Cadastre-se</StyledLink>
                </FooterText>
            </Card>
        </TelaStyled>
    );
}



