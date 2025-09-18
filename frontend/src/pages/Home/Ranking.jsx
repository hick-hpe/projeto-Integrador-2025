import styled from "styled-components";
import { FaFilter } from "react-icons/fa";
import { useNavigate } from "react-router-dom";


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
`;

const Title = styled.h2`
  color: #007bff;
`;

const FilterSection = styled.div`
  display: flex;
  align-items: center;
  gap: 5px;
  margin: 20px 0;
`;

const Select = styled.select`
  padding: 5px;
  border-radius: 5px;
`;

const Table = styled.table`
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

const TableHead = styled.thead`
  background-color: #007bff;
  color: white;
`;

const TableRow = styled.tr`
  background-color: ${(props) => (props.highlight ? "#a3e7e4" : "transparent")};
  &:not(:first-child) {
    border-top: 1px solid #ccc;
  }
`;

const TableCell = styled.td`
  padding: 12px;
  text-align: left;
`;

export default function Ranking_Page() {
    const navigate = useNavigate();

    const rankingData = [
        { pos: 1, name: "David Hotes", category: "Desenvolvimento Web", points: 327 },
        { pos: 2, name: "Henrique localhost", category: "Desenvolvimento Web", points: 313 },
        { pos: 3, name: "Nsaboqmmasvaiter", category: "Desenvolvimento Web", points: 200 },
        { pos: 4, name: "Nsaboqmmasvaiter", category: "Desenvolvimento Web", points: 200 },
    ];

    return (
        <Container>
            <Sidebar>
                <SidebarTitle>DevQuiz Aluno</SidebarTitle>
                <SidebarButton onClick={() => navigate("/home/Tela")}>Home</SidebarButton>
                <SidebarButton onClick={() => navigate("/home/Quizzes")}>Quizzes</SidebarButton>
                <SidebarButton onClick={() => navigate("/home/Certificados")}>Certificados</SidebarButton>
                <SidebarButton active>Ranking</SidebarButton>
                <SidebarButton onClick={() => navigate("/home/Perfil")}>Perfil</SidebarButton>
            </Sidebar>
            <Content>
                <Title>Ranking teste</Title>
                <FilterSection>
                    <span>Filtrar por:</span>
                    <FaFilter />
                    <Select>
                        <option>Pontuação</option>
                    </Select>
                </FilterSection>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Posição</TableCell>
                            <TableCell>Aluno</TableCell>
                            <TableCell>Disciplina/Categoria</TableCell>
                            <TableCell>Pontos</TableCell>
                        </TableRow>
                    </TableHead>
                    <tbody>
                        {rankingData.map((item) => (
                            <TableRow key={item.pos} highlight={item.pos === 2}>
                                <TableCell>#{item.pos}</TableCell>
                                <TableCell>{item.name}</TableCell>
                                <TableCell>{item.category}</TableCell>
                                <TableCell>{item.points}</TableCell>
                            </TableRow>
                        ))}
                    </tbody>
                </Table>
            </Content>
        </Container>
    );
}
