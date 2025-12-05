'''
{front index.html do site de receita}

<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Receitas Do MasterChef</title>
  <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600&display=swap" rel="stylesheet">
  <style>
    * {
      box-sizing: border-box;
    }

    body {
      font-family: 'Quicksand', sans-serif;
      margin: 0;
      padding: 0;
      background-color: #fffaf4;
      color: #333;
      transition: background-color 0.3s ease, color 0.3s ease;
    }

    .dark-mode {
      background-color: #2c2c2c;
      color: #f5f5f5;
    }

    header {
      background-color: #ff7043;
      color: white;
      padding: 15px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      position: relative;
      box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }

    .menu-icon {
      font-size: 24px;
      cursor: pointer;
    }

    .menu-options {
      display: none;
      position: absolute;
      top: 60px;
      right: 20px;
      background-color: white;
      border: 1px solid #ccc;
      border-radius: 8px;
      padding: 10px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.2);
      z-index: 10;
      }

    .menu-aberto {
      display: flex;
      flex-direction: column;
      gap: 10px;
     }

    .menu-options button {
      background-color: #ff7043;
      color: white;
      border: none;
      border-radius: 5px;
      padding: 8px 12px;
      font-size: 14px;
      cursor: pointer;
      transition: background 0.3s;
    }

    .menu-options button:hover {
      background-color: #e64a19;
    }

    .receitas-container {
      padding: 30px 20px;
      max-width: 800px;
      margin: auto;
    }

    h2 {
      text-align: center;
      font-size: 28px;
      margin-bottom: 20px;
    }

    h2::before {
      content: "🍽️ ";
    }

    .titulo-receita {
      cursor: pointer;
      font-weight: bold;
      font-size: 18px;
      margin: 15px 0 5px;
      padding: 10px;
      background-color: #ffe0b2;
      border-radius: 6px;
      transition: background 0.3s, transform 0.2s ease;
      animation: fadeInUp 0.5s ease;
    }

    .titulo-receita::before {
      content: "📌 ";
    }

    .titulo-receita:hover {
      background-color: #ffcc80;
      transform: scale(1.02);
    }

    .detalhes-receita {
      display: none;
      background-color: #fff3e0;
      padding: 15px;
      border-radius: 6px;
      margin-bottom: 20px;
      box-shadow: 0 1px 4px rgba(0,0,0,0.1);
    }

    .dark-mode .titulo-receita {
      background-color: #444;
      color: #fff;
    }

    .dark-mode .detalhes-receita {
      background-color: #555;
    }

    #formulario {
      display: none;
      padding: 30px 20px;
      max-width: 800px;
      margin: auto;
      background-color: #fff3e0;
      border-radius: 8px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    #formulario h3 {
      margin-bottom: 15px;
    }

    input, textarea {
      width: 100%;
      padding: 10px;
      margin-bottom: 12px;
      border: 1px solid #ccc;
      border-radius: 6px;
      font-size: 14px;
    }

    button {
      background-color: #ff7043;
      color: white;
      border: none;
      padding: 10px 16px;
      border-radius: 6px;
      font-size: 16px;
      cursor: pointer;
      transition: background 0.3s;
    }

    button:hover {
      background-color: #e64a19;
    }

    @keyframes fadeInUp {
      from {
        opacity: 0;
        transform: translateY(20px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    @media (max-width: 600px) {
      .receitas-container, #formulario {
        padding: 20px 10px;
      }
    }
  </style>
</head>
<body>

  <header>
    <h1>🍲 Receitas</h1>
    <div>
      <button onclick="toggleDarkMode()">🌙 Modo Escuro</button>
      <span class="menu-icon" onclick="toggleMenu()">☰</span>
    </div>
    <div class="menu-options" id="menu">
        <button onclick="window.location.href='cadastrar.html'">Cadastrar Receita</button>
      <button onclick="window.location.href='cad_usuario3.html'">Registrar-se
      <button onclick="window.location.href='cad_usuario2.html'">Fazer Login</button>
    </div>
  </header>

  <div class="receitas-container">
    <h2>📚 Lista de Receitas</h2>
    <div id="lista-receitas"></div>
  </div>

  <div id="formulario">
    <h3>➕ Nova Receita</h3>
    <input type="text" id="nome" placeholder="Nome da receita">
    <textarea id="ingredientes" placeholder="Ingredientes (um por linha)"></textarea>
    <textarea id="modo" placeholder="Modo de preparo"></textarea>
    <button onclick="handleCriar()">Salvar</button>
  </div>

  <script>
    const API_BASE = "https://beck-end-do-site-de-receitas.vercel.app";

    function toggleMenu() {
      const menu = document.getElementById("menu");
      menu.classList.toggle("menu-aberto");
    }

    function mostrarFormulario() {
      document.getElementById("formulario").style.display = "block";
      document.getElementById("menu").style.display = "none";
    }

    function toggleDarkMode() {
      document.body.classList.toggle("dark-mode");
    }

    async function buscarReceitas() {
      const res = await fetch(`${API_BASE}/receber`);
      if (!res.ok) throw new Error("Erro ao buscar receitas");
      return await res.json();
    }

    async function criarReceita(dados) {
      const res = await fetch(`${API_BASE}/enviar`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dados)
      });
      if (!res.ok) throw new Error("Erro ao criar receita");
      return await res.json();
    }

    async function handleCriar() {
      const nome = document.getElementById("nome").value;
      const ingredientes = document.getElementById("ingredientes").value;
      const modo = document.getElementById("modo").value;

      const novaReceita = { nome_da_receita: nome, ingredientes, modo_de_preparo: modo };
      await criarReceita(novaReceita);
      document.getElementById("formulario").style.display = "none";
      await carregarReceitas();
    }

    function formatarIngredientes(texto) {
      const itens = texto.split("\n").filter(i => i.trim() !== "");
      return `<ul>${itens.map(i => `<li>${i}</li>`).join("")}</ul>`;
    }

    async function carregarReceitas() {
      const container = document.getElementById("lista-receitas");
      container.innerHTML = "";
      const receitas = await buscarReceitas();

      receitas.forEach(r => {
        const div = document.createElement("div");
        div.innerHTML = `
          <div class="titulo-receita" onclick="window.location.href='receita.html?id=${r.id}'">${r.nome_da_receita}</div>
          <div class="detalhes-receita" id="detalhes-${r.id}">
            <strong>Ingredientes:</strong><br> ${formatarIngredientes(r.ingredientes)}<br>
            <strong>Modo de preparo:</strong><br> ${r.modo_de_preparo}
          </div>
        `;
        container.appendChild(div);
      });
    }

    carregarReceitas();
  </script>

</body>
</html>


'''
############################################################
'''
{front do receita.html do site de receita}



<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Detalhes da Receita</title>
  <style>
    body {
      font-family: 'Segoe UI', sans-serif;
      background-color: #fffaf4;
      padding: 30px;
      max-width: 800px;
      margin: auto;
    }

    h2 {
      color: #ff7043;
      margin-bottom: 20px;
    }

    ul {
      padding-left: 20px;
      margin-bottom: 30px;
    }

    li {
      margin-bottom: 8px;
    }

    .modo-preparo {
      background-color: #fff3e0;
      padding: 15px;
      border-radius: 6px;
      box-shadow: 0 1px 4px rgba(0,0,0,0.1);
    }

    a {
      display: inline-block;
      margin-bottom: 20px;
      color: #ff7043;
      text-decoration: none;
    }

    a:hover {
      text-decoration: underline;
    }
  </style>
</head>
<body>

  <a href="javascript:history.back()">← Voltar</a>
  <h2 id="titulo-receita">Receita</h2>
  <h3>Ingredientes</h3>
  <ul id="lista-ingredientes"></ul>
  <h3>Modo de Preparo</h3>
  <div class="modo-preparo" id="modo-preparo"></div>
<script>
  // URL da sua API hospedada na Vercel
  const API_BASE = "https://beck-end-do-site-de-receitas.vercel.app";

  function getIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get("id");
  }

  async function buscarReceitaPorId(id) {
    const res = await fetch(`${API_BASE}/especifico/${id}`);
    if (!res.ok) throw new Error("Erro ao buscar receita");
    return await res.json();
  }

  async function carregarDetalhes() {
    const id = getIdFromURL();
    const receita = await buscarReceitaPorId(id);

    document.getElementById("titulo-receita").textContent = receita.nome_da_receita;

    const ingredientes = receita.ingredientes
      .split(",")
      .map(i => i.trim())
      .filter(i => i !== "");
    const lista = document.getElementById("lista-ingredientes");
    ingredientes.forEach(item => {
      const li = document.createElement("li");
      li.textContent = item;
      lista.appendChild(li);
    });

    document.getElementById("modo-preparo").textContent = receita.modo_de_preparo;
  }

  carregarDetalhes();
</script>


</body>
</html>



'''
#################################################################
'''
{front do cadastrar.html do site de receita}

<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Cadastrar Receita</title>
  <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600&display=swap" rel="stylesheet">
  <style>
    body {
      font-family: 'Quicksand', sans-serif;
      margin: 0;
      padding: 0;
      background-color: #fffaf4;
      color: #333;
    }

    header {
      background-color: #ff7043;
      color: white;
      padding: 15px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }

    .voltar {
      background: none;
      border: none;
      color: white;
      font-size: 18px;
      cursor: pointer;
    }

    .form-container {
      max-width: 800px;
      margin: 40px auto;
      background-color: #fff3e0;
      padding: 30px;
      border-radius: 8px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    h2 {
      text-align: center;
      margin-bottom: 20px;
    }

    input, textarea {
      width: 100%;
      padding: 10px;
      margin-bottom: 12px;
      border: 1px solid #ccc;
      border-radius: 6px;
      font-size: 14px;
    }

    button {
      background-color: #ff7043;
      color: white;
      border: none;
      padding: 10px 16px;
      border-radius: 6px;
      font-size: 16px;
      cursor: pointer;
      transition: background 0.3s;
    }

    button:hover {
      background-color: #e64a19;
    }

    .loading {
      text-align: center;
      margin-top: 10px;
      font-size: 14px;
      color: #888;
    }
  </style>
</head>
<body>

  <header>
    <button class="voltar" onclick="window.location.href='index.html'">← Voltar</button>
    <h1>Nova Receita</h1>
    <div></div>
  </header>

  <div class="form-container">
    <h2>Cadastrar Receita</h2>
    <input type="text" id="nome" placeholder="Nome da receita">
    <textarea id="ingredientes" placeholder="Ingredientes (um por linha)"></textarea>
    <textarea id="modo" placeholder="Modo de preparo"></textarea>
    <button id="btnSalvar" onclick="handleCriar()">Salvar Receita</button>
    <div id="loading" class="loading" style="display: none;">Salvando receita...</div>
  </div>
<script>
  // URL base da sua API hospedada na Vercel
  const API_BASE = "https://beck-end-do-site-de-receitas.vercel.app";

  async function criarReceita(dados) {
    const token = localStorage.getItem("access_token");

    if (!token) {
      alert("Você precisa estar logado para cadastrar uma receita.");
      return;
    }

    try {
      const res = await fetch(`${API_BASE}/enviar`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(dados)
      });

      const result = await res.json();

      if (!res.ok) {
        alert(result.detail || "Erro ao salvar receita.");
        return;
      }

      alert("Receita cadastrada com sucesso!");
      window.location.href = "index.html";
    } catch (error) {
      alert("Erro de conexão com o servidor.");
      console.error(error);
    }
  }

  async function handleCriar() {
    const nome = document.getElementById("nome").value;
    const ingredientes = document.getElementById("ingredientes").value;
    const modo = document.getElementById("modo").value;
    const btn = document.getElementById("btnSalvar");
    const loading = document.getElementById("loading");

    if (!nome || !ingredientes || !modo) {
      alert("Preencha todos os campos!");
      return;
    }

    btn.disabled = true;
    loading.style.display = "block";

    const novaReceita = {
      nome_da_receita: nome,
      ingredientes,
      modo_de_preparo: modo
    };

    await criarReceita(novaReceita);

    btn.disabled = false;
    loading.style.display = "none";
  }
</script>


</body>
</html>



'''
################################################################
'''
{front do cad_usuario2.html do site de receita}


<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <title>Login - Receitas</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background: #f9f9f9;
      margin: 0;
      padding: 0;
    }

    .top-bar {
      background-color: #ffffff;
      padding: 10px 20px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      display: flex;
      align-items: center;
    }

    .back-button {
      text-decoration: none;
      color: #007bff;
      font-weight: bold;
      font-size: 16px;
    }

    .container {
      display: flex;
      flex-direction: column;
      align-items: center;
      margin-top: 100px;
    }

    form {
      background: white;
      padding: 30px;
      border-radius: 8px;
      box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }

    input {
      display: block;
      margin-bottom: 15px;
      padding: 10px;
      width: 250px;
    }

    button {
      padding: 10px 20px;
      background: #28a745;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }

    #response {
      margin-top: 20px;
      font-weight: bold;
    }
  </style>
</head>
<body>

  <div class="top-bar">
    <a href="index.html" class="back-button">← Voltar</a>
  </div>

  <div class="container">
    <form id="loginForm">
      <h2>Login</h2>
      <input type="text" id="username" placeholder="Usuário" required />
      <input type="password" id="password" placeholder="Senha" required />
      <button type="submit">Entrar</button>
    </form>

    <div id="response"></div>
  </div>

  <script>
    const form = document.getElementById('loginForm');
    const responseDiv = document.getElementById('response');

    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      const username = document.getElementById('username').value;
      const password = document.getElementById('password').value;

      try {
        const res = await fetch('https://beck-end-do-site-de-receitas.vercel.app/login10', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ username, password })
        });

        const data = await res.json();

        if (res.ok) {
          responseDiv.textContent = 'Login bem-sucedido!';
          responseDiv.style.color = 'green';
          localStorage.setItem('access_token', data.access_token);

          // Redireciona para a página de envio de receita
          setTimeout(() => {
            window.location.href = 'cadastrar.html';
          }, 1000);
        } else {
          responseDiv.textContent = data.detail || 'Erro ao fazer login.';
          responseDiv.style.color = 'red';
        }
      } catch (error) {
        responseDiv.textContent = 'Erro de conexão com o servidor.';
        responseDiv.style.color = 'red';
      }
    });
  </script>

</body>
</html>


'''
#############################################################
'''
{front do cad_usuario3.html do site de receita}

<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Registro</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #f4f4f4;
      margin: 0;
      padding: 0;
    }

    .top-bar {
      background-color: #fff;
      padding: 10px;
      display: flex;
      align-items: center;
    }

    .back-button {
      background-color: #007BFF;
      color: white;
      border: none;
      padding: 8px 12px;
      border-radius: 4px;
      cursor: pointer;
      margin-left: 10px;
    }

    .container {
      max-width: 400px;
      margin: 50px auto;
      background-color: white;
      padding: 30px;
      border-radius: 8px;
      box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }

    h2 {
      text-align: center;
      margin-bottom: 20px;
    }

    input {
      width: 100%;
      padding: 10px;
      margin: 8px 0;
      border: 1px solid #ccc;
      border-radius: 4px;
    }

    button {
      width: 100%;
      background-color: #28a745;
      color: white;
      padding: 10px;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }

    button:hover {
      background-color: #218838;
    }

    .message {
      margin-top: 15px;
      text-align: center;
      font-weight: bold;
    }

    .success {
      color: green;
    }

    .error {
      color: red;
    }
  </style>
</head>
<body>

  <div class="top-bar">
    <button class="back-button" onclick="window.location.href='index.html'">← Voltar</button>
  </div>

  <div class="container">
    <h2>Registro</h2>
    <form id="registerForm">
      <input type="text" id="username" placeholder="Nome de usuário" required>
      <input type="password" id="password" placeholder="Senha" required>
      <button type="submit">Registrar</button>
    </form>
    <div class="message" id="message"></div>
  </div>

  <script>
    const form = document.getElementById("registerForm");
    const message = document.getElementById("message");

    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      const username = document.getElementById("username").value.trim();
      const password = document.getElementById("password").value.trim();

      if (!username || !password) {
        message.textContent = "Preencha todos os campos.";
        message.className = "message error";
        return;
      }

      const data = { username, password };

      try {
        const response = await fetch("https://beck-end-do-site-de-receitas.vercel.app/register", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
          message.textContent = result.msg || "Usuário registrado com sucesso!";
          message.className = "message success";

          // Redireciona para login após 2 segundos
          setTimeout(() => {
            window.location.href = "cad_usuario2.html";
          }, 2000);
        } else {
          message.textContent = result.detail || "Erro ao registrar.";
          message.className = "message error";
        }
      } catch (err) {
        message.textContent = "Erro de conexão com o servidor.";
        message.className = "message error";
      }
    });
  </script>

</body>
</html>


'''
############################################################

'''
{front index.html do site de receita}

<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Receitas Do MasterChef</title>
  <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600&display=swap" rel="stylesheet">
  <style>
    * {
      box-sizing: border-box;
    }

    html, body {
      margin: 0;
      padding: 0;
      font-family: 'Quicksand', sans-serif;
      background-color: #fffaf4;
      color: #333;
      overflow-x: hidden;
      transition: background-color 0.3s ease, color 0.3s ease;
    }

    .dark-mode {
      background-color: #2c2c2c;
      color: #f5f5f5;
    }

    header {
      background-color: #ff7043;
      color: white;
      padding: 15px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 10px;
      box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }

    .menu-icon {
      font-size: 24px;
      cursor: pointer;
    }

    .menu-options {
      display: none;
      position: absolute;
      top: 60px;
      right: 20px;
      background-color: white;
      border: 1px solid #ccc;
      border-radius: 8px;
      padding: 10px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.2);
      z-index: 10;
    }

    .menu-aberto {
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .menu-options button {
      background-color: #ff7043;
      color: white;
      border: none;
      border-radius: 5px;
      padding: 8px 12px;
      font-size: 14px;
      cursor: pointer;
      transition: background 0.3s;
    }

    .menu-options button:hover {
      background-color: #e64a19;
    }

    .receitas-container {
      padding: 30px 20px;
      max-width: 800px;
      margin: auto;
    }

    h2 {
      text-align: center;
      font-size: 28px;
      margin-bottom: 20px;
    }

    h2::before {
      content: "🍽️ ";
    }

    .titulo-receita {
      cursor: pointer;
      font-weight: bold;
      font-size: 18px;
      margin: 15px 0 5px;
      padding: 10px;
      background-color: #ffe0b2;
      border-radius: 6px;
      transition: background 0.3s, transform 0.2s ease;
      animation: fadeInUp 0.5s ease;
    }

    .titulo-receita::before {
      content: "📌 ";
    }

    .titulo-receita:hover,
    .titulo-receita:focus {
      background-color: #ffcc80;
      transform: scale(1.02);
      outline: 2px solid #ff7043;
    }

    .detalhes-receita {
      display: none;
      background-color: #fff3e0;
      padding: 15px;
      border-radius: 6px;
      margin-bottom: 20px;
      box-shadow: 0 1px 4px rgba(0,0,0,0.1);
    }

    .dark-mode .titulo-receita {
      background-color: #444;
      color: #fff;
    }

    .dark-mode .detalhes-receita {
      background-color: #555;
    }

    #formulario {
      display: none;
      padding: 30px 20px;
      max-width: 800px;
      margin: auto;
      background-color: #fff3e0;
      border-radius: 8px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    #formulario h3 {
      margin-bottom: 15px;
    }

    input, textarea {
      width: 100%;
      padding: 10px;
      margin-bottom: 12px;
      border: 1px solid #ccc;
      border-radius: 6px;
      font-size: 14px;
    }

    button {
      background-color: #ff7043;
      color: white;
      border: none;
      padding: 10px 16px;
      border-radius: 6px;
      font-size: 16px;
      cursor: pointer;
      transition: background 0.3s;
    }

    button:hover {
      background-color: #e64a19;
    }

    button:focus {
      outline: 2px solid #ff7043;
    }

    @keyframes fadeInUp {
      from {
        opacity: 0;
        transform: translateY(20px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    @media (max-width: 600px) {
      .receitas-container, #formulario {
        padding: 20px 10px;
      }

      h2 {
        font-size: 22px;
      }

      .titulo-receita {
        font-size: 16px;
        padding: 8px;
      }

      button {
        font-size: 14px;
        padding: 8px 12px;
      }
    }

    @media (min-width: 1200px) {
      body {
        font-size: 18px;
      }

      .receitas-container, #formulario {
        max-width: 1000px;
      }
    }
  </style>
</head>
<body>

  <header>
    <h1>🍲 Receitas</h1>
    <div>
      <button onclick="toggleDarkMode()">🌙 Modo Escuro</button>
      <span class="menu-icon" onclick="toggleMenu()">☰</span>
    </div>
    <div class="menu-options" id="menu">
      <button onclick="window.location.href='cadastrar.html'">Cadastrar Receita</button>
      <button onclick="window.location.href='cad_usuario3.html'">Registrar-se</button>
      <button onclick="window.location.href='cad_usuario2.html'">Fazer Login</button>
    </div>
  </header>

  <div class="receitas-container">
    <h2>📚 Lista de Receitas</h2>
    <div id="lista-receitas"></div>
  </div>

  <div id="formulario">
    <h3>➕ Nova Receita</h3>
    <input type="text" id="nome" placeholder="Nome da receita">
    <textarea id="ingredientes" placeholder="Ingredientes (um por linha)"></textarea>
    <textarea id="modo" placeholder="Modo de preparo"></textarea>
    <button onclick="handleCriar()">Salvar</button>
  </div>

  <script>
    const API_BASE = "https://beck-end-do-site-de-receitas.vercel.app";

    function toggleMenu() {
      const menu = document.getElementById("menu");
      menu.classList.toggle("menu-aberto");
    }

    function mostrarFormulario() {
      document.getElementById("formulario").style.display = "block";
      document.getElementById("menu").style.display = "none";
    }

    function toggleDarkMode() {
      document.body.classList.toggle("dark-mode");
    }

    async function buscarReceitas() {
      const res = await fetch(`${API_BASE}/receber`);
      if (!res.ok) throw new Error("Erro ao buscar receitas");
      return await res.json();
    }

    async function criarReceita(dados) {
      const res = await fetch(`${API_BASE}/enviar`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dados)
      });
      if (!res.ok) throw new Error("Erro ao criar receita");
      return await res.json();
    }

    async function handleCriar() {
      const nome = document.getElementById("nome").value;
      const ingredientes = document.getElementById("ingredientes").value;
      const modo = document.getElementById("modo").value;

      const novaReceita = { nome_da_receita: nome, ingredientes, modo_de_preparo: modo };
      await criarReceita(novaReceita);
      document.getElementById("formulario").style.display = "none";
      await carregarReceitas();
    }

    function formatarIngredientes(texto) {
      const itens = texto.split("\n").filter(i => i.trim() !== "");
      return `<ul>${itens.map(i => `<li>${i}</li>`).join("")}</ul>`;
    }
                                                

    async function carregarReceitas() {
      const container = document.getElementById("lista-receitas");
      container.innerHTML = "";
      const receitas = await buscarReceitas();

      receitas.forEach(r => {
        const div = document.createElement("div");
        div.innerHTML = `
          <div class="titulo-receita" onclick="window.location.href='receita.html?id=${r.id}'">${r.nome_da_receita}</div>
          <div class="detalhes-receita" id="detalhes-${r.id}">
            <strong>Ingredientes:</strong><br> ${formatarIngredientes(r.ingredientes)}<br>
            <strong>Modo de preparo:</strong><br> ${r.modo_de_preparo}
          </div>
        `;
        container.appendChild(div);
      });
    }

    carregarReceitas();
  </script>

</body>
</html>


'''

'''
{front receita.html do site de receita}


<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Detalhes da Receita</title>
  <style>
    * {
      box-sizing: border-box;
    }

    html, body {
      margin: 0;
      padding: 0;
      font-family: 'Segoe UI', sans-serif;
      background-color: #fffaf4;
      color: #333;
      overflow-x: hidden;
    }

    body {
      padding: 30px;
      max-width: 800px;
      margin: auto;
    }

    h2 {
      color: #ff7043;
      margin-bottom: 20px;
      font-size: 28px;
      text-align: center;
    }

    h3 {
      font-size: 20px;
      margin-top: 30px;
    }

    ul {
      padding-left: 20px;
      margin-bottom: 30px;
    }

    li {
      margin-bottom: 8px;
      font-size: 16px;
    }

    .modo-preparo {
      background-color: #fff3e0;
      padding: 15px;
      border-radius: 6px;
      box-shadow: 0 1px 4px rgba(0,0,0,0.1);
      font-size: 16px;
      line-height: 1.5;
    }

    a {
      display: inline-block;
      margin-bottom: 20px;
      color: #ff7043;
      text-decoration: none;
      font-size: 16px;
    }

    a:hover {
      text-decoration: underline;
    }

    @media (max-width: 600px) {
      body {
        padding: 20px 15px;
      }

      h2 {
        font-size: 22px;
      }

      h3 {
        font-size: 18px;
      }

      li, .modo-preparo, a {
        font-size: 15px;
      }
    }

    @media (min-width: 1200px) {
      body {
        max-width: 1000px;
        font-size: 18px;
      }
    }
  </style>
</head>
<body>

  <a href="javascript:history.back()">← Voltar</a>
  <h2 id="titulo-receita">Receita</h2>
  <h3>Ingredientes</h3>
  <ul id="lista-ingredientes"></ul>
  <h3>Modo de Preparo</h3>
  <div class="modo-preparo" id="modo-preparo"></div>

  <script>
    const API_BASE = "https://beck-end-do-site-de-receitas.vercel.app";

    function getIdFromURL() {
      const params = new URLSearchParams(window.location.search);
      return params.get("id");
    }

    async function buscarReceitaPorId(id) {
      const res = await fetch(`${API_BASE}/especifico/${id}`);
      if (!res.ok) throw new Error("Erro ao buscar receita");
      return await res.json();
    }

    async function carregarDetalhes() {
      const id = getIdFromURL();
      const receita = await buscarReceitaPorId(id);

      document.getElementById("titulo-receita").textContent = receita.nome_da_receita;

      const ingredientes = receita.ingredientes
        .split(",")
        .map(i => i.trim())
        .filter(i => i !== "");
      const lista = document.getElementById("lista-ingredientes");
      ingredientes.forEach(item => {
        const li = document.createElement("li");
        li.textContent = item;
        lista.appendChild(li);
      });

      document.getElementById("modo-preparo").textContent = receita.modo_de_preparo;
    }

    carregarDetalhes();
  </script>

</body>
</html>



'''