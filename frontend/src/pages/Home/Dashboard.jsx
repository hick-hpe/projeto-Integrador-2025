import styled from "styled-components";
import Sidebar from "../../components/Sidebar";
import { useEffect, useState } from "react";

const Content = styled.div`
  flex: 1;
  background-color: #f7f7f7;
  padding: 30px;
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

const SubTitle = styled.h4`
  margin-top: 10px;
`;

const CardsRow = styled.div`
  display: flex;
  gap: 20px;
  margin: 20px 0;
`;

const Card = styled.div`
  flex: 1;
  background-color: white;
  border-radius: 10px;
  padding: 15px;
  border-top: 4px solid #00cc66;
  text-align: center;
`;

const ChartPlaceholder = styled.div`
  background-color: lightgray;
  height: 120px;
  margin: 20px 0;
  border-radius: 10px;
`;

// const Table = styled.table`
//   width: 100%;
//   border-collapse: collapse;
//   background-color: white;
//   border-radius: 10px;
//   overflow: hidden;
// `;

// const TableHead = styled.thead`
//   background-color: #00aaff;
//   color: white;
// `;

// const TableRow = styled.tr`
//   &:nth-child(even) {
//     background-color: #f0f0f0;
//   }
// `;

// const TableCell = styled.td`
//   padding: 10px;
//   text-align: center;
// `;

const EmblemesRow = styled.div`
  display: flex;
  gap: 20px;
  margin: 20px 0;
`;

const EmblemaCard = styled.div`
  flex: 1;
  background-color: #fff;
  border-radius: 10px;
  padding: 15px;
  text-align: center;
  border-top: 4px solid #ffc107; /* cor ouro */
`;

const EmblemaIcon = styled.div`
  font-size: 40px;
  margin-bottom: 10px;
`;

const DashboardContainer = styled.div`
    display: flex;
    height: 100vh;
`;

export default function Dashboard() {

    const [username, setUsername] = useState("");

    // simulação de emblemas
    const emblemas = [
        { nome: "Matemática Mestre", icone: "🏆" },
        { nome: "Física Intermediária", icone: "🎖️" },
        { nome: "Quizzes Concluídos", icone: "🥇" },
    ];


    useEffect(() => {
        const fetchUserData = async () => {
            // verificar se ta logado
            try {
                const response = await fetch("http://localhost:8000/auth/me/", {
                    method: "GET",
                    credentials: "include", // envia os cookies
                });

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

    const handleLogout = async () => {
        try {
            await fetch("http://localhost:8000/auth/logout/", {
                method: "POST",
                credentials: "include", // envia os cookies
            });

            navigate("/");
        } catch (error) {
            console.error("Erro ao fazer logout:", error);
        }
    };

    return (
        <DashboardContainer>
            <Sidebar />

            <Content>
                <LogoutButton onClick={handleLogout}>Logout</LogoutButton>
                <Title>DASHBOARD</Title>
                <SubTitle>Bem vindo, {username}</SubTitle>
                <CardsRow>
                    <Card>
                        <p>Posição no Ranking</p>
                        <h3>#1</h3>
                    </Card>
                    <Card>
                        <p>Quizzes Realizados</p>
                        <h3>10</h3>
                    </Card>

                    <Card>
                        <h1>1123123123</h1>
                        <p>Certificados Emitidos</p>
                        <h3>4</h3>
                    </Card>
                </CardsRow>

                <SubTitle>Estatísticas</SubTitle>
                <ChartPlaceholder />

                {/* <SubTitle>Ranking - Top#3</SubTitle>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Posição</TableCell>
                            <TableCell>Aluno</TableCell>
                            <TableCell>Pontos</TableCell>
                        </TableRow>
                    </TableHead>
                    <tbody>
                        <TableRow>
                            <TableCell>#1</TableCell>
                            <TableCell>David Hotes</TableCell>
                            <TableCell>327</TableCell>
                        </TableRow>
                        <TableRow>
                            <TableCell>#2</TableCell>
                            <TableCell>Henrique localhost</TableCell>
                            <TableCell>313</TableCell>
                        </TableRow>
                        <TableRow>
                            <TableCell>#3</TableCell>
                            <TableCell>Nsboqmmnasvolter</TableCell>
                            <TableCell>200</TableCell>
                        </TableRow>
                    </tbody>
                </Table> */}

                <SubTitle>Seus Emblemas</SubTitle>
                <EmblemesRow>
                    {emblemas.map((e, i) => (
                        <EmblemaCard key={i}>
                            <EmblemaIcon>{e.icone}</EmblemaIcon>
                            <p>{e.nome}</p>
                        </EmblemaCard>
                    ))}
                </EmblemesRow>

            </Content>
        </DashboardContainer>
    );
}

