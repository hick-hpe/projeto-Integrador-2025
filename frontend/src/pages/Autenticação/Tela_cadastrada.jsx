import styled from "styled-components";
import { FiArrowLeft } from "react-icons/fi";
import { Link } from "react-router-dom";

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
  gap: 5px;
  color: black;
  font-size: 14px;
  text-decoration: none;
  margin-bottom: 15px;

  &:hover {
    text-decoration: underline;
  }
`;

const Title = styled.h2`
  text-align: center;
  margin: 10px 0 20px;
  font-size: 22px;
  font-weight: bold;
  color: #28a745;
`;

const Message = styled.p`
  text-align: center;
  font-size: 16px;
  color: #555;
  margin-bottom: 20px;
`;

const Button = styled(Link)`
  display: block;
  text-align: center;
  padding: 12px;
  background-color: #007bff;
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 5px;
  text-decoration: none;
  font-size: 16px;

  &:hover {
    background-color: #0056b3;
  }
`;

const TopText = styled.div`
  position: absolute;
  top: 10px;
  left: 20px;
  font-size: 12px;
  color: #ccc;
`;

export default function CadastroRealizado() {
  return (
    <TelaStyled>
      <TopText>Cadastro</TopText>
      <Card>
        <BackLink to="/">
          <FiArrowLeft size={15} />
          Voltar início
        </BackLink>
        <Title>Cadastro Realizado!</Title>
        <Message>Seu cadastro foi concluído com sucesso. Seja bem-vindo!</Message>
        <Button to="/">Ir para login</Button>
      </Card>
    </TelaStyled>
  );
}