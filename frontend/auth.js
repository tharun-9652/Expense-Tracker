const API = "http://127.0.0.1:5000/api/auth";

// Save & load token helpers
function saveToken(t){ localStorage.setItem("token", t); }
function getToken(){ return localStorage.getItem("token"); }

// If already logged in → go to dashboard
if (getToken() && !window.location.href.includes("dashboard.html")) {
    window.location.href = "dashboard.html";
}

// LOGIN
const loginForm = document.querySelector("#loginForm");
if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const user = {
            username: username.value,
            password: password.value
        };

        const res = await fetch(`${API}/login`, {
            method: "POST",
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify(user)
        });

        const data = await res.json();

        if (data.token) {
            saveToken(data.token);
            window.location.href = "dashboard.html";
        } else {
            loginError.textContent = data.error;
        }
    });
}

// REGISTER
const registerForm = document.querySelector("#registerForm");
if (registerForm) {
    registerForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const user = {
            username: r_username.value,
            password: r_password.value
        };

        const res = await fetch(`${API}/register`, {
            method: "POST",
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify(user)
        });

        const data = await res.json();

        if (data.message) {
            alert("Account created! Login now.");
            window.location.href = "index.html";
        } else {
            registerError.textContent = data.error;
        }
    });
}
document.querySelector("#logoutBtn").onclick = () => {
    localStorage.removeItem("token");
    window.location.href = "index.html";
};
