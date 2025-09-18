import styled from "styled-components";
import { useNavigate } from "react-router-dom";
import { FaPlay } from "react-icons/fa";

const Container = styled.div`
  display: flex;
  height: 100vh;
  font-family: Arial, sans-serif;
`;

const Sidebar = styled.div`
  width: 200px;
  background-color: #007bff;
  color: white;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
`;

const SidebarTitle = styled.h3`
  color: white;
  margin-bottom: 30px;
`;

const SidebarButton = styled.button`
  background-color: ${(props) => (props.active ? "#e6f4ff" : "#0056b3")};
  border: ${(props) => (props.active ? "2px solid #00ccff" : "none")};
  color: ${(props) => (props.active ? "#007bff" : "white")};
  border-radius: 10px;
  padding: 10px;
  text-align: left;
  cursor: pointer;
  font-weight: bold;
  &:hover {
    background-color: #3399ff;
  }
`;

const Content = styled.div`
  flex: 1;
  background-color: #f7f7f7;
  padding: 30px;
`;

const Title = styled.h2`
  color: #007bff;
  margin-bottom: 20px;
`;

const Paragraph = styled.p`
  margin-bottom: 10px;
  line-height: 1.6;
`;

const Highlight = styled.span`
  font-weight: bold;
`;

const StartButton = styled.button`
  background-color: #28a745;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  margin-top: 20px;
`;

export default function Quiz_de_Programacao() {
  const navigate = useNavigate();

  return (
    <Container>
      <Sidebar>
        <SidebarTitle>DevQuiz Adm</SidebarTitle>
        <SidebarButton onClick={() => navigate("/Home/Tela")}>Home</SidebarButton>
        <SidebarButton active onClick={() => navigate("/Home/Quizzes")}>Quizzes</SidebarButton>
        <SidebarButton onClick={() => navigate("/Home/Certificados")}>Certificados</SidebarButton>
        <SidebarButton onClick={() => navigate("/Home/Ranking")}>Ranking</SidebarButton>
        <SidebarButton onClick={() => navigate("/Home/Perfil")}>Perfil</SidebarButton>
      </Sidebar>
      <Content>
        <Title>Quizzes de Programação</Title>
        <Paragraph><Highlight>Informações acerca do quiz:</Highlight></Paragraph>
        <Paragraph>
          Este quiz avalia os conhecimentos básicos sobre JavaScript, incluindo variáveis, estruturas de controle, funções e manipulação do DOM.
          Ideal para alunos que concluíram o módulo introdutório e desejam revisar os principais conceitos antes de avançar para tópicos mais avançados.
        </Paragraph>
        <Paragraph><Highlight>Quantidade de perguntas:</Highlight> 10</Paragraph>
        <Paragraph><Highlight>Tipo de perguntas:</Highlight> Múltipla escolha e verdadeiro/falso</Paragraph>
        <Paragraph><Highlight>Tempo estimado:</Highlight> 15 minutos</Paragraph>
        <Paragraph><Highlight>Notas:</Highlight><br />
          A desistência da realização do quiz não salvará seu progresso e você não irá conquistar pontos.
          Portanto, será necessário refazê-lo e completá-lo.
        </Paragraph>
        <StartButton onClick={() => navigate("/Home/Disciplinas/Pasta_de_Programacao/Quiz_iniciado")}>
          <FaPlay /> Iniciar quiz
        </StartButton>
      </Content>
    </Container>
  );
}
