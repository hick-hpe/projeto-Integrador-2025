import styled from "styled-components";
import Sidebar from "../../components/Sidebar";
import { use, useEffect, useState } from "react";
import {
    BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid,
    PieChart, Pie, Cell, Legend
} from "recharts";

// ------------------------------
// STYLES
// ------------------------------

const Container = styled.div`
  display: flex;
  height: 100vh;
  width: 100%;
  background-color: #eef1f5;
  font-family: Arial, sans-serif;
`;

const Content = styled.div`
  flex: 1;
  padding: 40px;
  overflow-y: auto;
  position: relative;
`;

const LogoutButton = styled.button`
  position: absolute;
  top: 20px;
  right: 30px;
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  font-size: 14px;
  &:hover {
    background-color: #c82333;
  }
`;

const Title = styled.h2`
  color: #007bff;
`;

const SectionTitle = styled.h3`
  margin-top: 35px;
  color: #444;
`;

const CardsRow = styled.div`
  display: flex;
  gap: 20px;
  margin: 25px 0;
  flex-wrap: wrap;
`;

const Card = styled.div`
  flex: 1;
  min-width: 200px;
  background-color: white;
  border-radius: 12px;
  padding: 18px;
  border-left: 5px solid #00cc66;
  box-shadow: 0 3px 7px rgba(0,0,0,0.1);
  text-align: center;

  h3 {
    margin: 10px 0 0;
    font-size: 26px;
    color: #333;
  }
`;

const ChartsArea = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 30px;
  margin-top: 20px;
`;

const ChartBox = styled.div`
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 3px 7px rgba(0,0,0,0.1);
`;

const EmblemasRow = styled.div`
  display: flex;
  gap: 20px;
  margin-top: 20px;
`;

const EmblemaCard = styled.div`
  flex: 1;
  max-width: 180px;
  background-color: #fff;
  border-radius: 10px;
  padding: 15px;
  text-align: center;
  border-top: 4px solid #ffc107;
  box-shadow: 0 3px 7px rgba(0,0,0,0.08);
`;

const LogoImg = styled.img`
  width: 60px;
  height: 60px;
  object-fit: contain;
  margin-bottom: 10px;
`;

// ------------------------------
// COMPONENTE PRINCIPAL
// ------------------------------
export default function Dashboard() {
    const [username, setUsername] = useState("");
    const [emblemasConquistados, setEmblemasConquistados] = useState([]);
    const [tentativas, setTentativas] = useState([]);
    const [barData, setBarData] = useState([]);
    const [pieData, setPieData] = useState([]);
    const [numQuizzesRealizados, setNumQuizzesRealizados] = useState(0);
    const [numCertificados, setNumCertificados] = useState(0);

    // autenticacao
    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const response = await fetch("http://localhost:8000/auth/me/", {
                    method: "GET",
                    credentials: "include",
                });

                if (response.status === 401) {
                    window.location.href = "/";
                    return;
                }

                if (response.ok) {
                    const data = await response.json();
                    setUsername(data.username);
                }
            } catch (error) {
                console.error("Erro na requisição auth:", error);
            }
        };

        fetchUserData();
    }, []);

    // emblemas
    useEffect(() => {
        const fetchEmblemas = async () => {
            try {
                const res = await fetch("http://localhost:8000/api/emblemas/aluno/", {
                    credentials: "include",
                });
                if (res.ok) {
                    const data = await res.json();
                    setEmblemasConquistados(data);
                }
            } catch (err) {
                console.error("Erro ao buscar emblemas:", err);
            }
        };

        fetchEmblemas();
    }, []);

    // logout
    const handleLogout = async () => {
        try {
            const response = await fetch("http://localhost:8000/auth/logout/", {
                method: "POST",
                credentials: "include",
            });

            if (response.ok) window.location.href = "/";
        } catch (error) {
            console.error("Erro na requisição:", error);
        }
    };

    // certificados
    useEffect(() => {
        const fetchCertificados = async () => {
            try {
                const res = await fetch("http://localhost:8000/api/certificados/", {
                    credentials: "include",
                });
                if (res.ok) {
                    const data = await res.json();
                    setNumCertificados(data.length);
                }
            } catch (err) {
                console.error("Erro ao buscar emblemas:", err);
            }
        };

        fetchCertificados();
    }, []);

    // tentativas
    useEffect(() => {
        const fetchTentativas = async () => {
            try {
                const response = await fetch("http://localhost:8000/api/tentativas/", {
                    credentials: "include",
                });

                if (!response.ok) {
                    console.error("Erro ao buscar tentativas:", response.status);
                    return;
                }

                const data = await response.json();
                setTentativas(data);
            } catch (error) {
                console.error("Erro na requisição tentativas:", error);
            }
        };

        fetchTentativas();
    }, []);

    // processar tentativas para os graficos
    useEffect(() => {
        if (tentativas.length === 0) return;

        const disciplinas = {};
        const niveis = {};
        let numQuizzesRealizadosTemp = 0;

        tentativas.forEach((t) => {
            numQuizzesRealizadosTemp++;

            // --- DISCIPLINAS PARA BARCHART ---
            if (!disciplinas[t.disciplina]) {
                disciplinas[t.disciplina] = { disciplina: t.disciplina, quizzes: 0, aprovados: 0 };
            }

            disciplinas[t.disciplina].quizzes += 1;
            if (t.aprovado) disciplinas[t.disciplina].aprovados += 1;

            // --- NÍVEIS PARA PIE CHART ---
            if (!niveis[t.nivel]) {
                niveis[t.nivel] = 1;
            } else {
                niveis[t.nivel] += 1;
            }
        });

        // num quizzes
        setNumQuizzesRealizados(numQuizzesRealizadosTemp);

        // Converte objetos -> arrays
        setBarData(Object.values(disciplinas));

        setPieData(
            Object.entries(niveis).map(([name, value]) => ({
                name,
                value,
            }))
        );
    }, [tentativas]);

    const pieColors = ["#007bff", "#28a745", "#ffc107", "#dc3545"];

    // legendas dos graficos
    const CustomLegend = () => {
        return (
            <div style={{ display: "flex", gap: "20px", padding: "10px 0" }}>
                <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
                    <span style={{ width: 12, height: 12, background: "#007bff" }} />
                    <span>Total de Quizzes</span>
                </div>

                <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
                    <span style={{ width: 12, height: 12, background: "#28a745" }} />
                    <span>Quizzes Aprovados (≥ 70%)</span>
                </div>
            </div>
        );
    };

    const PieLegend = ({ data, colors }) => {
        return (
            <div style={{
                display: "flex",
                flexDirection: "column",
                gap: "6px",
                padding: "10px 0 0 0"
            }}>
                {data.map((item, i) => (
                    <div key={i} style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                        <span style={{
                            width: 12,
                            height: 12,
                            background: colors[i],
                            borderRadius: "50%"
                        }} />
                        <span>{item.name}</span>
                    </div>
                ))}
            </div>
        );
    };

    return (
        <Container>
            <Sidebar />

            <Content>
                <LogoutButton onClick={handleLogout}>Logout</LogoutButton>

                <Title>DASHBOARD</Title>
                <h4>Bem vindo, {username}</h4>

                {/* CARDS */}
                <CardsRow>
                    <Card>
                        <p>Quizzes Realizados</p>
                        <h3>{numQuizzesRealizados}</h3>
                    </Card>

                    <Card>
                        <p>Certificados Emitidos</p>
                        <h3>{numCertificados}</h3>
                    </Card>

                    <Card>
                        <p>Emblemas Conquistados</p>
                        <h3>{emblemasConquistados.length}</h3>
                    </Card>
                </CardsRow>

                {/* GRÁFICOS */}
                <SectionTitle>Estatísticas</SectionTitle>

                <ChartsArea>
                    {/* BAR CHART */}
                    <ChartBox>
                        <h4>Quizzes x Acertos na Por Disciplina</h4>
                        <BarChart width={450} height={300} data={barData}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="disciplina" />
                            <YAxis />
                            <Tooltip />

                            <Legend content={<CustomLegend />} />

                            <Bar dataKey="quizzes" fill="#007bff" />
                            <Bar dataKey="aprovados" fill="#28a745" />
                        </BarChart>
                    </ChartBox>

                    {/* PIE CHART */}
                    <ChartBox>
                        <h4>Quizzes por Tema</h4>

                        <PieChart width={380} height={300}>
                            <Pie
                                data={pieData}
                                cx={180}
                                cy={130}
                                outerRadius={110}
                                dataKey="value"
                                label
                            >
                                {pieData.map((_, i) => (
                                    <Cell key={i} fill={pieColors[i]} />
                                ))}
                            </Pie>

                            <Tooltip />

                            {/* LEGENDA CUSTOMIZADA */}
                            <Legend
                                content={<PieLegend data={pieData} colors={pieColors} />}
                                verticalAlign="bottom"
                            />
                        </PieChart>
                    </ChartBox>
                </ChartsArea>

                {/* EMBLEMAS */}
                <SectionTitle>Seus Emblemas</SectionTitle>
                <EmblemasRow>
                    {emblemasConquistados.slice(0, 3).map((item) => (
                        <EmblemaCard key={item.id}>
                            {item.emblema.logo ? (
                                <LogoImg src={`http://localhost:8000${item.emblema.logo}`} />
                            ) : (
                                <span style={{ fontSize: 40 }}>🏅</span>
                            )}
                            <p><strong>{item.emblema.nome}</strong></p>
                        </EmblemaCard>
                    ))}

                    {emblemasConquistados.length === 0 && (
                        <p>Nenhum emblema conquistado ainda.</p>
                    )}
                </EmblemasRow>

            </Content>
        </Container>
    );
}
