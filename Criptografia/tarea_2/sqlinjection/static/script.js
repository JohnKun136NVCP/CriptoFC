document.getElementById("loginForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const usuario = document.getElementById("usuario").value;
    const password = document.getElementById("password").value;

   
    const response = await fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ usuario, password })
    });

    const data = await response.text();
    document.getElementById("resultado").innerHTML = data;
});
