import styled from "styled-components";
import { FaCamera } from "react-icons/fa";
import Sidebar from "../../components/Sidebar";
import { useEffect, useState } from "react";
import Modal from "../../components/Modal";

const Container = styled.div`
  display: flex;
  height: 100vh;
  width: 100%;
  background-color: #eef1f5;
  font-family: Arial, sans-serif;
  overflow: hidden;

  /* Mobile: sidebar ocupa a tela quando ativa, então o content precisa ficar atrás */
  @media (max-width: 768px) {
    position: relative;
  }
`;

const Content = styled.div`
  flex: 1;
  padding: 40px;
  overflow-y: auto;
  height: 100vh;

  /* Mobile: diminuir paddings */
  @media (max-width: 768px) {
    padding: 20px 15px;
  }
`;

const Title = styled.h1`
  color: #007bff;
  margin-bottom: 20px;

  @media (max-width: 768px) {
    font-size: 22px;
    text-align: center;
  }
`;

const Card = styled.div`
  background: white;
  padding: 30px;
  padding-bottom: 0px;
  max-width: 650px;
  margin: auto;
  border-radius: 15px;
  box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
  margin-bottom: 80px;

  @media (max-width: 768px) {
    padding: 20px;
    margin-bottom: 40px;
  }
`;

const ProfileSection = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
`;

const ProfileImageWrapper = styled.div`
  position: relative;
  width: 130px;
  height: 130px;
  border-radius: 50%;
  overflow: hidden;
  margin-bottom: 10px;
  box-shadow: 0px 3px 10px rgba(0,0,0,0.15);

  @media (max-width: 768px) {
    width: 110px;
    height: 110px;
  }
`;

const ProfileImage = styled.img`
  width: 100%;
  height: 100%;
`;

const CameraIcon = styled(FaCamera)`
  position: absolute;
  bottom: 8px;
  right: 8px;
  background-color: #007bff;
  color: white;
  border-radius: 50%;
  padding: 6px;
  cursor: pointer;
  font-size: 18px;
  transition: 0.2s;

  &:hover {
    background-color: #005bb5;
  }
`;

const InfoBox = styled.div`
  display: flex;
  gap: 25px;
  margin: 20px 0;

  @media (max-width: 768px) {
    flex-direction: column;
    width: 100%;
    gap: 15px;
  }
`;

const StatBox = styled.div`
  background: #f9fafb;
  padding: 15px 25px;
  border-radius: 10px;
  border-left: 4px solid #007bff;
  text-align: center;
  font-weight: bold;
  flex: 1;

  @media (max-width: 768px) {
    padding: 12px;
  }
`;

const StatNumber = styled.div`
  margin-top: 3px;
  font-size: 20px;
  color: #333;
`;

const FormSection = styled.div`
  margin-top: 30px;
  padding: 30px;
  display: flex;
  flex-direction: column;
  gap: 22px;

  @media (max-width: 768px) {
    padding: 20px 10px;
  }
`;

const Label = styled.label`
  font-weight: bold;
  margin-bottom: 5px;
`;

const Input = styled.input`
  padding: 10px;
  width: 100%;
  border-radius: 8px;
  border: 1px solid #ccc;
  transition: 0.2s;

  &:focus {
    border-color: #007bff;
    box-shadow: 0 0 4px rgba(0,123,255,0.4);
  }
`;

const SaveButton = styled.button`
  background-color: #28a745;
  color: white;
  padding: 10px 14px;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  margin-top: 8px;

  &:hover {
    background-color: #1d7e34;
  }
`;

const DeleteButton = styled.button`
  background-color: #dc3545;
  color: white;
  padding: 12px 16px;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  margin-top: 35px;
  align-self: center;
  width: 100%;

  &:hover {
    background-color: #b52a36;
  }
`;

export default function Perfil() {

  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [open, setOpen] = useState(false);

  // autenticacao
  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const r = await fetch("http://localhost:8000/auth/me/", {
          method: "GET",
          credentials: "include",
        });

        if (r.status === 401) {
          window.location.href = "/";
          return;
        }

        if (r.ok) {
          const data = await r.json();
          setUsername(data.username);
          setEmail(data.email);
        }
      } catch (error) {
        console.error("Erro:", error);
      }
    };

    fetchUserData();
  }, []);

  // atualizar nome, email e/ou senha
  const handleSave = async (field) => {
    const payload = {};

    if (field === "username") payload.username = username;
    if (field === "email") payload.email = email;
    if (field === "password") payload.password = password;

    try {
      const res = await fetch("http://localhost:8000/auth/conta/", {
        method: "PATCH",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (res.ok) {
        alert("Atualizado com sucesso!");
        if (field === "password") setPassword(""); // limpa senha
      } else {
        const errData = await res.json();
        console.error(errData);
        alert("Erro ao atualizar");
      }
    } catch (err) {
      console.error(err);
    }
  };

  // excluir conta
  const handleDelete = async () => {
    try {
      const res = await fetch("http://localhost:8000/auth/conta/", {
        method: "DELETE",
        credentials: "include",
      });

      if (res.ok) {
        alert("Conta excluída com sucesso!");
        window.location.href = "/"; // redireciona para login ou home
      }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <Container>
      <Sidebar />

      {/* modal para exclusão de conta */}
      <Modal
        visible={open}
        onClose={() => setOpen(false)}
        funcaoParaBotao={handleDelete}
      >
        <h2>ATENÇÃO!</h2>
        <p>Você está prestes a excluir sua conta permanentemente. Esta ação não pode ser desfeita.</p>
        <p>Todos os seus dados, quizzes e emblemas serão perdidos. Tem certeza que deseja continuar?</p>
      </Modal>

      <Content>
        <Title>Meu Perfil</Title>

        <Card>
          <ProfileSection>
            <ProfileImageWrapper>
              <ProfileImage src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" />
              <CameraIcon />
            </ProfileImageWrapper>

            <h2>{username}</h2>

            {/* <InfoBox>
              <StatBox>
                Pontuação Total
                <StatNumber>250</StatNumber>
              </StatBox>

              <StatBox>
                Certificados
                <StatNumber>2</StatNumber>
              </StatBox>
            </InfoBox> */}
          </ProfileSection>

          <FormSection>
            <div>
              <Label>Alterar nome</Label>
              <Input
                placeholder="Novo nome"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
              <SaveButton onClick={() => handleSave("username")}>Salvar</SaveButton>
            </div>

            <div>
              <Label>Alterar email</Label>
              <Input
                placeholder="Novo email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
              <SaveButton onClick={() => handleSave("email")}>Salvar</SaveButton>
            </div>

            <div>
              <Label>Alterar senha</Label>
              <Input
                type="password"
                placeholder="Nova senha"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <SaveButton onClick={() => handleSave("password")}>Salvar</SaveButton>
            </div>

            <DeleteButton onClick={() => setOpen(true)}>Excluir conta</DeleteButton>
          </FormSection>
        </Card>
      </Content>
    </Container>
  );
}
