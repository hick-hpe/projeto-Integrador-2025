import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import styled from "styled-components";

const Container = styled.div`
  background-color: #f4f6ff;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  padding: 40px 20px;
  align-items: flex-start;
  font-family: 'Segoe UI', Roboto, Arial, sans-serif;
`;

const ResultBox = styled.div`
  background-color: #ffffff;
  border-radius: 14px;
  padding: 35px 40px;
  max-width: 780px;
  width: 100%;
  box-shadow:
    0px 6px 16px rgba(0, 0, 0, 0.10),
    0px 1px 3px rgba(0,0,0,0.05);
`;

const Title = styled.h2`
  color: #337eff;
  font-weight: 700;
  margin-bottom: 30px;
  font-size: 26px;
  text-align: center;
`;

const AnswerItem = styled.div`
  background: #fafcff;
  border: 1px solid #e4eaff;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 20px;
`;

const QuestionText = styled.p`
  font-weight: 600;
  margin-bottom: 10px;
  font-size: 17px;
`;

const UserAnswer = styled.p`
  padding: 12px 15px;
  border-radius: 8px;
  background-color: ${({ correct }) =>
        correct ? "rgba(40, 167, 69, 0.12)" : "rgba(200, 35, 51, 0.12)"};
  border-left: 5px solid ${({ correct }) =>
        correct ? "#28a745" : "#c82333"};
  margin-bottom: 12px;
`;

const Explanation = styled.div`
  background-color: #eef2ff;
  padding: 12px 15px;
  border-radius: 8px;
  margin-top: 10px;
  font-size: 15px;
  border-left: 4px solid #557cff;
`;

const BackButton = styled.button`
  background-color: #337eff;
  color: white;
  border: none;
  padding: 12px 22px;
  font-size: 16px;
  border-radius: 8px;
  cursor: pointer;
  margin-top: 30px;
  display: block;
  margin-left: auto;
  margin-right: auto;

  &:hover {
    background-color: #2868d6;
  }
`;


export default function ResultadoQuiz() {
    const location = useLocation();
    const navigate = useNavigate();
    const { quiz_id } = location.state || {};

    const [userAnswers, setUserAnswers] = useState([]);
    const [correctAnswers, setCorrectAnswers] = useState([]);
    const [loading, setLoading] = useState(true);

    // Buscar respostas do aluno
    useEffect(() => {
        if (!quiz_id) return;

        const fetchUserAnswers = async () => {
            const url = `http://localhost:8000/api/quizzes/${quiz_id}/respostas-ultimo-quiz/`;

            try {
                const response = await fetch(url, { credentials: "include" });
                const data = await response.json();
                setUserAnswers(data);
                console.log(data);
            } catch (err) {
                console.error("Erro ao buscar respostas do aluno:", err);
            }
        };

        fetchUserAnswers();
    }, [quiz_id]);

    // Buscar gabarito
    useEffect(() => {
        if (!quiz_id) return;

        const fetchCorrectAnswers = async () => {
            const url = `http://localhost:8000/api/quizzes/${quiz_id}/questoes/respostas-corretas/`;

            try {
                const response = await fetch(url, { credentials: "include" });
                const data = await response.json();
                setCorrectAnswers(data);
            } catch (err) {
                console.error("Erro ao buscar gabarito:", err);
            } finally {
                setLoading(false);
            }
        };

        fetchCorrectAnswers();
    }, [quiz_id]);

    if (loading) return <p>Carregando resultado...</p>;

    const handleBack = () => navigate(`/quiz-info/${quiz_id}/`);

    return (
        <Container>
            <ResultBox>
                <Title>Resultado do Quiz</Title>

                {correctAnswers.map((q) => {
                    const userAnswerObj = userAnswers.find(a => a.questao === q.id);
                    const userAlt = userAnswerObj?.alternativa;
                    const isCorrect = userAlt === q.resposta_correta;

                    const alternativaTexto =
                        q.alternativas.find(a => a.id === userAlt)?.texto || "Não respondida";

                    const corretaTexto =
                        q.alternativas.find(a => a.id === q.resposta_correta)?.texto;

                    return (
                        <AnswerItem key={q.id}>
                            <QuestionText>{q.descricao}</QuestionText>

                            <UserAnswer correct={isCorrect}>
                                <strong>Sua resposta:</strong> {alternativaTexto}
                                <br />
                                {isCorrect ? (
                                    <span>✅ Resposta correta!</span>
                                ) : (
                                    <span>❌ Correta: {corretaTexto}</span>
                                )}
                            </UserAnswer>

                            <Explanation>
                                <strong>Explicação:</strong> {q.explicacao}
                            </Explanation>
                        </AnswerItem>
                    );
                })}

                <BackButton onClick={handleBack}>Voltar ao início</BackButton>
            </ResultBox>
        </Container>
    );
}
