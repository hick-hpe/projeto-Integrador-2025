import styled from "styled-components";
import { FaFilePdf } from "react-icons/fa";
import Sidebar from "../../components/Sidebar";
import { useEffect, useState } from "react";

const Container = styled.div`
  display: flex;
  height: 100vh;
  width: 100%;
  overflow: hidden;
  background-color: #eef1f5;
  font-family: Arial, sans-serif;
`;

const Content = styled.div`
  flex: 1;
  padding: 40px;
  overflow-y: auto;
  height: 100vh;
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

  const [username, setUsername] = useState("");
  const [certificados, setCertificados] = useState([]);

  // =======================
  // Buscar usuário logado
  // =======================
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
        } else {
          console.error("Erro ao obter dados do usuário.");
        }
      } catch (err) {
        console.error("Erro na requisição:", err);
      }
    };

    fetchUserData();
  }, []);

  // ===========================
  // Buscar certificados do aluno
  // ===========================
  useEffect(() => {
    const fetchCertificados = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/certificados/", {
          method: "GET",
          credentials: "include",
        });

        if (response.ok) {
          const data = await response.json();
          setCertificados(data);
        } else {
          console.error("Erro ao buscar certificados.");
        }
      } catch (err) {
        console.error("Erro na requisição:", err);
      }
    };

    fetchCertificados();
  }, []);

  // baixar certificado
  const downloadCertificado = async (codigo) => {
    try {
      const URL = `http://localhost:8000/api/certificados/${codigo}/download/`;

      const response = await fetch(URL, {
        credentials: "include" // IMPORTANTE se estiver usando cookies/CSRF/autenticação
      });

      if (!response.ok) {
        throw new Error("Erro ao baixar certificado");
      }

      // transforma em blob (arquivo binário)
      const blob = await response.blob();

      // cria URL temporária
      const url = window.URL.createObjectURL(blob);

      // cria elemento <a> invisível
      const a = document.createElement("a");
      a.href = url;

      // nome sugerido no FileResponse será respeitado se usar browser moderno
      a.download = `certificado_${codigo}.pdf`;

      document.body.appendChild(a);
      a.click();   // força o download
      a.remove();

      // limpa URL temporária
      window.URL.revokeObjectURL(url);

    } catch (error) {
      console.error(error);
    }
  };

  return (
    <Container>
      <Sidebar />

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
            {
              certificados.length == 0 ?
                <TableRow>
                  <TableCell>Você ainda não conquistou nenhum certificado.</TableCell>
                </TableRow>
                : certificados.map((cert) => (
                  <TableRow key={cert.codigo}>
                    <TableCell>{cert.codigo}</TableCell>
                    <TableCell>{cert.disciplina}</TableCell>
                    <TableCell>{cert.data_emissao}</TableCell>
                    <TableCell>
                      <PdfButton onClick={() => downloadCertificado(cert.codigo)}>
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
