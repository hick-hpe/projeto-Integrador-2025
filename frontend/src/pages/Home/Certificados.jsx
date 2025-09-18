import styled from "styled-components";
import { FaFilePdf } from "react-icons/fa";
import { useNavigate } from "react-router-dom";

const certificados = [
  {
    codigo: "ABCDE12345",
    curso: "Introdução ao Django",
    data: "12/06/2025",
  },
  {
    codigo: "FGHIJ67890",
    curso: "Docker",
    data: "12/06/2025",
  },
];

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

const Table = styled.table`
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  border-radius: 10px;
  overflow: hidden;
`;

const TableHead = styled.thead`
  background-color: #007bff;
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

const PdfButton = styled.button`
  background: none;
  border: none;
  cursor: pointer;
  color: red;
  font-size: 1.2em;
`;

export default function Meus_Certificados() {
  const navigate = useNavigate();

  return (
    <Container>
      <Sidebar>
        <SidebarTitle>DevQuiz Aluno</SidebarTitle>
        <SidebarButton onClick={() => navigate("/home/Tela")}>Home</SidebarButton>
        <SidebarButton onClick={() => navigate("/home/Quizzes")}>Quizzes</SidebarButton>
        <SidebarButton active>Certificados</SidebarButton>
        <SidebarButton onClick={() => navigate("/home/Ranking")}>Ranking</SidebarButton>
        <SidebarButton onClick={() => navigate("/home/Perfil")}>Perfil</SidebarButton>
      </Sidebar>
      <Content>
        <Title>Meus Certificados</Title>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Código</TableCell>
              <TableCell>Categoria/Curso</TableCell>
              <TableCell>Data de Emissão</TableCell>
              <TableCell>Ver</TableCell>
            </TableRow>
          </TableHead>
          <tbody>
            {certificados.map((cert) => (
              <TableRow key={cert.codigo}>
                <TableCell>{cert.codigo}</TableCell>
                <TableCell>{cert.curso}</TableCell>
                <TableCell>{cert.data}</TableCell>
                <TableCell>
                  <PdfButton>
                    <FaFilePdf />
                  </PdfButton>
                </TableCell>
              </TableRow>
            ))}
          </tbody>
        </Table>
      </Content>
    </Container>
  );
}
