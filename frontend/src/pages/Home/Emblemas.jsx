import styled from "styled-components";
import Sidebar from "../../components/Sidebar";
import { useEffect, useState } from "react";
import { FaMedal } from "react-icons/fa";

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
  margin-bottom: 20px;
`;

const Grid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
  margin: 60px 0;
`;

const Card = styled.div`
  background: white;
  padding: 20px;
  border-radius: 12px;
  text-align: center;
  border-top: 4px solid ${(p) => (p.conquistado ? "#28a745" : "#ccc")};
  box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.1);
`;

const MedalIcon = styled(FaMedal)`
  font-size: 2.5em;
  color: ${(props) => (props.active ? "#f5c518" : "#c0c0c0")};
  margin-bottom: 10px;
`;

const LogoImg = styled.img`
  width: 70px;
  height: 70px;
  object-fit: contain;
  margin-bottom: 10px;
`;

const Name = styled.h4`
  margin: 10px 0 5px 0;
`;

const Desc = styled.p`
  font-size: 0.9em;
  color: #555;
`;

const Status = styled.span`
  margin-top: 10px;
  display: inline-block;
  font-weight: bold;
  color: ${(p) => (p.ok ? "#28a745" : "#999")};
`;

export default function Emblemas() {
  const [emblemas, setEmblemas] = useState([]);
  const [conquistados, setConquistados] = useState([]);

  // Buscar TODOS os emblemas
  useEffect(() => {
    fetch("http://localhost:8000/api/emblemas/", {
      credentials: "include",
    })
      .then((res) => res.json())
      .then(setEmblemas)
      .catch((err) => console.error("Erro:", err));
  }, []);

  // Buscar emblemas conquistados pelo aluno
  useEffect(() => {
    fetch("http://localhost:8000/api/emblemas/aluno/", {
      credentials: "include",
    })
      .then((res) => res.json())
      .then((data) => {
        setConquistados(data.map((e) => e.emblema.id)); // apenas ids
      })
      .catch((err) => console.error("Erro:", err));
  }, []);

  return (
    <Container>
      <Sidebar />

      <Content>
        <Title>Meus Emblemas</Title>

        <Grid>
          {emblemas.map((emb) => {
            const isActive = conquistados.includes(emb.id);

            return (
              <Card key={emb.id} conquistado={isActive}>
                {/* Mostrar logo se existir, senão o ícone */}
                {emb.logo ? (
                  <LogoImg src={`http://localhost:8000${emb.logo}`} />
                ) : (
                  <MedalIcon active={isActive} />
                )}

                <Name>{emb.nome} em {emb.disciplina}</Name>
                <Desc>{emb.descricao}</Desc>
                <Status ok={isActive}>
                  {isActive ? "Conquistado ✓" : "Pendente —"}
                </Status>
              </Card>
            );
          })}
        </Grid>
      </Content>
    </Container>
  );
}
