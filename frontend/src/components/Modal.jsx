import styled from "styled-components";
import { IoClose } from "react-icons/io5";

const ModalBackDrop = styled.div`
  display: ${({ visible }) => (visible ? "flex" : "none")};
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  justify-content: center;
  align-items: center;
  z-index: 999;
`;

const ModalContent = styled.div`
  background: #fff;
  padding: 25px;
  border-radius: 12px;
  width: 380px;
  max-width: 95%;
  text-align: center;
  position: relative;
  animation: fadeIn 0.25s ease;

  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: scale(0.95);
    }
    to {
      opacity: 1;
      transform: scale(1);
    }
  }
`;

const CloseBtn = styled.button`
  position: absolute;
  top: 10px;
  right: 10px;
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 22px;
  color: #555;

  &:hover {
    color: red;
  }
`;

const FooterButton = styled.button`
  margin-top: 20px;
  background: #007bff;
  color: white;
  padding: 10px 18px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-size: 16px;

  &:hover {
    background: #005fcc;
  }
`;

export default function Modal({ children, visible, onClose, funcaoParaBotao }) {
  return (
    <ModalBackDrop visible={visible}>
      <ModalContent>
        <CloseBtn onClick={onClose}>
          <IoClose />
        </CloseBtn>

        {children}

        {
          funcaoParaBotao ?
            <FooterButton onClick={funcaoParaBotao}>OK</FooterButton>
            :
            <FooterButton onClick={onClose}>OK</FooterButton>
        }
      </ModalContent>
    </ModalBackDrop>
  );
}
