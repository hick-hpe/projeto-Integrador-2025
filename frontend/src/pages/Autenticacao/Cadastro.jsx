import styled from "styled-components";
import { useNavigate } from "react-router-dom";
import { useState } from "react";

const TelaStyled = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f3f3f3;
`;

const Form = styled.form`
  background-color: white;
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  width: 350px;
`;

const Title = styled.h2`
  text-align: center;
  color: #007bff;
  margin-bottom: 25px;
  font-size: 24px; /* aumentei para destaque */
`;

const Label = styled.label`
  display: block;
  margin-top: 12px;
  margin-bottom: 6px;
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

const StyledLink = styled.a`
  display: block;
  text-align: right;
  font-size: 14px; /* mínimo 14px */
  color: #007bff;
  text-decoration: none;
  margin-top: 12px;

  &:hover {
    text-decoration: underline;
  }
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
  font-size: 18px;

  &:hover {
    background-color: #218838;
  }
`;

export default function Cadastro() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [matricula, setMatricula] = useState("");
  const [email, setEmail] = useState("");
  const [password, setSenha] = useState("");
  const [confirmarSenha, setConfirmarSenha] = useState("");

  const handleCadastro = async (e) => {
    e.preventDefault();

    if (password !== confirmarSenha) {
      alert("As senhas não coincidem!");
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/auth/cadastro/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username, email, password, matricula
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        alert(data.error || "Erro ao cadastrar");
        return;
      }

      alert("Cadastro realizado com sucesso!");
      navigate("/");

    } catch (error) {
      console.error("Erro no cadastro:", error);
      alert("Erro inesperado ao cadastrar");
    }
  };

  return (
    <TelaStyled>
      <Form method="post">
        <Title>Crie sua Conta</Title>

        <Label>Nome completo</Label>
        <Input
          type="text"
          placeholder="Digite seu username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

        <Label>Matrícula</Label>
        <Input
          type="text"
          placeholder="Digite sua matrícula"
          value={matricula}
          onChange={(e) => setMatricula(e.target.value)}
        />

        <Label>Email</Label>
        <Input
          type="email"
          placeholder="Digite seu email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <Label>Senha</Label>
        <Input
          type="password"
          placeholder="Digite sua password"
          value={password}
          onChange={(e) => setSenha(e.target.value)}
        />

        <Label>Confirmar senha</Label>
        <Input
          type="password"
          placeholder="Confirme sua senha"
          value={confirmarSenha}
          onChange={(e) => setConfirmarSenha(e.target.value)}
        />

        <Button type="submit" onClick={handleCadastro}>Entrar</Button>

        <StyledLink href="/">Já tem conta? Entre!</StyledLink>
      </Form>
    </TelaStyled>
  );
}

