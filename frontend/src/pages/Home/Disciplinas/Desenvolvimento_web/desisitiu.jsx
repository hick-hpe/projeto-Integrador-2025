import React from "react";
import { useNavigate } from "react-router-dom";
import styled from "styled-components";

const TelaContainer = styled.div`
  height: 100vh;
  background-color: #fdeaea;
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: Arial, sans-serif;
`;

const Card = styled.div`
  background-color: white;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  text-align: center;
  max-width: 500px;
  width: 100%;
`;

const Emoji = styled.div`
  font-size: 2.5rem;
  margin-bottom: 10px;
`;

const Titulo = styled.h2`
  color: #c0392b;
  margin-bottom: 10px;
`;

const Texto = styled.p`
  font-size: 1rem;
  margin-bottom: 10px;
`;

const Alerta = styled.div`
  background-color: #fce2e2;
  padding: 16px;
  border-radius: 10px;
  color: #a94442;
  font-size: 0.95rem;
  margin: 20px 0;
`;

const Botoes = styled.div`
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
`;

const Botao = styled.button`
  padding: 10px 20px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-weight: bold;
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 8px;
  color: white;
  background-color: ${(props) => (props.painel ? "#6c757d" : "#007bff")};

  &:hover {
    background-color: ${(props) => (props.painel ? "#5a6268" : "#0056b3")};
  }
`;

export default function DesistenciaQuiz() {
  const navigate = useNavigate();

  return (
    <TelaContainer>
      <Card>
        <Emoji>😲</Emoji>
        <Titulo>Que pena!</Titulo>
        <Texto>
          Você desistiu do quiz de<strong>Desenvolvimento Web</strong>.
        </Texto>
        <Alerta>
          <p>Lembre-se: cada tentativa conta para seu progresso!</p>
          <p>
            Você ainda tem <strong>X</strong> tentativa(s) restante(s) neste quiz.
          </p>
        </Alerta>
        <Botoes>
          <Botao onClick={() => navigate("/Home/Disciplinas/Desenvolvimento_web")}>📘 Tentar novamente</Botao>
          <Botao painel onClick={() => navigate("/Home/Quizzes")}>🏠 Voltar ao Painel</Botao>
        </Botoes>
      </Card>
    </TelaContainer>
  );
}
