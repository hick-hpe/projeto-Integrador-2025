import styled from "styled-components";
import { FaFilter, FaClipboardList } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import Sidebar from "../../components/Sidebar";

const Container = styled.div`
  display: flex;
  height: 100vh;
  font-family: Arial, sans-serif;
  font-size: 16px; /* fonte mínima */
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
  const [listDisciplinas, setListDisciplinas] = useState([]);
  const [chaveValorDiscQuiz, setChaveValorDiscQuiz] = useState({});

  const URL_DISCIPLINAS = "http://localhost:8000/api/disciplinas/";

  // Buscar disciplinas
  useEffect(() => {
    const fetchDisciplinas = async () => {
      try {
        const response = await fetch(URL_DISCIPLINAS, { credentials: "include" });
        const data = await response.json();
        setListDisciplinas(data);
      } catch (err) {
        console.error("Erro ao buscar disciplinas:", err);
      }
    };

    fetchDisciplinas();
  }, []);

  // Buscar quizzes
  useEffect(() => {
    if (!listDisciplinas.length) return;

    const fetchQuizzes = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/quizzes/", {
          credentials: "include",
        });

        const quizzes = await response.json();

        const agrupado = {};
        quizzes.forEach((quiz) => {
          const idDisc = quiz.disciplina;
          if (!agrupado[idDisc]) agrupado[idDisc] = [];
          agrupado[idDisc].push(quiz);
        });

        setChaveValorDiscQuiz(agrupado);
      } catch (err) {
        console.error("Erro ao buscar quizzes:", err);
      }
    };

    fetchQuizzes();
  }, [listDisciplinas]);

  const realizarQuiz = (disciplina) =>
    navigate(`/Home/Disciplinas/${disciplina.nome}`);

  return (
    <Container>
      
      <Sidebar />

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

        {!listDisciplinas.length ? (
          <h2>Carregando disciplinas...</h2>
        ) : (
          listDisciplinas.map((disciplina) => (
            <TableSection key={disciplina.id}>
              <Title>Quizzes de {disciplina.nome}</Title>

              <QuizButton onClick={() => realizarQuiz(disciplina)}>
                <FaClipboardList /> Realizar Quiz
              </QuizButton>

              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Título</TableCell>
                    <TableCell>Disciplina</TableCell>
                    <TableCell>Pontuação</TableCell>
                    <TableCell>Nível</TableCell>
                  </TableRow>
                </TableHead>

                <tbody>
                  {!chaveValorDiscQuiz[disciplina.id] ? (
                    <TableRow>
                      <TableCell colSpan="4">Carregando quizzes...</TableCell>
                    </TableRow>
                  ) : chaveValorDiscQuiz[disciplina.id].length === 0 ? (
                    <TableRow>
                      <TableCell colSpan="4">Nenhum quiz disponível.</TableCell>
                    </TableRow>
                  ) : (
                    chaveValorDiscQuiz[disciplina.id].map((quiz) => (
                      <TableRow key={quiz.id}>
                        <TableCell>{quiz.descricao}</TableCell>
                        <TableCell>{disciplina.nome}</TableCell>
                        <TableCell>{quiz.pontuacao || "-"}</TableCell>
                        <TableCell>{quiz.nivel || "-"}</TableCell>
                      </TableRow>
                    ))
                  )}
                </tbody>
              </Table>
            </TableSection>
          ))
        )}
      </Content>
    </Container>
  );
}
