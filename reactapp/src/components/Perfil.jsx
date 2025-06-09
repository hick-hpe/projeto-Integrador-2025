import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button, Form, Card, Container, Row, Col, Alert, Spinner, NavLink } from "react-bootstrap";
import { FaRedo, FaSignOutAlt, FaCheckCircle, FaTimesCircle, FaDownload } from "react-icons/fa";
import { IoMdClose } from "react-icons/io";
import _default from "react-bootstrap/esm/Accordion";

const Perfil = () => {
  const QUIZ = 1;
  const API_URL = `http://localhost:8000/api/quizzes/${QUIZ}/questoes/`;
  const URL_INICIAR_QUIZ = `http://localhost:8000/api/quizzes/${QUIZ}/iniciar/`;
  const URL_DESISTIR_QUIZ = `http://localhost:8000/api/quizzes/${QUIZ}/desistir/`;
  const URL_CONCLUIR_QUIZ = `http://localhost:8000/api/quizzes/${QUIZ}/concluir/`;
  const AUTH_URL = "http://localhost:8000/auth/";
  const URL_GET_USER = `${AUTH_URL}teste-autenticacao/`;
  const URL_LOGOUT = `${AUTH_URL}logout/`;
  const URL_DOWNLOAD_CERTIFICADO = `http://localhost:8000/certificados/download/`;

  const [usuario, setUsuario] = useState("");
  const [questoes, setQuestoes] = useState([]);
  const [questaoAtual, setQuestaoAtual] = useState(0);
  const [questaoIdAtual, setQuestaoIdAtual] = useState(0);
  const [alternativaAtual, setAlternativaAtual] = useState(0);
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
        if ('detail' in data) console.log('detail level error');
        // console.log(data)
        // setQuestoes(data.filter((d, i) => i < 2));
      })
      .catch((err) => console.error("Erro ao carregar questões:", err));
  }, []);

  useEffect(() => {
    fetch(URL_INICIAR_QUIZ, {
      credentials: "include",
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log('Iniciando...');
        console.log(data.detail);
      })
      .catch((err) => console.error("Erro ao carregar questões:", err));
  }, []);

  const questao = questoes[questaoAtual];

  const handleResposta = (questaoId, alternativaId) => {
    setRespostas((prev) => ({
      ...prev,
      [questaoId]: alternativaId,
    }));
    setQuestaoIdAtual(questaoId);
    setAlternativaAtual(alternativaId);
  };

  const irParaAnterior = () => {
    if (questaoAtual > 0) setQuestaoAtual(questaoAtual - 1);
  };

  const irParaProxima = () => {
    const URL_ENVIAR_RESPOSTA = `http://localhost:8000/api/quizzes/${QUIZ}/questoes/${questaoIdAtual}/`;
    fetch(URL_ENVIAR_RESPOSTA, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ 'alternativa_id': (alternativaAtual) }),
      credentials: "include",
    })
      .then((res) => res.json())
      .then((data) => { })
      .catch((err) => console.error("Erro ao responder a questão: ", err));
    setQuestaoAtual(questaoAtual + 1);

    if (questaoAtual == questoes.length - 1) {
      concluirQuiz();
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
        const res = await fetch(`http://localhost:8000/api/quizzes/${QUIZ}/questoes/${questao.id}/resposta/`, {
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
        console.error("Erro ao buscar resultado: ", error);
      }
    }

    setResultados(resultadosFinais);
    setLoadingResultados(false);
  };

  const downloadCertificado = async () => {
    try {
      const response = await fetch(URL_DOWNLOAD_CERTIFICADO, {
        credentials: "include",
      });

      if (!response.ok) {
        throw new Error("Erro ao baixar certificado");
      }

      // Recebe o arquivo como blob
      const blob = await response.blob();

      // Cria uma URL temporária para o blob
      const url = window.URL.createObjectURL(blob);

      // Cria um link temporário e simula o clique para baixar
      const a = document.createElement("a");
      a.href = url;
      a.download = "certificado.pdf"; // Nome sugerido para o arquivo
      document.body.appendChild(a);
      a.click();

      // Limpa o link e a URL temporária
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error("Erro ao baixar certificado: ", error);
    }
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

  const desistirQuiz = async () => {
    try {
      const response = await fetch(URL_DESISTIR_QUIZ, {
        method: "POST",
        credentials: "include",
      });

      const data = await response.json();

      if (response.ok) {
        alert(data.detail);
        navigate("/");
      } else {
        alert("Erro ao sair: " + (data.detail || "Erro desconhecido"));
      }
    } catch (error) {
      console.error("Erro na requisição:", error);
      alert("Erro de rede ou resposta inválida.");
    }
  };

  const concluirQuiz = async () => {
    try {
      const response = await fetch(URL_CONCLUIR_QUIZ, {
        method: "POST",
        credentials: "include",
      });

      const data = await response.json();

      if (response.ok) {
        console.log('quiz concluido -------------');
        console.log(data);
        // navigate("/");
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
      <p>
        Bem vindo, <strong>{usuario.toUpperCase()}</strong>
        <Button
          as="a"
          variant="link"
          className="text-primary p-0 ms-2 align-baseline"
          style={{ textDecoration: 'underline', fontWeight: 'bold' }}
          onClick={makeLogout}
        > Logout
        </Button>
      </p>

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
        <Button
          variant="success"
          onClick={() => location.reload()}
          disabled={!resultados.length}
        >
          <FaRedo className="me-2" /> Recomeçar
        </Button>
        <div
          title={
            resultados.length === 0
              ? "Responda o questionário antes"
              : ((resultados.filter(r => r.respostaMarcada === r.respostaCorreta).length) / questoes.length) < 0.7
                ? "Acerte pelo menos 70% das questões"
                : ""
          }
        >
          <Button
            disabled={resultados.length === 0 || ((resultados.filter(r => r.respostaMarcada === r.respostaCorreta).length) / questoes.length) < 0.7}
            variant="primary"
            onClick={downloadCertificado}
          >
            <FaDownload className="me-2" /> Download
          </Button>
        </div>
        <Button variant="danger" onClick={desistirQuiz}>
          <IoMdClose className="me-2" /> Desistir
        </Button>
      </div>
    </Container>
  );
};

export default Perfil;
