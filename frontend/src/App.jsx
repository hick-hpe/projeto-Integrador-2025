import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Autenticacao/Home';
import Criar_Conta from './pages/Autenticacao/Criar_Conta';
import Erro404 from './pages/Autenticacao/Erro404';
import Esqueceu_senha from './pages/Autenticacao/Esqueceu_senha';
import VerificacaoCodigo from './pages/Autenticacao/Verificacao_recuperacao';
import AlterarSenha from './pages/Autenticacao/alteracao_senha'; 
import CadastroRealizado from './pages/Autenticacao/Tela_cadastrada'; 
import Tela_inicial from './pages/Home/Tela';
import Quizzes_tela from './pages/Home/Quizzes';
import Meus_Certificados from './pages/Home/Certificados';
//import Ranking_Page from './pages/Home/Ranking';
import Perfil_Page from './pages/Home/Perfil';
import QuizInfoPage from './pages/Home/Disciplinas/Desenvolvimento_Web';
import Quiz_de_Programacao from './pages/Home/Disciplinas/Quiz_Programacao';
import QuizForm from './pages/Home/Disciplinas/Desenvolvimento_web/Quiz_Iniciado';
import DesistenciaQuiz from './pages/Home/Disciplinas/Desenvolvimento_web/desisitiu';
import Programação_Quiz from './pages/Home/Disciplinas/Pasta_de_Programacao/Quiz_iniciado';
import Desistencia_Programacao from './pages/Home/Disciplinas/Pasta_de_Programacao/desistiu_2';
import Resultado from "./pages/Home/Disciplinas/Pasta_de_Programacao/Resultado";
import './App.css';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home/>} />
        <Route path="/Criar_Conta" element={<Criar_Conta/>} />
        <Route path="/Tela_cadastrada" element={<CadastroRealizado/>} />
        <Route path="/Esqueceu_senha" element={<Esqueceu_senha/>} />
        <Route path="/Verificacao_recuperacao" element={<VerificacaoCodigo/>} />
        <Route path="/alteracao_senha" element={<AlterarSenha/>} />
        <Route path="/Home/Tela" element={<Tela_inicial/>} />
        <Route path="*" element={<Erro404/>} />
        <Route path="/Home/Quizzes" element={<Quizzes_tela/>} />
        <Route path="/Home/Certificados" element={<Meus_Certificados/>} />
        <Route path="/Home/Perfil" element={<Perfil_Page/>} />
        <Route path="/Home/Disciplinas/Desenvolvimento_Web" element={<QuizInfoPage/>} />
        <Route path="/Home/Disciplinas/Quiz_Programacao" element={<Quiz_de_Programacao/>} />
        <Route path="/Home/Disciplinas/Desenvolvimento_web/Quiz_Iniciado" element={<QuizForm/>} />
        <Route path="/Home/Disciplinas/Desenvolvimento_web/desistiu" element={<DesistenciaQuiz/>} />
        <Route path="/Home/Disciplinas/Pasta_de_Programacao/Quiz_iniciado" element={<Programação_Quiz/>} />
        <Route path="/Home/Disciplinas/Pasta_de_Programacao/desistiu_2" element={<Desistencia_Programacao/>} />
        <Route path="/Home/Disciplinas/Pasta_de_Programacao/Resultado" element={<Resultado/>} />
        

      </Routes>
    </BrowserRouter>
  );
}
//<Route path="/Home/Ranking" element={<Ranking_Page/>} /> //desativado (a pensar oque fazer no lugar)