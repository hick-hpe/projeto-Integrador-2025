import React, { useState } from "react";
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
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState({});
  const [selectedOption, setSelectedOption] = useState("");

  const questions = [
    {
      id: 1,
      text: "Qual comando é usado para iniciar um novo projeto Django?",
      options: [
        "django-admin startproject",
        "django-admin startapp",
        "python manage.py runserver",
        "django new project",
      ],
    },
    {
      id: 2,
      text: "O que o arquivo `urls.py` define?",
      options: [
        "Estilos CSS do projeto",
        "As rotas entre URLs e views",
        "As configurações de banco de dados",
        "Os templates HTML",
      ],
    },
    {
      id: 3,
      text: "Qual comando roda o servidor local do Django?",
      options: [
        "python manage.py runserver",
        "django-admin deploy",
        "python server.py",
        "django manage.py server",
      ],
    },
  ];

  const handleOptionChange = (e) => {
    setSelectedOption(e.target.value);
  };

  const handleSubmit = () => {
    if (!selectedOption) return;

    setAnswers({ ...answers, [questions[currentQuestion].id]: selectedOption });
    setSelectedOption("");

    if (currentQuestion + 1 < questions.length) {
      setCurrentQuestion(currentQuestion + 1);
    } else {
      navigate("/resultado", { state: { answers } });
    }
  };

  const handleQuit = () => {
    navigate("/Home/Disciplinas/Desenvolvimento_web/desistiu", {
      state: { nomeQuiz: "Des. Web II - Básico" }
    });
  };

  const q = questions[currentQuestion];

  return (
    <PageContainer>
      <QuizBox>
        <QuizTitle>Quiz: Des. Web II - Básico</QuizTitle>
        <QuestionNumber>Pergunta {currentQuestion + 1}</QuestionNumber>
        <QuestionText>{q.text}</QuestionText>
        {q.options.map((opt, idx) => (
          <Option key={idx} selected={selectedOption === opt}>
            <input
              type="radio"
              name={`question-${q.id}`}
              value={opt}
              checked={selectedOption === opt}
              onChange={handleOptionChange}
            />
            {String.fromCharCode(65 + idx)} {opt}
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
