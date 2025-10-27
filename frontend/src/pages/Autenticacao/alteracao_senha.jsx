import styled from "styled-components";
import { FiArrowLeft, FiLock } from "react-icons/fi";
import { Link } from "react-router-dom";

const Tela = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f3f3f3;
  padding: 20px;
`;

const Cartao = styled.div`
  background-color: white;
  padding: 30px 40px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 350px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
`;

const LinkVoltar = styled(Link)`
  display: flex;
  align-items: center;
  gap: 5px;
  color: black;
  font-size: 14px;
  text-decoration: none;
  margin-bottom: 20px;

  &:hover {
    text-decoration: underline;
    color: #007bff;
  }
`;

const Titulo = styled.h2`
  text-align: center;
  margin: 10px 0 25px;
  font-size: 22px;
  font-weight: bold;
  color: #007bff;
`;

const GrupoInput = styled.div`
  position: relative;
  margin-bottom: 18px;
`;

const Icone = styled(FiLock)`
  position: absolute;
  top: 50%;
  left: 12px;
  transform: translateY(-50%);
  color: #aaa;
`;

const Entrada = styled.input`
  width: 100%;
  padding: 12px 12px 12px 38px;
  border-radius: 6px;
  border: 1px solid #ccc;
  font-size: 15px;
  box-sizing: border-box;
  transition: border-color 0.3s;

  &:focus {
    border-color: #007bff;
    outline: none;
  }
`;

const Botao = styled(Link)`
  align-self: center;
  width: auto;
  min-width: 220px;
  text-align: center;
  padding: 12px 20px;
  background-color: #28a745;
  color: white;
  font-weight: bold;
  border-radius: 6px;
  text-decoration: none;
  font-size: 16px;
  margin-top: 20px;
  transition: background-color 0.3s;

  &:hover {
    background-color: #218838;
  }
`;

export default function RedefinirSenha() {
  return (
    <Tela>
      <Cartao>
        <LinkVoltar to="/Verificacao_recuperacao">
          <FiArrowLeft size={15} />
          Voltar
        </LinkVoltar>
        <Titulo>Redefinir Senha</Titulo>
        <GrupoInput>
          <Icone />
          <Entrada type="password" placeholder="Nova senha" />
        </GrupoInput>
        <GrupoInput>
          <Icone />
          <Entrada type="password" placeholder="Confirmar nova senha" />
        </GrupoInput>
        <Botao to="/">Salvar e voltar ao login</Botao>
      </Cartao>
    </Tela>
  );
}
