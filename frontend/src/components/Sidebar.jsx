import { useLocation, useNavigate } from "react-router-dom";
import styled from "styled-components";
import { FaChevronRight, FaTimes } from "react-icons/fa";
import { useState } from "react";

const SidebarWrapper = styled.div`
  position: relative;
  z-index: 999;
`;

const SidebarContainer = styled.div`
  height: 100vh;
  width: 220px;
  background-color: #007bff;
  color: white;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  position: fixed;
  top: 0;
  left: 0;
  transition: transform 0.3s ease;

  /* Desktop */
  @media (min-width: 768px) {
    position: relative;
    transform: translateX(0) !important;
  }

  /* Mobile Slide */
  transform: translateX(
    ${(props) => (props.active ? "0" : "-100%")}
  );
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

const OpenIcon = styled.div`
  position: fixed;
  top: 50%;
  left: 10px;
  background-color: #007bff;
  padding: 15px 8px;
  border-radius: 10px;
  display: flex;
  cursor: pointer;
  z-index: 999;

  /* Só aparece no mobile */
  @media (min-width: 768px) {
    display: none;
  }
`;

const CloseButton = styled.button`
  background: none;
  border: none;
  color: white;
  font-size: 22px;
  cursor: pointer;
  align-self: flex-end;

  /* Some no desktop */
  @media (min-width: 768px) {
    display: none;
  }
`;

export default function Sidebar() {
  const navigate = useNavigate();
  const location = useLocation();

  const [open, setOpen] = useState(false);

  const menu = [
    { text: "Dashboard", path: ["/dashboard"] },
    { text: "Quizzes", path: ["/quizzes", "/quiz-info/"] },
    { text: "Certificados", path: ["/certificados"] },
    { text: "Emblemas", path: ["/emblemas"] },
    { text: "Perfil", path: ["/perfil"] },
    { text: "Validar certificado", path: ["/validar-ceritificado"]}
  ];

  return (
    <SidebarWrapper>

      {/* Botão de abrir (aparece só no mobile) */}
      {!open && (
        <OpenIcon onClick={() => setOpen(true)}>
          <FaChevronRight color="#fff" size={20} />
        </OpenIcon>
      )}

      {/* Sidebar */}
      <SidebarContainer active={open}>
        {/* Botão de fechar — só no mobile */}
        <CloseButton onClick={() => setOpen(false)}>
          <FaTimes />
        </CloseButton>

        <SidebarTitle>DevQuiz Aluno</SidebarTitle>

        {menu.map((item) =>
          item.path.some((p) => location.pathname.startsWith(p)) ? (
            <SidebarButtonActive key={item.text}>
              {item.text}
            </SidebarButtonActive>
          ) : (
            <SidebarButton
              key={item.text}
              onClick={() => {
                navigate(item.path[0]);
                setOpen(false); // fecha quando navega (mobile)
              }}
            >
              {item.text}
            </SidebarButton>
          )
        )}
      </SidebarContainer>
    </SidebarWrapper>
  );
}
