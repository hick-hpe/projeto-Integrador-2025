import { useLocation, useNavigate } from "react-router-dom";
import styled from "styled-components";

const Container = styled.div`
  background-color: #f2f2f2;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: 'Segoe UI', Roboto, Arial, sans-serif;
`;

const ResultBox = styled.div`
  background-color: #fff;
  border-radius: 12px;
  padding: 35px 40px;
  max-width: 700px;
  width: 100%;
  box-shadow: 0px 3px 12px rgba(0, 0, 0, 0.12);
`;

const Title = styled.h2`
  color: #337eff;
  font-weight: bold;
  margin-bottom: 30px;
  font-size: 24px;
`;

const AnswerItem = styled.div`
  margin-bottom: 20px;
`;

const QuestionText = styled.p`
  font-weight: bold;
  margin-bottom: 5px;
`;

const UserAnswer = styled.p`
  color: ${({ correct }) => (correct ? "#28a745" : "#c82333")};
`;

const BackButton = styled.button`
  background-color: #337eff;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  border-radius: 6px;
  cursor: pointer;
  margin-top: 30px;

  &:hover {
    background-color: #2868d6;
  }
`;

export default function ResultadoQuiz() {
    const location = useLocation();
    const navigate = useNavigate();
    const { answers } = location.state || {};
    console.log(answers);

    const questions = [
        {
            id: 1,
            text: "Qual linguagem é conhecida por sua forte tipagem estática?",
            correct: "Java",
        },
        {
            id: 2,
            text: "Qual desses é um operador lógico em JavaScript?",
            correct: "||",
        },
        {
            id: 3,
            text: "Qual estrutura é usada para repetir um bloco de código em várias linguagens?",
            correct: "for",
        },
    ];

    const handleBack = () => {
        navigate("/");
    };

    return (
        <Container>
            <ResultBox>
                <Title>Resultado do Quiz</Title>
                {questions.map((q) => {
                    const userAnswer = answers?.[q.id];
                    const isCorrect = userAnswer === q.correct;

                    return (
                        <AnswerItem key={q.id}>
                            <QuestionText>{q.text}</QuestionText>
                            <UserAnswer correct={isCorrect}>
                                Sua resposta: {userAnswer || "Não respondida"} <br />
                                {isCorrect ? "✅ Correta" : `❌ Correta: ${q.correct}`}
                            </UserAnswer>
                        </AnswerItem>
                    );
                })}
                <BackButton onClick={handleBack}>Voltar ao início</BackButton>
            </ResultBox>
        </Container>
    );
};
