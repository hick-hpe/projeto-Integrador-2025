import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Form, Button, Container, Row, Col } from 'react-bootstrap';
import { FaUser, FaLock, FaSignInAlt } from "react-icons/fa";

const Login = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();
    const AUTH_URL = "http://localhost:8000/auth/token/";

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await fetch(AUTH_URL, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password }),
                credentials: "include",
            });

            const data = await response.json();

            if (response.ok) {
                alert("Login feito com sucesso!");
                navigate("/perfil");
            } else {
                alert("Erro ao logar: Credenciais inválidas");
            }
        } catch (error) {
            console.error("Erro na requisição:", error);
            alert("Erro de rede ou resposta inválida.");
        }
    };

    return (
        <Container className="mt-5">
            <Row className="justify-content-center">
                <Col md={6}>
                    <h2 className="mb-4 text-center">Login</h2>
                    <Form onSubmit={handleSubmit}>
                        <Form.Group className="mb-3">
                            <Form.Label><FaUser className="me-2" />Usuário</Form.Label>
                            <Form.Control
                                type="text"
                                placeholder="Digite seu usuário"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                required
                            />
                        </Form.Group>

                        <Form.Group className="mb-3">
                            <Form.Label><FaLock className="me-2" />Senha</Form.Label>
                            <Form.Control
                                type="password"
                                placeholder="Digite sua senha"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                            />
                        </Form.Group>

                        <div className="d-grid">
                            <Button variant="primary" type="submit">
                                <FaSignInAlt className="me-2" /> Entrar
                            </Button>
                        </div>
                        <a href="/cadastro">Criar conta</a>
                    </Form>
                </Col>
            </Row>
        </Container>
    );
};

export default Login;
