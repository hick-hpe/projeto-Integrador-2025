import styled from "styled-components";
import { useNavigate } from "react-router-dom";
import { FaCamera } from "react-icons/fa";

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
  border: ${(props) => (props.active ? "2px solid #00ff66" : "none")};
  color: ${(props) => (props.active ? "#00ff66" : "white")};
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

const ProfileSection = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
`;

const ProfileImageWrapper = styled.div`
  position: relative;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  overflow: hidden;
  margin: 10px 0;
`;

const ProfileImage = styled.img`
  width: 100%;
  height: 100%;
`;

const CameraIcon = styled(FaCamera)`
  position: absolute;
  bottom: 0;
  right: 0;
  background-color: white;
  border-radius: 50%;
  padding: 4px;
`;

const InfoBox = styled.div`
  display: flex;
  justify-content: center;
  gap: 20px;
  margin: 20px 0;
`;

const StatBox = styled.div`
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  min-width: 150px;
  text-align: center;
`;

const Points = styled.div`
  color: red;
  font-weight: bold;
`;

const Certs = styled.div`
  color: green;
  font-weight: bold;
`;

const FormSection = styled.div`
  max-width: 400px;
  margin: auto;
  display: flex;
  flex-direction: column;
  gap: 15px;
`;

const Label = styled.label`
  font-weight: bold;
`;

const Input = styled.input`
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ccc;
`;

const SaveButton = styled.button`
  background-color: green;
  color: white;
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  font-weight: bold;
  align-self: flex-end;
  cursor: pointer;
`;

const DeleteButton = styled.button`
  background-color: red;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
  margin-top: 20px;
  align-self: center;
`;

export default function Perfil_Page() {
  const navigate = useNavigate();

  return (
    <Container>
      <Sidebar>
        <SidebarTitle>DevQuiz Aluno</SidebarTitle>
        <SidebarButton onClick={() => navigate("/home/Tela")}>Home</SidebarButton>
        <SidebarButton onClick={() => navigate("/home/Quizzes")}>Quizzes</SidebarButton>
        <SidebarButton onClick={() => navigate("/home/Certificados")}>Certificados</SidebarButton>
        <SidebarButton onClick={() => navigate("/home/Ranking")}>Ranking</SidebarButton>
        <SidebarButton active>Perfil</SidebarButton>
      </Sidebar>
      <Content>
        <Title>Meu Perfil</Title>
        <ProfileSection>
          <ProfileImageWrapper>
            <ProfileImage src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" alt="Avatar" />
            <CameraIcon />
          </ProfileImageWrapper>
          <h2>Henrique localhost</h2>
          <InfoBox>
            <StatBox>
              <div>Total de Pontuação:</div>
              <Points>250 Pontos</Points>
            </StatBox>
            <StatBox>
              <div>Total de Certificados:</div>
              <Certs>2 Certificados</Certs>
            </StatBox>
          </InfoBox>
        </ProfileSection>
        <FormSection>
          <div>
            <Label>Alterar nome:</Label>
            <Input placeholder="Novo nome" />
            <SaveButton>Salvar</SaveButton>
          </div>
          <div>
            <Label>Alterar email:</Label>
            <Input placeholder="Novo email" />
            <SaveButton>Salvar</SaveButton>
          </div>
          <div>
            <Label>Alterar senha:</Label>
            <Input placeholder="Nova senha" type="password" />
            <SaveButton>Salvar</SaveButton>
          </div>
          <DeleteButton>Excluir Conta</DeleteButton>
        </FormSection>
      </Content>
    </Container>
  );
}