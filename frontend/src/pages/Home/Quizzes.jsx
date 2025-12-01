import styled from "styled-components";
import { FaFilter, FaClipboardList } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import Sidebar from "../../components/Sidebar";
import Modal from "../../components/Modal";

const Container = styled.div`
  display: flex;
  height: 100vh;
  width: 100%;
  overflow: hidden;
  background-color: #eef1f5;
  font-family: Arial, sans-serif;
`;

const Content = styled.div`
  flex: 1;
  padding: 40px;
  overflow-y: auto;
  height: 100vh;
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

const QuizButtonDesativado = styled.button`
  background-color: #559b66;
  color: white;
  padding: 8px 12px;
  border: none;
  border-radius: 6px;
  font-weight: bold;
  cursor: not-allowed;
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 15px;
`;

const ContainerFilters = styled.div`
  display: flex;
  justify-content: space-between;
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

export default function Quizzes() {
  const navigate = useNavigate();
  const [filtroTipo, setFiltroTipo] = useState("Todos");
  const [filtroDisciplinas, setFiltroDisciplinas] = useState("Todos");
  const [listDisciplinas, setListDisciplinas] = useState([]);
  const [listDisciplinasFiltro, setListDisciplinasFiltro] = useState([]);
  const [listQuizzes, setListQuizzes] = useState([]);
  const [chaveValorDiscQuiz, setChaveValorDiscQuiz] = useState({});
  const [chaveValorDiscQuizFilter, setChaveValorDiscQuizFilter] = useState({});
  const [podeFazerQuiz, setPodeFazerQuiz] = useState({});
  const [modalVisible, setModalVisible] = useState(false);
  const [username, setUsername] = useState("");

  // autenticacao
  useEffect(() => {
    const fetchUserData = async () => {
      // verificar se ta logado
      try {
        const response = await fetch("http://localhost:8000/auth/me/", {
          method: "GET",
          credentials: "include", // envia os cookies
        });

        if (response.status === 401) {
          // não está autenticado
          window.location.href = "/";
          return;
        }

        if (response.ok) {
          const data = await response.json();
          setUsername(data.username);
        } else {
          console.error("Erro ao buscar dados do usuário");
        }
      } catch (error) {
        console.error("Erro na requisição:", error);
      }
    }
    fetchUserData();
  }, []);

  const URL_DISCIPLINAS = "http://localhost:8000/api/disciplinas/";

  // buscar disciplinas
  useEffect(() => {
    const fetchDisciplinas = async () => {
      try {
        const response = await fetch(URL_DISCIPLINAS, { credentials: "include" });
        const data = await response.json();
        setListDisciplinas(data);
        setListDisciplinasFiltro(data);
      } catch (err) {
        console.error("Erro ao buscar disciplinas:", err);
      }
    };

    fetchDisciplinas();
  }, []);

  // buscar quizzes
  useEffect(() => {
    const fetchQuizzes = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/quizzes/", {
          credentials: "include",
        });
        const quizzes = await response.json();
        setListQuizzes(quizzes);
      } catch (err) {
        console.error("Erro ao buscar quizzes:", err);
      }
    };

    fetchQuizzes();
  }, []);

  // organizar os quizzes por disciplinas
  useEffect(() => {
    if (!listQuizzes || listQuizzes.length === 0) return;

    const agrupado = {};
    listQuizzes.forEach((quiz) => {
      const idDisc = quiz.disciplina;
      if (!agrupado[idDisc]) agrupado[idDisc] = [];
      agrupado[idDisc].push(quiz);
    });

    // console.log('agrupado:', agrupado);
    setChaveValorDiscQuiz(agrupado);
    setChaveValorDiscQuizFilter(agrupado);
  }, [listQuizzes]);

  // verificar se pode fazer os quizzes
  useEffect(() => {
    if (!listQuizzes || listQuizzes.length === 0) return;

    const fetchChecks = async () => {
      try {
        // Criar um array de promessas
        const promessas = listQuizzes.map((quiz) =>
          fetch(`http://localhost:8000/api/quizzes/${quiz.id}/aluno-pode-fazer/`, {
            credentials: "include",
          })
            .then((res) => res.json())
            .then((data) => ({
              id: quiz.id,
              pode: data.detail === "OK"
            }))
        );

        // executar todas simultaneamente
        const resultados = await Promise.all(promessas);

        // transformar em objeto { id: boolean }
        const mapa = resultados.reduce((acc, item) => {
          acc[item.id] = item.pode;
          return acc;
        }, {});

        console.log('mapa: ', mapa);
        setPodeFazerQuiz(mapa);

      } catch (err) {
        console.error("Erro ao verificar quizzes:", err);
      }
    };

    fetchChecks();
  }, [listQuizzes]);

  // handle filtroTipo
  const handleFiltroTipoChange = (e) => {
    setFiltroTipo(e.target.value);

    if (e.target.value === "Todos") {
      setChaveValorDiscQuizFilter(chaveValorDiscQuiz);
      return;
    } else if (e.target.value === "Alta") {
      // Pontuação alta (300+)
      const filtrado = {};
      for (const discId in chaveValorDiscQuiz) {
        filtrado[discId] = chaveValorDiscQuiz[discId].filter(
          (quiz) => quiz.pontuacao >= 300
        );
      }
      setChaveValorDiscQuizFilter(filtrado);
    } else if (e.target.value === "Baixa") {
      // Pontuação baixa (<300)
      const filtrado = {};
      for (const discId in chaveValorDiscQuiz) {
        filtrado[discId] = chaveValorDiscQuiz[discId].filter(
          (quiz) => quiz.pontuacao < 300
        );
      }
      setChaveValorDiscQuizFilter(filtrado);
    } else if (["Iniciante", "Intermediário", "Avançado"].includes(e.target.value)) {
      // Nível
      const filtrado = {};
      for (const discId in chaveValorDiscQuiz) {
        filtrado[discId] = chaveValorDiscQuiz[discId].filter(
          (quiz) => quiz.nivel === e.target.value
        );
      }
      setChaveValorDiscQuizFilter(filtrado);
    }
  }

  // handle filtro disciplinas
  const handleFiltroDisciplinasChange = (e) => {
    const valor = e.target.value;
    setFiltroDisciplinas(valor);

    // Se escolher TODOS
    if (valor === "Todos") {
      setListDisciplinasFiltro(listDisciplinas);
      setChaveValorDiscQuizFilter(chaveValorDiscQuiz);
      return;
    }

    // Filtra disciplinas
    const disciplinasFiltradas = listDisciplinas.filter(
      (disc) => disc.nome === valor
    );
    setListDisciplinasFiltro(disciplinasFiltradas);

    // Filtra quizzes ligados à disciplina selecionada
    const filtrado = {};
    for (const discNome in chaveValorDiscQuiz) {
      if (discNome === valor) {
        filtrado[discNome] = chaveValorDiscQuiz[discNome];
      }
    }

    setChaveValorDiscQuizFilter(filtrado);
  };

  const realizarQuiz = (quizID) => {
    // console.log("Realizar quiz de ", disciplina);
    // console.log("Id: ", disciplina.id);
    console.log(`Pode fazer Quiz_id=${quizID}?? -> ${podeFazerQuiz[quizID]}`);

    if (!podeFazerQuiz[quizID]) {
      setModalVisible(true);
    } else {
      navigate(`/quiz-info/${quizID}`);
    }
  }

  return (
    <Container>

      <Sidebar />

      <Modal visible={modalVisible} onClose={() => setModalVisible(false)}>
        <h2>Você não pode fazer este quiz!!!</h2>
        <p style={{ marginTop: '10px' }}>Deve concluir o de nível anterior!</p>
      </Modal>

      <Content>
        <ContainerFilters>
          <FilterSection>
            <span>Filtrar por:</span>
            <FaFilter />
            <Select value={filtroTipo} onChange={handleFiltroTipoChange}>
              <option value="Todos">Todos</option>
              <option value="Alta">Pontuação Alta (300+)</option>
              <option value="Baixa">Pontuação Baixa (&lt;300)</option>
              <option value="Iniciante">Iniciante</option>
              <option value="Intermediário">Intermediário</option>
              <option value="Avançado">Avançado</option>
            </Select>
          </FilterSection>
          <FilterSection>
            <span>Filtrar por disciplinas</span>
            <FaFilter />
            <Select value={filtroDisciplinas} onChange={handleFiltroDisciplinasChange}>
              <option value="Todos">Todos</option>
              {
                listDisciplinas.length == 0 ?
                  (<option value="">Carregando...</option>) :
                  listDisciplinas.map(disciplina => (
                    <option value={disciplina.nome}>{disciplina.nome}</option>
                  ))
              }
            </Select>
          </FilterSection>
        </ContainerFilters>

        {!listDisciplinasFiltro.length ? (
          <h2>Carregando disciplinas...</h2>
        ) : (
          listDisciplinasFiltro.map((disciplina) => (
            <TableSection key={disciplina.id}>
              <Title>Quizzes de {disciplina.nome}</Title>

              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Título</TableCell>
                    <TableCell>Disciplina</TableCell>
                    <TableCell>Pontuação</TableCell>
                    <TableCell>Nível</TableCell>
                    <TableCell>Ação</TableCell>
                  </TableRow>
                </TableHead>

                <tbody>
                  {!chaveValorDiscQuizFilter[disciplina.nome] ? (
                    <TableRow key={`${disciplina.id} - ${disciplina.nome}`}>
                      <TableCell colSpan="4">Nenhum quiz disponível.</TableCell>
                    </TableRow>
                  ) : (
                    chaveValorDiscQuizFilter[disciplina.nome].map((quiz) => (
                      <TableRow key={`${quiz.id} - ${quiz.titulo}`}>
                        <TableCell>{quiz.descricao}</TableCell>
                        <TableCell>{disciplina.nome}</TableCell>
                        <TableCell>{quiz.pontuacao || "-"}</TableCell>
                        <TableCell>{quiz.nivel || "-"}</TableCell>
                        <TableCell>
                          {
                            podeFazerQuiz[quiz.id] ?
                              <QuizButton onClick={() => realizarQuiz(quiz.id)}>
                                <FaClipboardList /> Realizar Quiz
                              </QuizButton>
                              :
                              <QuizButtonDesativado onClick={() => realizarQuiz(quiz.id)}>
                                <FaClipboardList /> Realizar Quiz
                              </QuizButtonDesativado>
                          }
                        </TableCell>
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
