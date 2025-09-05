// src/App.js
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import TesteAPI from "./TesteAPI";
// import Login from "./components/Login";
import Cadastro from "./components/Cadastro";
import Perfil from "./components/Perfil";
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<TesteAPI />} />
        {/* <Route path="/" element={<Login />} /> */}
        <Route path="/cadastro" element={<Cadastro />} />
        <Route path="/perfil" element={<Perfil />} />
      </Routes>
    </Router>
  );
}

export default App;
