import { useLocation, useNavigate } from "react-router-dom";
import styled from "styled-components";

const SidebarContainer = styled.div`
  height: 100vh;
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
  background-color: #0056b3;
  border: none;
  color: white;
  border-radius: 10px;
  padding: 10px;
  text-align: left;
  cursor: pointer;
  font-weight: bold;

  &:hover {
    background-color: #3399ff;
  }
`;

const SidebarButtonActive = styled.button`
  background-color: #e6f4ff;
  border: 2px solid #00ccff;
  color: #007bff;
  border-radius: 10px;
  padding: 10px;
  text-align: left;
  cursor: pointer;
  font-weight: bold;
`;

export default function Sidebar() {
  const navigate = useNavigate();
  const location = useLocation();

  const menu = [
    { text: "Dashboard", path: ["/dashboard"] },
    { text: "Quizzes", path: ["/quizzes", "/quiz-info/"] }, // essa rota é dinâmica: /quiz-info/:id
    { text: "Certificados", path: ["/certificados"] },
    { text: "Ranking", path: ["/ranking"] },
    { text: "Perfil", path: ["/perfil"] },
  ];

  return (
    <SidebarContainer>
      <SidebarTitle>DevQuiz Aluno</SidebarTitle>

      {menu.map((item) =>
        item.path.some((p) => location.pathname.startsWith(p)) ? (
          <SidebarButtonActive key={item.text}>
            {item.text}
          </SidebarButtonActive>
        ) : (
          <SidebarButton key={item.text} onClick={() => navigate(item.path[0])}>
            {item.text}
          </SidebarButton>
        )
      )}
    </SidebarContainer>
  );
}
