import styled from "styled-components";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

const Container = styled.div`
  display: flex;
  height: 100vh;
  font-family: Arial, sans-serif;
`;

const Sidebar = styled.div`
  width: 200px;
  background-color: #007bff;
  color: white;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
`;

const SidebarTitle = styled.h3`
  color: white;
  margin-bottom: 30px;
`;

const SidebarButton = styled.button`
  background-color: ${(props) => (props.active ? "#e6f4ff" : "#0056b3")};
  border: ${(props) => (props.active ? "2px solid #00ccff" : "none")};
  color: ${(props) => (props.active ? "#007bff" : "white")};
  border-radius: 10px;
  padding: 10px;
  text-align: left;
  cursor: pointer;
  font-weight: bold;
  &:hover {
    background-color: #3399ff;
  }
`;

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

const Table = styled.table`
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  border-radius: 10px;
  overflow: hidden;
`;

const TableHead = styled.thead`
  background-color: #00aaff;
  color: white;
`;

const TableRow = styled.tr`
  &:nth-child(even) {
    background-color: #f0f0f0;
  }
`;

const TableCell = styled.td`
  padding: 10px;
  text-align: center;
`;

export default function Tela_inicial() {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');

  useEffect(() => {
    const buscarUsuario = async () => {
      const URL = 'http://localhost:8000/auth/teste-autenticacao/';
      
      try {
        const response = await fetch(URL, {credentials: 'include'});

        const data = await response.json();
        console.log('Dados recebidos:', data);

        if (response.ok && data.username) {
          setUsername(data.username);
        } else {
          console.warn("Resposta inesperada:", data);
        }

      } catch (error) {
        console.error('Erro ao buscar dados:', error);
      }
    };

    buscarUsuario();
  }, []);


  const handleLogout = () => {
    navigate("/");
  };

  return (
    <Container>
      <Sidebar>
        <SidebarTitle>DevQuiz Aluno</SidebarTitle>
        <SidebarButton active>Home</SidebarButton>
        <SidebarButton onClick={() => navigate("/Home/Quizzes")}>Quizzes</SidebarButton>
        <SidebarButton onClick={() => navigate("/Home/Certificados")}>Certificados</SidebarButton>
        <SidebarButton onClick={() => navigate("/home/Ranking")}>Ranking</SidebarButton>
        <SidebarButton onClick={() => navigate("/home/Perfil")}>Perfil</SidebarButton>
      </Sidebar>
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

        <SubTitle>Ranking - Top#3</SubTitle>
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
        </Table>
      </Content>
    </Container>
  );
}