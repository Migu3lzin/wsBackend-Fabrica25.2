const API = "https://openlibrary.org/search.json?title=Dom+Quixote";
let token = localStorage.getItem("token");

async function login() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const res = await fetch(`${API}/token/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });

  if (res.ok) {
    const data = await res.json();
    token = data.access;
    localStorage.setItem("token", token);
    document.getElementById("loginStatus").innerText = "Login feito com sucesso!";
  } else {
    document.getElementById("loginStatus").innerText = "Falha no login!";
  }
}

async function listarLivros() {
  const res = await fetch(`${API}/books/`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  const data = await res.json();
  const ul = document.getElementById("livrosSalvos");
  ul.innerHTML = "";
  data.forEach(l => {
    const li = document.createElement("li");
    li.textContent = `${l.title} - Autores: ${l.authors.map(a => a.name).join(", ")}`;
    ul.appendChild(li);
  });
}

async function buscarOL() {
  const res = await fetch("https://openlibrary.org/search.json?title=Dom+Quixote");
  const data = await res.json();
  const ul = document.getElementById("resultadosOL");
  ul.innerHTML = "";
  data.docs.slice(0, 5).forEach(item => {
    const li = document.createElement("li");
    li.innerHTML = `<b>${item.title}</b> - ${item.author_name?.join(", ") || "Autor desconhecido"}
      <button onclick='salvarLivro("${item.title}", ${JSON.stringify(item.author_name)})'>Salvar</button>`;
    ul.appendChild(li);
  });
}

async function salvarLivro(title, authors) {
  const res = await fetch(`${API}/books/`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ title, authors }),
  });

  if (res.ok) {
    alert("Livro salvo com sucesso!");
  } else {
    alert("Erro ao salvar livro (token inválido?)");
  }
}
