import styled from "styled-components";
import { FaFilter, FaClipboardList } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import { useState } from "react";

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
  overflow-y: auto;
`;

const TableSection = styled.div`
  margin-bottom: 50px;
`;

const Title = styled.h2`
  color: #007bff;
  margin-bottom: 10px;
`;

const QuizButton = styled.button`
  background-color: #28a745;
  color: white;
  padding: 8px 12px;
  border: none;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 15px;
`;

const FilterSection = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 30px;
`;

const Select = styled.select`
  padding: 6px 10px;
  border-radius: 5px;
`;

const Table = styled.table`
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  border-radius: 10px;
  overflow: hidden;
`;

const TableHead = styled.thead`
  background-color: #00aaff;
  color: white;
`;

const TableRow = styled.tr`
  &:nth-child(even) {
    background-color: #f0f0f0;
  }
`;

const TableCell = styled.td`
  padding: 10px;
  text-align: center;
`;

export default function Quizzes_tela() {
  const navigate = useNavigate();
  const [filtro, setFiltro] = useState("Todos");

  const quizzesTabela1 = [
    {
      titulo: "Des. Web II - Básico",
      categoria: "Desenvolvimento Web",
      pontuacao: 200,
      nivel: "Iniciante",
    },
    {
      titulo: "Prog. Web I",
      categoria: "Desenvolvimento Web",
      pontuacao: 400,
      nivel: "Mediano",
    },
    {
      titulo: "Estrutura de Dados",
      categoria: "Programação",
      pontuacao: 600,
      nivel: "Avançado",
    },
  ];

  const quizzesTabela2 = [
    {
      titulo: "Des. Web II - Básico",
      categoria: "Desenvolvimento Web",
      pontuacao: 200,
      nivel: "Iniciante",
    },
    {
      titulo: "Prog. Web I",
      categoria: "Desenvolvimento Web",
      pontuacao: 400,
      nivel: "Mediano",
    },
    {
      titulo: "Estrutura de Dados",
      categoria: "Programação",
      pontuacao: 600,
      nivel: "Avançado",
    },
  ];

  const realizarQuiz = () => {
    navigate("/home/Disciplinas/Desenvolvimento_Web");
  };

  const Quiz_Programacao = () => {
    navigate("/home/Disciplinas/Quiz_Programacao");
  };

  const filtrarQuizzes = (quizzes) => {
    return quizzes.filter((quiz) => {
      if (filtro === "Todos") return true;
      if (filtro === "Alta") return quiz.pontuacao >= 300;
      if (filtro === "Baixa") return quiz.pontuacao < 300;
      return quiz.nivel === filtro;
    });
  };

  return (
    <Container>
      <Sidebar>
        <SidebarTitle>DevQuiz Aluno</SidebarTitle>
        <SidebarButton onClick={() => navigate("/Home/Tela")}>Home</SidebarButton>
        <SidebarButton active>Quizzes</SidebarButton>
        <SidebarButton onClick={() => navigate("/Home/Certificados")}>Certificados</SidebarButton>
        <SidebarButton onClick={() => navigate("/Home/Ranking")}>Ranking</SidebarButton>
        <SidebarButton onClick={() => navigate("/Home/Perfil")}>Perfil</SidebarButton>
      </Sidebar>

      <Content>
        <FilterSection>
          <span>Filtrar por:</span>
          <FaFilter />
          <Select value={filtro} onChange={(e) => setFiltro(e.target.value)}>
            <option value="Todos">Todos</option>
            <option value="Alta">Pontuação Alta (300+)</option>
            <option value="Baixa">Pontuação Baixa (&lt;300)</option>
            <option value="Iniciante">Iniciante</option>
            <option value="Mediano">Mediano</option>
            <option value="Avançado">Avançado</option>
          </Select>
        </FilterSection>

        {/* Primeira Tabela */}
        <TableSection>
          <Title>Quizzes de Desenvolvimento Web</Title>
          <QuizButton onClick={realizarQuiz}>
            <FaClipboardList /> Realizar Quiz
          </QuizButton>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Título</TableCell>
                <TableCell>Disciplina/Materia</TableCell>
                <TableCell>Pontuação</TableCell>
                <TableCell>Nível</TableCell>
              </TableRow>
            </TableHead>
            <tbody>
              {filtrarQuizzes(quizzesTabela1).map((quiz, index) => (
                <TableRow key={index}>
                  <TableCell>{quiz.titulo}</TableCell>
                  <TableCell>{quiz.categoria}</TableCell>
                  <TableCell>{quiz.pontuacao}</TableCell>
                  <TableCell>{quiz.nivel}</TableCell>
                </TableRow>
              ))}
            </tbody>
          </Table>
        </TableSection>

        {/* Segunda Tabela */}
        <TableSection>
          <Title>Quizzes de Programação</Title>
          <QuizButton onClick={Quiz_Programacao}>
            <FaClipboardList /> Realizar Quiz
          </QuizButton>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Título</TableCell>
                <TableCell>Disciplina/Materia</TableCell>
                <TableCell>Pontuação</TableCell>
                <TableCell>Nível</TableCell>
              </TableRow>
            </TableHead>
            <tbody>
              {filtrarQuizzes(quizzesTabela2).map((quiz, index) => (
                <TableRow key={index}>
                  <TableCell>{quiz.titulo}</TableCell>
                  <TableCell>{quiz.categoria}</TableCell>
                  <TableCell>{quiz.pontuacao}</TableCell>
                  <TableCell>{quiz.nivel}</TableCell>
                </TableRow>
              ))}
            </tbody>
          </Table>
        </TableSection>
      </Content>
    </Container>
  );
}
