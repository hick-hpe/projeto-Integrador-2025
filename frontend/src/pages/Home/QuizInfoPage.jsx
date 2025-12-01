import styled from "styled-components";
import { useNavigate, useParams } from "react-router-dom";
import { FaArrowLeft, FaPlay } from "react-icons/fa";
import Sidebar from "../../components/Sidebar";
import { useEffect, useState } from "react";

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

export default function QuizInfoPage() {
  const navigate = useNavigate();
  const { id } = useParams();

  const [quiz, setQuiz] = useState(null);
  const [questoes, setQuestoes] = useState([]);
  const [username, setUsername] = useState("");
  const [quizIniciado, setQuizIniciado] = useState(false);

  // auth
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

  // quiz info
  useEffect(() => {
    const fetchQuiz = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/quizzes/${id}/`, {
          credentials: "include"
        });
        const data = await response.json();
        setQuiz(data);
        console.log("Quiz data:", data);
      } catch (err) {
        console.error("Erro ao buscar quiz:", err);
      }
    };

    fetchQuiz();
  }, [id]);

  // questoes
  useEffect(() => {
    const fetchQuestoes = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/quizzes/${id}/questoes/`, {
          credentials: "include"
        });
        const data = await response.json();
        setQuestoes(data);
      } catch (err) {
        console.error("Erro ao buscar questões:", err);
      }
    };

    fetchQuestoes();
  }, [id]);

  // iniciar quiz
  const fetchIniciarQuiz = async () => {
    try {
      await fetch(`http://localhost:8000/api/quizzes/${id}/iniciar/`, {
        method: 'POST',
        credentials: 'include'
      });

      // iniciar
      setQuizIniciado(true);

    } catch (err) {
      console.error(err);
    }
  }

  // iniciar e redirecionar
  const handleIniciarQuiz = async () => {
    await fetchIniciarQuiz();
    navigate(`/quiz-info/${id}/iniciado`);
  };

  return (
    <Container>
      <Sidebar />

      <Content>
        <Title>
          <div style={{ display: "flex", alignItems: 'center', gap: '10px' }}>
            <FaArrowLeft onClick={() => navigate('/quizzes/')} style={{ cursor: 'pointer' }} /> {quiz?.titulo} - {quiz?.nivel}
          </div>
        </Title>
        <Paragraph><Highlight>Informações acerca do quiz:</Highlight></Paragraph>
        <Paragraph>
          {quiz?.descricao}
        </Paragraph>
        <Paragraph><Highlight>Quantidade de perguntas:</Highlight> {questoes.length}</Paragraph>
        <Paragraph><Highlight>Tipo de perguntas:</Highlight> {quiz?.tipo_questoes}</Paragraph>
        <Paragraph><Highlight>Tempo estimado:</Highlight> 15 minutos</Paragraph>
        <Paragraph><Highlight>Notas:</Highlight><br />
          A desistência da realização do quiz não salvará seu progresso e você não irá conquistar pontos.
          Portanto, será necessário refazê-lo e completá-lo.
        </Paragraph>
        <StartButton onClick={handleIniciarQuiz}>
          <FaPlay /> Iniciar quiz
        </StartButton>
      </Content>
    </Container>
  );
}
