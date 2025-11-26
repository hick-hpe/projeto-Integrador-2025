import { useEffect, useState } from "react";
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
    const { quiz_id } = location.state || {};

    const [userAnswers, setUserAnswers] = useState([]);
    const [correctAnswers, setCorrectAnswers] = useState([]);
    const [loading, setLoading] = useState(true);

    // Buscar respostas do aluno
    useEffect(() => {
        if (!quiz_id) return;

        const fetchUserAnswers = async () => {
            const url = `http://localhost:8000/api/respostas-ultimo-quiz/${quiz_id}/`;

            try {
                const response = await fetch(url, { credentials: "include" });
                const data = await response.json();
                setUserAnswers(data);
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

                    const alternativaTexto = q.alternativas.find(a => a.id === userAlt)?.texto || "Não respondida";
                    const corretaTexto = q.alternativas.find(a => a.id === q.resposta_correta)?.texto;

                    return (
                        <AnswerItem key={q.id}>
                            <QuestionText>{q.descricao}</QuestionText>

                            <UserAnswer correct={isCorrect}>
                                <strong>Sua resposta:</strong> {alternativaTexto} <br />

                                {isCorrect ? (
                                    <span>✅ Correta!</span>
                                ) : (
                                    <span>❌ Correta: {corretaTexto}</span>
                                )}

                                <div>
                                    <strong>Explicação:</strong> {q.explicacao}
                                </div>
                            </UserAnswer>
                        </AnswerItem>
                    );
                })}

                <BackButton onClick={handleBack}>Voltar ao início</BackButton>
            </ResultBox>
        </Container>
    );
}
