import { useEffect, useState } from "react";
import styled from "styled-components";
import { FaPlay, FaTimes } from "react-icons/fa";
import { useNavigate, useParams } from "react-router-dom";

const PageContainer = styled.div`
  background-color: #f2f2f2;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: 'Segoe UI', Roboto, Arial, sans-serif;
`;

const QuizBox = styled.div`
  background-color: #ffffff;
  border-radius: 12px;
  padding: 35px 40px;
  width: 100%;
  max-width: 700px;
  box-shadow: 0px 3px 12px rgba(0, 0, 0, 0.12);
`;

const QuizTitle = styled.h2`
  color: #337eff;
  font-weight: bold;
  margin-bottom: 30px;
  font-size: 24px;
`;

const QuestionNumber = styled.h3`
  color: #333;
  font-size: 20px;
  margin-bottom: 8px;
`;

const QuestionText = styled.p`
  font-size: 18px;
  margin-bottom: 25px;
  color: #222;
`;

const Option = styled.label`
  display: block;
  background-color: ${({ selected }) => (selected ? "#bdeeff" : "#eee")};
  padding: 12px 16px;
  margin-bottom: 12px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  transition: background 0.2s;

  &:hover {
    background-color: #dcefff;
  }

  input {
    margin-right: 10px;
  }
`;

const Buttons = styled.div`
  display: flex;
  justify-content: space-between;
  margin-top: 30px;
  flex-wrap: wrap;
`;

const SubmitButton = styled.button`
  background-color: #28a745;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;

  &:hover {
    background-color: #218838;
  }
`;

const QuitButton = styled.button`
  background-color: #c82333;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;

  &:hover {
    background-color: #a71d2a;
  }
`;

export default function QuizIniciado() {
  const navigate = useNavigate();
  const { id } = useParams();
  const [quizIniciado, setQuizIniciado] = useState(false);
  const [quiz, setQuiz] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [alternativaID, setAlternativaID] = useState(null);
  const [answers, setAnswers] = useState({});
  const [selectedOption, setSelectedOption] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [username, setUsername] = useState("");

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await fetch("http://localhost:8000/auth/me/", {
          method: "GET",
          credentials: "include" // envia os cookies
        });

        console.log(response.status);

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

  // buscar info quiz
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
  }, [username, id]);

  // iniciar quiz
  useEffect(() => {
    if (!id || !quiz) return;

    const fetchIniciarQuiz = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/quizzes/${id}/iniciar/`, {
          method: 'POST',
          credentials: 'include'
        });

        if (response.ok) {
          setQuizIniciado(true);
        }
      } catch (err) {
        console.error(err);
      }
    }
    fetchIniciarQuiz();
  }, [quiz, id]);

  // buscar perguntas do backend
  useEffect(() => {
    if (!quizIniciado) return;

    const fetchQuestions = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/quizzes/${id}/questoes/`,
          { credentials: 'include' });
        if (!response.ok) throw new Error("Erro ao buscar questões");
        const data = await response.json();
        setQuestions(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchQuestions();
  }, [quizIniciado]);

  // escolher uma opção
  const handleOptionChange = (e, altID) => {
    setAlternativaID(altID);
    setSelectedOption(e.target.value);
  };

  // salva resposta marcada
  const handleSubmit = async () => {
    if (!selectedOption) return;

    const questionId = questions[currentQuestion].id;
    const URL_ENVIAR_RESPOSTA = `http://localhost:8000/api/quizzes/${id}/questoes/${questionId}/`;

    const data = {
      alternativa_id: alternativaID
    };

    try {
      await fetch(URL_ENVIAR_RESPOSTA, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),
      });
    } catch (err) {
      console.error("Erro ao enviar resposta:", err);
    }

    // próxima questão
    if (currentQuestion + 1 < questions.length) {
      setCurrentQuestion(prev => prev + 1);
    } else {
      navigate("/resultado-quiz/");
    }
  };

  const handleQuit = () => {
    // navigate("/desistiu-quiz");
  };

  // Mostrar estado de carregamento ou erro
  if (loading) return <p>Carregando perguntas...</p>;
  if (error) return <p>Erro: {error}</p>;
  if (questions.length === 0) return <p>Nenhuma questão encontrada.</p>;

  return (
    <PageContainer>
      <QuizBox>
        <QuizTitle>{quiz?.titulo} - {quiz?.nivel}</QuizTitle>

        <QuestionNumber>Pergunta {currentQuestion + 1}</QuestionNumber>
        <QuestionText>{questions[currentQuestion].descricao}</QuestionText>

        {questions[currentQuestion].alternativas.map((alt, idx) => (
          <Option key={alt.id} selected={selectedOption === alt.texto}>
            <input
              type="radio"
              name={`question-${questions[currentQuestion].id}`}
              value={alt.texto}
              checked={selectedOption === alt.texto}
              onChange={(e) => handleOptionChange(e, alt.id)}
            />
            {String.fromCharCode(65 + idx)}) {alt.texto}
          </Option>
        ))}

        <Buttons>
          <QuitButton onClick={handleQuit}>
            <FaTimes /> Desistir
          </QuitButton>
          <SubmitButton onClick={handleSubmit}>
            <FaPlay />
            {currentQuestion + 1 === questions.length
              ? "Finalizar"
              : "Próxima pergunta"}
          </SubmitButton>
        </Buttons>
      </QuizBox>
    </PageContainer>
  );
};
