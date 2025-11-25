import { useState } from "react";
import styled from "styled-components";
import { FiArrowLeft } from "react-icons/fi";
import { Link, useNavigate } from "react-router-dom";

const TelaStyled = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f3f3f3;
`;

const Card = styled.div`
  background-color: white;
  padding: 30px 40px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 350px;
  position: relative;
`;

const BackLink = styled(Link)`
  display: flex;
  align-items: center;
  gap: 6px;
  color: black;
  font-size: 14px; /* mínimo 14px */
  text-decoration: none;
  margin-bottom: 15px;

  &:hover {
    text-decoration: underline;
  }
`;

const Title = styled.h2`
  text-align: center;
  margin: 10px 0 20px;
  font-size: 24px; /* mais confortável */
  font-weight: bold;
  color: #28a745;
`;

const Input = styled.input`
  width: 100%;
  padding: 12px;
  margin-bottom: 14px;
  border: 1px solid #ccc;
  border-radius: 5px;
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
  font-size: 18px; /* maior para destaque */
  margin-top: 10px;

  &:hover {
    background-color: #218838;
    cursor: pointer;
  }
`;

const ErrorMsg = styled.p`
  color: red;
  font-size: 14px; /* mínimo 14px */
  text-align: center;
  margin-top: -5px;
  margin-bottom: 10px;
`;

export default function Cadastro() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const [error, setError] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // validação de senhas
    if (formData.password !== formData.confirmPassword) {
      setError("As senhas não coincidem.");
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/auth/cadastro/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: formData.username,
          email: formData.email,
          password: formData.password,
        }),
      });

      if (response.ok) {
        navigate("/cadastro/realizado");
      } else {
        const data = await response.json();
        setError(data?.error || "Erro ao cadastrar. Tente novamente.");
      }
    } catch (err) {
      setError("Erro de conexão com o servidor.");
    }
  };

  return (
    <TelaStyled>
      <Card>
        <BackLink to="/">
          <FiArrowLeft size={18} /> {/* aumentado para combinar */}
          Voltar
        </BackLink>

        <Title>Crie sua conta</Title>

        <form onSubmit={handleSubmit}>
          <Input
            type="text"
            name="username"
            placeholder="Usuário"
            value={formData.username}
            onChange={handleChange}
            required
          />
          <Input
            type="email"
            name="email"
            placeholder="E-mail"
            value={formData.email}
            onChange={handleChange}
            required
          />
          <Input
            type="password"
            name="password"
            placeholder="Senha"
            value={formData.password}
            onChange={handleChange}
            required
          />
          <Input
            type="password"
            name="confirmPassword"
            placeholder="Confirmar senha"
            value={formData.confirmPassword}
            onChange={handleChange}
            required
          />

          {error && <ErrorMsg>{error}</ErrorMsg>}

          <Button type="submit">Cadastrar</Button>
        </form>
      </Card>
    </TelaStyled>
  );
}
