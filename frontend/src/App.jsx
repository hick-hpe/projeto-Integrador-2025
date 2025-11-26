import { BrowserRouter, Routes, Route } from 'react-router-dom';
// auth
import Login from './pages/Autenticacao/Login';
import Cadastro from './pages/Autenticacao/Cadastro';
import EsqueceuSenha from './pages/Autenticacao/EsqueceuSenha';

// home
import Dashboard from './pages/Home/Dashboard';
import Perfil from './pages/Home/Perfil';
import Quizzes from './pages/Home/Quizzes';
import Ranking from './pages/Home/Ranking';
import Certificados from './pages/Home/Certificados';
import QuizInfoPage from './pages/Home/QuizInfoPage';
import QuizIniciado from './pages/Home/QuizIniciado';
import ResultadoQuiz from './pages/Home/ResultadoQuiz';

// import Erro404 from './pages/Autenticacao/Erro404';
// import VerificacaoCodigo from './pages/Autenticacao/Verificacao_recuperacao';
// import AlterarSenha from './pages/Autenticacao/alteracao_senha'; 
// import CadastroRealizado from './pages/Autenticacao/Tela_cadastrada'; 
// import Tela_inicial from './pages/Home/Tela';
// import Meus_Certificados from './pages/Home/Certificados';
// import Perfil_Page from './pages/Home/Perfil';
// import QuizInfoPage from './pages/Home/Disciplinas/Desenvolvimento_Web';
// import Quiz_de_Programacao from './pages/Home/Disciplinas/Quiz_Programacao';
// import QuizForm from './pages/Home/Disciplinas/Desenvolvimento_web/Quiz_Iniciado';
// import DesistenciaQuiz from './pages/Home/Disciplinas/Desenvolvimento_web/desisitiu';
// import Programação_Quiz from './pages/Home/Disciplinas/Pasta_de_Programacao/Quiz_iniciado';
// import Desistencia_Programacao from './pages/Home/Disciplinas/Pasta_de_Programacao/desistiu_2';
// import Resultado from "./pages/Home/Disciplinas/Pasta_de_Programacao/Resultado";
import './App.css';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* auth */}
        <Route path="/" element={<Login />} />
        <Route path="/cadastro/" element={<Cadastro/>} />
        {/* <Route path="/Tela_cadastrada" element={<CadastroRealizado/>} /> */}
        <Route path="/esqueceu-senha/" element={<EsqueceuSenha/>} />
        {/* <Route path="/Verificacao_recuperacao" element={<VerificacaoCodigo/>} /> */}
        {/* <Route path="/alteracao_senha" element={<AlterarSenha/>} /> */}
        
        {/* home */}
        <Route path="/dashboard/" element={<Dashboard/>} />
        <Route path="/quizzes/" element={<Quizzes/>} />
        <Route path="/perfil/" element={<Perfil/>} />
        <Route path='/certificados/' element={<Certificados/>} />
        <Route path="/ranking/" element={<Ranking/>} />
        <Route path="/quiz-info/:id/" element={<QuizInfoPage/>} />
        <Route path="/quiz-info/:id/iniciado/" element={<QuizIniciado/>} />
        <Route path='/resultado-quiz/' element={<ResultadoQuiz />} />

        {/* <Route path="*" element={<Erro404/>} /> */}
        {/* <Route path="/Home/Certificados" element={<Meus_Certificados/>} /> */}
        {/* <Route path="/Home/Perfil" element={<Perfil_Page/>} /> */}
        {/* <Route path="/Home/Disciplinas/Desenvolvimento_Web" element={<QuizInfoPage/>} /> */}
        {/* <Route path="/Home/Disciplinas/Quiz_Programacao" element={<Quiz_de_Programacao/>} /> */}
        {/* <Route path="/Home/Disciplinas/Desenvolvimento_web/Quiz_Iniciado" element={<QuizForm/>} /> */}
        {/* <Route path="/Home/Disciplinas/Desenvolvimento_web/desistiu" element={<DesistenciaQuiz/>} /> */}
        {/* <Route path="/Home/Disciplinas/Pasta_de_Programacao/Quiz_iniciado" element={<Programação_Quiz/>} /> */}
        {/* <Route path="/Home/Disciplinas/Pasta_de_Programacao/desistiu_2" element={<Desistencia_Programacao/>} /> */}
        {/* <Route path="/Home/Disciplinas/Pasta_de_Programacao/Resultado" element={<Resultado/>} /> */}
        

      </Routes>
    </BrowserRouter>
  );
}

