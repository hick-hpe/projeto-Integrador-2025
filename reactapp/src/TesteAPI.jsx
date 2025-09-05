import { useState, useEffect } from 'react';

function App() {
  const [message, setMessage] = useState('Carregando...');

  useEffect(() => {
    // URL da API dentro da rede Docker
    const apiUrl = process.env.REACT_APP_API_URL; // ajuste conforme sua rota

    fetch(apiUrl)
      .then((res) => res.json())
      .then((data) => setMessage(data.message))
      .catch((err) => setMessage('Erro ao conectar à API'));
  }, []);

  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h1>{message}</h1>
    </div>
  );
}

export default App;
