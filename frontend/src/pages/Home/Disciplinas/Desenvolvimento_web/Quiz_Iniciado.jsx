import React, { useEffect, useState } from "react";
import styled from "styled-components";
import { FaPlay, FaTimes } from "react-icons/fa";
import { useNavigate } from "react-router-dom";

const PageContainer = styled.div`
  background-color: #f2f2f2;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 20px;
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

const QuizForm = () => {
  const navigate = useNavigate();
  const [questions, setQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState({});
  const [selectedOption, setSelectedOption] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");


  // Buscar perguntas do backend
  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/quizzes/1/questoes/", { credentials: 'include' });
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
  }, []);

  const handleOptionChange = (e) => {
    setSelectedOption(e.target.value);
  };

  const handleSubmit = () => {
    if (!selectedOption) return;

    const questionId = questions[currentQuestion].id;
    setAnswers({ ...answers, [questionId]: selectedOption });
    setSelectedOption("");

    if (currentQuestion + 1 < questions.length) {
      setCurrentQuestion(currentQuestion + 1);
    } else {
      navigate("/resultado", { state: { answers } });
    }
  };

  const handleQuit = () => {
    navigate("/Home/Disciplinas/Desenvolvimento_web/desistiu", {
      state: { nomeQuiz: "Des. Web II - Básico" },
    });
  };

  // Mostrar estado de carregamento ou erro
  if (loading) return <p>Carregando perguntas...</p>;
  if (error) return <p>Erro: {error}</p>;
  if (questions.length === 0) return <p>Nenhuma questão encontrada.</p>;

  const q = questions[currentQuestion];

  return (
    <PageContainer>
      <QuizBox>
        <QuizTitle>Quiz: Des. Web II - Básico</QuizTitle>
        <QuestionNumber>Pergunta {currentQuestion + 1}</QuestionNumber>
        <QuestionText>{q.descricao}</QuestionText>

        {q.alternativas.map((alt, idx) => (
          <Option key={alt.id} selected={selectedOption === alt.texto}>
            <input
              type="radio"
              name={`question-${q.id}`}
              value={alt.texto}
              checked={selectedOption === alt.texto}
              onChange={handleOptionChange}
            />
            {String.fromCharCode(65 + idx)} {alt.texto}
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

export default QuizForm;
