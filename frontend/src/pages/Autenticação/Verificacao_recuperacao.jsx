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
  color: #007bff;
`;

const Message = styled.p`
  text-align: center;
  font-size: 15px;
  color: #555;
  margin-bottom: 20px;
`;

const Input = styled.input`
  width: 100%;
  padding: 12px;
  border-radius: 5px;
  border: 1px solid #ccc;
  font-size: 16px;
  text-align: center;
  letter-spacing: 4px;
  margin-bottom: 20px;
`;

const LinkButton = styled(Link)`
  display: block;
  width: 100%;
  text-align: center;
  padding: 12px;
  background-color: #28a745;
  color: white;
  font-weight: bold;
  border-radius: 5px;
  text-decoration: none;
  font-size: 16px;

  &:hover {
    background-color: #218838;
  }
`;

const TopText = styled.div`
  position: absolute;
  top: 10px;
  left: 20px;
  font-size: 12px;
  color: #ccc;
`;

const ResendLink = styled.a`
  display: block;
  text-align: center;
  font-size: 13px;
  color: #007bff;
  text-decoration: none;
  margin-top: 10px;

  &:hover {
    text-decoration: underline;
  }
`;

export default function VerificacaoCodigo() {
  return (
    <TelaStyled>
      <TopText>Recuperação</TopText>
      <Card>
        <BackLink to="/Esqueceu_senha">
          <FiArrowLeft size={15} />
          Voltar
        </BackLink>
        <Title>Verifique seu Código</Title>
        <Message>
          Um código foi enviado para sua caixa de entrada. Aguarde alguns instantes e insira-o abaixo para continuar a recuperação de senha.
        </Message>
        <Input type="text" maxLength="6" placeholder="••••••" />
        <LinkButton to="/alteracao_senha">Confirmar código</LinkButton>
        <ResendLink href="#">Reenviar código</ResendLink>
      </Card>
    </TelaStyled>
  );
}