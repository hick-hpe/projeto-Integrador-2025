import styled from "styled-components";
import { FiArrowLeft } from "react-icons/fi";
import { Link } from "react-router-dom";

const Tela = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f3f3f3;
`;

const Cartao = styled.div`
  background-color: white;
  padding: 30px 40px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 350px;
  position: relative;
`;

const LinkVoltar = styled(Link)`
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

const Titulo = styled.h2`
  text-align: center;
  margin: 10px 0 20px;
  font-size: 22px;
  font-weight: bold;
  color: #007bff;
`;

const Rotulo = styled.label`
  display: block;
  margin-top: 10px;
  margin-bottom: 5px;
  font-size: 14px;
`;

const Entrada = styled.input`
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
  margin-bottom: 10px;
  font-size: 14px;
`;

const BotaoLink = styled(Link)`
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

export default function EsqueceuSenha() {
  return (
    <Tela>
      <Cartao>
        <LinkVoltar to="/">
          <FiArrowLeft size={15} />
          Voltar início
        </LinkVoltar>
        <Titulo>Recuperação de senha</Titulo>
        <Rotulo>Digite seu e-mail</Rotulo>
        <Entrada type="email" placeholder="Digite seu e-mail" />
        <BotaoLink to="/verificacao_recuperacao">
          Receber link de verificação
        </BotaoLink>
      </Cartao>
    </Tela>
  );
}

//Json
const handleRecover = (e) => {
  e.preventDefault();
  const info = { email };
  fetch('http://localhost:8000/api/recuperar-senha', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(info)
  })
    .then(res => res.json())
    .then(data => {
      console.log('Recuperação de senha:', data);
      alert('Verifique seu e-mail para redefinir a senha.');
    })
    .catch(err => {
      console.error('Erro na recuperação de senha:', err);
    });
};
