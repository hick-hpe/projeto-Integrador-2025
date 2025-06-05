import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const NIVEL = 1;
const BASE_URL = "http://localhost:8000";
const API_URL = `${BASE_URL}/api/quizzes/${NIVEL}/questoes/`;
const AUTH_URL = `${BASE_URL}/auth`;
const URL_GET_USER = `${AUTH_URL}/teste-autenticacao/`;
const URL_LOGOUT = `${AUTH_URL}/logout/`;

const Perfil = () => {
  const [usuario, setUsuario] = useState("");
  const [questoes, setQuestoes] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUsuario = async () => {
      try {
        const response = await fetch(URL_GET_USER, { credentials: "include" });

        if (response.status === 401) {
          alert("Você não está autenticado!");
          navigate("/");
          return;
        }

        const data = await response.json();
        console.log("Usuário autenticado:", data);
        setUsuario(data.user || "Desconhecido");
      } catch (err) {
        console.error("Erro ao autenticar:", err);
      }
    };

    fetchUsuario();
  }, [navigate]);

  useEffect(() => {
    const fetchQuestoes = async () => {
      try {
        const res = await fetch(API_URL, { credentials: "include" });
        const data = await res.json();
        console.log("Questões:", data);
        setQuestoes(data);
      } catch (err) {
        console.error("Erro ao carregar questões:", err);
      }
    };

    fetchQuestoes();
  }, []);

  const doLogout = async () => {
    try {
      const response = await fetch(URL_LOGOUT, {
        method: "POST",
        credentials: "include",
      });

      const data = await response.json();
      console.log("Logout:", data);

      if (response.ok) {
        alert("Logout feito com sucesso!");
        navigate("/");
      } else {
        alert("Erro ao fazer logout: " + (data.detail || "Erro desconhecido"));
      }
    } catch (error) {
      console.error("Erro na requisição de logout:", error);
      alert("Erro de rede ou resposta inválida.");
    }
  };

  return (
    <div>
      <h1>Quiz de Desenvolvimento Web II</h1>
      <div><strong>Usuário:</strong> {usuario}</div>

      <div>
        {questoes.map((questao, index) => (
          <div key={questao.id}>
            <p><strong>{index + 1}. {questao.descricao}</strong></p>
            {questao.alternativas.map((alt) => (
              <div key={alt.id}>
                <label>
                  <input type="radio" name={`questao-${questao.id}`} />
                  {alt.texto}
                </label>
              </div>
            ))}
          </div>
        ))}
      </div>

      <button onClick={doLogout}>Logout</button>
    </div>
  );
};

export default Perfil;
