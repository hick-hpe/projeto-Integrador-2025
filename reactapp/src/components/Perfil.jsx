import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button, Form, Card, Container, Row, Col, Alert, Spinner } from "react-bootstrap";
import { FaRedo, FaSignOutAlt, FaCheckCircle, FaTimesCircle } from "react-icons/fa";

const Perfil = () => {
  const NIVEL = 1;
  const API_URL = `https://potential-memory-j6px6qq4jpw3pjg6-8000.app.github.dev/api/quizzes/${NIVEL}/questoes/`;
  const AUTH_URL = "https://potential-memory-j6px6qq4jpw3pjg6-8000.app.github.dev/auth/";
  const URL_GET_USER = `${AUTH_URL}teste-autenticacao/`;
  const URL_LOGOUT = `${AUTH_URL}logout/`;

  const [usuario, setUsuario] = useState("");
  const [questoes, setQuestoes] = useState([]);
  const [questaoAtual, setQuestaoAtual] = useState(0);
  const [respostas, setRespostas] = useState({});
  const [resultados, setResultados] = useState([]);
  const [loadingResultados, setLoadingResultados] = useState(false);

  const navigate = useNavigate();

  useEffect(() => {
    fetch(URL_GET_USER, { credentials: "include" })
      .then((res) => {
        if (res.status === 401) navigate("/");
        return res.json();
      })
      .then((data) => setUsuario(data.user))
      .catch((err) => console.error("Erro ao autenticar:", err));
  }, []);

  useEffect(() => {
    fetch(API_URL, { credentials: "include" })
      .then((res) => res.json())
      .then((data) => {
        setQuestoes(data);
      })
      .catch((err) => console.error("Erro ao carregar questões:", err));
  }, []);

  const questao = questoes[questaoAtual];

  const handleResposta = (questaoId, alternativaId) => {
    setRespostas((prev) => ({
      ...prev,
      [questaoId]: alternativaId,
    }));
  };

  const irParaAnterior = () => {
    if (questaoAtual > 0) setQuestaoAtual(questaoAtual - 1);
  };

  const irParaProxima = () => {
    if (questaoAtual < questoes.length - 1) {
      setQuestaoAtual(questaoAtual + 1);
    } else {
      buscarResultados();
    }
  };

  const buscarResultados = async () => {
    setLoadingResultados(true);
    const resultadosFinais = [];

    for (const questao of questoes) {
      const respostaId = respostas[questao.id];
      if (!respostaId) continue;

      try {
        const res = await fetch(`http://https://potential-memory-j6px6qq4jpw3pjg6-8000.app.github.dev/api/quizzes/${NIVEL}/questoes/${questao.id}/resposta/`, {
          credentials: "include",
        });
        const data = await res.json();
        resultadosFinais.push({
          questao: data.detail.questao,
          respostaMarcada: questao.alternativas.find((alt) => alt.id === respostaId)?.texto || "Não respondida",
          respostaCorreta: data.detail.alternativa,
          explicacao: data.detail.explicacao,
        });
      } catch (error) {
        console.error("Erro ao buscar resultado:", error);
      }
    }

    setResultados(resultadosFinais);
    setLoadingResultados(false);
  };

  const makeLogout = async () => {
    try {
      const response = await fetch(URL_LOGOUT, {
        method: "POST",
        credentials: "include",
      });

      const data = await response.json();

      if (response.ok) {
        alert("Logout feito com sucesso!");
        navigate("/");
      } else {
        alert("Erro ao sair: " + (data.detail || "Erro desconhecido"));
      }
    } catch (error) {
      console.error("Erro na requisição:", error);
      alert("Erro de rede ou resposta inválida.");
    }
  };

  return (
    <Container className="my-4">
      <h1 className="text-center">Quiz de Desenvolvimento Web II</h1>
      <p>Bem vindo, <strong>{usuario.toUpperCase()}</strong></p>

      {loadingResultados ? (
        <div className="text-center mt-5">
          <Spinner animation="border" /> Carregando resultados...
        </div>
      ) : resultados.length > 0 ? (
        <>
          <h3>
            <FaCheckCircle className="text-success me-2" />
            Resultados: {
              resultados.filter(r => r.respostaMarcada === r.respostaCorreta).length
            } / {questoes.length} acertos
          </h3>
          {resultados.map((res, idx) => (
            <Card key={idx} className="mb-3">
              <Card.Body>
                <Card.Title>{idx + 1}. {res.questao}</Card.Title>
                <p><strong>Sua resposta:</strong> {res.respostaMarcada}</p>
                <p><strong>Resposta correta:</strong> {res.respostaCorreta}</p>
                <p><strong>Explicação:</strong> {res.explicacao}</p>
                <p>
                  <strong>Status:</strong>{" "}
                  {res.respostaMarcada === res.respostaCorreta ? (
                    <span className="text-success">
                      <FaCheckCircle className="me-1" />Correta
                    </span>
                  ) : (
                    <span className="text-danger">
                      <FaTimesCircle className="me-1" />Errada
                    </span>
                  )}
                </p>
              </Card.Body>
            </Card>
          ))}
        </>
      ) : questao ? (
        <Card className="mb-3">
          <Card.Body>
            <Card.Title>{questaoAtual + 1}. {questao.descricao}</Card.Title>
            <Form>
              {questao.alternativas.map((alt) => (
                <Form.Check
                  type="radio"
                  id={`alt-${alt.id}`}
                  key={alt.id}
                  name={`questao-${questao.id}`}
                  label={alt.texto}
                  checked={respostas[questao.id] === alt.id}
                  onChange={() => handleResposta(questao.id, alt.id)}
                />
              ))}
            </Form>
          </Card.Body>
        </Card>
      ) : (
        <Alert variant="info">Carregando questão...</Alert>
      )}

      {resultados.length === 0 && (
        <Row className="mt-3">
          <Col>
            <Button
              variant="secondary"
              onClick={irParaAnterior}
              disabled={questaoAtual === 0}
            >
              Anterior
            </Button>
          </Col>
          <Col className="text-end">
            <Button
              variant="primary"
              onClick={irParaProxima}
              disabled={!respostas[questao?.id]}
            >
              {questaoAtual === questoes.length - 1 ? "Finalizar" : "Próxima"}
            </Button>
          </Col>
        </Row>
      )}
      <div className="d-flex justify-content-between mt-4">
        <Button variant="success" onClick={() => location.reload()}>
          <FaRedo className="me-2" /> Recomeçar
        </Button>
        <Button variant="danger" onClick={makeLogout}>
          <FaSignOutAlt className="me-2" /> Logout
        </Button>
      </div>
    </Container>
  );
};

export default Perfil;
