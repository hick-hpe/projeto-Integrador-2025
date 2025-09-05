import { useState, useEffect } from 'react';

function App() {
  const [message, setMessage] = useState('Carregando...');

  useEffect(() => {
    const apiUrl = import.meta.env.VITE_REACT_APP_API_URL;
    console.log(apiUrl);

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
