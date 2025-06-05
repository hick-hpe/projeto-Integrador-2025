import { useState } from "react";
import { useNavigate } from "react-router-dom";

const Login = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();
    const AUTH_URL = "http://localhost:8000/auth/";

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await fetch(AUTH_URL + "token/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password }),
                credentials: "include",
            });

            const data = await response.json();
            console.log("Resposta da API:", data);

            if (response.ok) {
                alert("Login feito com sucesso!");
                navigate("/perfil");
            } else {
                alert("Erro ao logar: " + (data.detail || "Erro desconhecido"));
            }
        } catch (error) {
            console.error("Erro na requisição:", error);
            alert("Erro de rede ou resposta inválida.");
        }
    };

    return (
        <div>
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Usuário"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                /><br />
                <input
                    type="password"
                    placeholder="Senha"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                /><br />
                <button type="submit">Entrar</button>
            </form>
        </div>
    );
}

export default Login;
