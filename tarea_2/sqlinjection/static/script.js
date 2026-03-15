document.getElementById("loginForm").addEventListener("submit", async function(e) {
    try {
        e.preventDefault();

        const usuario = document.getElementById("usuario").value;
        const password = document.getElementById("password").value;

        const response = await fetch("/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ usuario, password })
        });

        const data = await response.json();

        if(data.success){ 
            window.location.href = data.redirect; 
        } else {
            document.getElementById("resultado").innerHTML = data.message; 
        }
    } catch (error) {
        document.getElementById("resultado").innerHTML = "Error en el servidor";
    }
});