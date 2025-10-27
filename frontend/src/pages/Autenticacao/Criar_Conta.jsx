import styled from "styled-components";
import { useNavigate } from "react-router-dom";

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

const Link = styled.a`
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

const FooterText = styled.p`
  text-align: center;
  font-size: 14px;
  margin-top: 15px;

  a {
    color: #007bff;
    text-decoration: none;

    &:hover {
      text-decoration: underline;
    }
  }
`;

export default function Criar_Conta() {
  const navigate = useNavigate();

  const handleCadastro = () => {
    // Aqui você pode adicionar validações ou lógica de envio
    navigate('/Tela_cadastrada'); // Redireciona para a próxima tela
  };

  return (
    <TelaStyled>
      <Card>
        <Title>Crie sua Conta</Title>
        <Label>Nome completo</Label>
        <Input type="text" placeholder="Digite seu nome" />
        <Label>Email</Label>
        <Input type="email" placeholder="Digite seu email" />
        <Label>Senha</Label>
        <Input type="password" placeholder="Digite sua senha" />
        <Label>Confirmar senha</Label>
        <Input type="password" placeholder="Confirme sua senha" />
        <Button onClick={handleCadastro}>Cadastrar</Button>
        <FooterText>
          Já tem conta? <Link href="/">Voltar início</Link>
        </FooterText>
      </Card>
    </TelaStyled>
  );
}