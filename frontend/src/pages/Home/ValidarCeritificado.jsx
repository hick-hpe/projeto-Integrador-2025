import styled from "styled-components";
import Sidebar from "../../components/Sidebar";
import { useState } from "react";

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

const Title = styled.h1`
    color: #0062cc;
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  max-width: 400px;
  margin-top: 20px;
  gap: 15px;
`;

const Input = styled.input`
  padding: 12px;
  border-radius: 6px;
  border: 1px solid #ccc;
  font-size: 16px;
`;

const Button = styled.button`
  padding: 12px;
  border-radius: 6px;
  font-size: 16px;
  background-color: #007bff;
  border: none;
  color: white;
  cursor: pointer;
  transition: 0.2s;

  &:hover {
    background-color: #0062cc;
  }
`;

const Message = styled.div`
  margin-top: 20px;
  padding: 15px;
  border-radius: 6px;
  font-size: 16px;
  font-weight: bold;
  color: ${(props) => (props.valido ? "#0b7a0b" : "#b30000")};
  background-color: ${(props) => (props.valido ? "#c9f7c9" : "#ffd2d2")};
  border: 1px solid ${(props) => (props.valido ? "#6ed96e" : "#ff8c8c")};
`;

export default function ValidarCeritificado() {
  const [codigo, setCodigo] = useState("");
  const [matricula, setMatricula] = useState("");
  const [resultado, setResultado] = useState(null);
  const [loading, setLoading] = useState(false);

  const validarCertificado = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResultado(null);

    try {
      const response = await fetch("http://localhost:8000/api/certificados/validar-certificado/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ codigo, matricula }),
      });

      const data = await response.json();
      setResultado(data.valido);
    } catch (error) {
      setResultado(false);
    }

    setLoading(false);
  };

  return (
    <Container>
      <Sidebar />

      <Content>
        <Title>Validar certificado</Title>

        <Form onSubmit={validarCertificado}>
          <Input
            type="text"
            placeholder="Código do certificado"
            value={codigo}
            onChange={(e) => setCodigo(e.target.value)}
          />

          <Input
            type="text"
            placeholder="Matrícula do aluno"
            value={matricula}
            onChange={(e) => setMatricula(e.target.value)}
          />

          <Button type="submit" disabled={loading}>
            {loading ? "Validando..." : "Validar"}
          </Button>
        </Form>

        {resultado !== null && (
          <Message valido={resultado}>
            {resultado ? "✔ Certificado válido!" : "✖ Certificado inválido!"}
          </Message>
        )}
      </Content>
    </Container>
  );
}
