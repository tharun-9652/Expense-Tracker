// ------------------- AUTH REDIRECT -------------------
// Only protect dashboard (index.html)
if (!localStorage.getItem("token") && window.location.pathname.includes("index.html")) {
    window.location.href = "login.html";
}

// Auto-detect backend URL
const API = (window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost')
    ? "http://127.0.0.1:5000/api"
    : "/api";

// Shorthands
const qs = s => document.querySelector(s);
const qsa = s => document.querySelectorAll(s);

// Views
const views = {
    dashboard: qs("#dashboard"),
    expenses: qs("#expenses"),
    categories: qs("#categories"),
    reports: qs("#reports")
};

const navBtns = qsa(".nav-btn");

// Month
let currentMonth = new Date().toISOString().slice(0, 7);
qs("#filterMonth").value = currentMonth;


// ------------------- INIT -------------------
function init() {
    setupNav();
    setupTheme();
    bindAddExpenseForm();
    bindCategoryActions();
    loadCategories();
    loadExpensesTable();
    refreshDashboard();
    bindReportRefresh();
}
init();


// ------------------- NAVIGATION -------------------
function setupNav() {
    navBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            navBtns.forEach(x => x.classList.remove("active"));
            btn.classList.add("active");
            showView(btn.dataset.view);
        });
    });
}

function showView(name) {
    Object.keys(views).forEach(k => {
        views[k].classList.toggle("hidden", k !== name);
    });

    if (name === "expenses") loadExpensesTable();
    if (name === "reports") refreshReports();
}


// ------------------- THEME -------------------
function setupTheme() {
    const saved = localStorage.getItem("theme") || "light";
    setTheme(saved);

    qs("#themeToggle").addEventListener("click", () => {
        const newTheme = document.body.classList.contains("dark") ? "light" : "dark";
        setTheme(newTheme);
    });
}

function setTheme(theme) {
    document.body.classList.toggle("dark", theme === "dark");
    localStorage.setItem("theme", theme);
    qs("#themeToggle").textContent = theme === "dark" ? "☀️" : "🌙";
}


// ------------------- EXPENSES -------------------
function bindAddExpenseForm() {
    const form = qs("#addForm");
    const clearBtn = qs("#clearForm");

    clearBtn.addEventListener("click", () => form.reset());

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const payload = {
            date: qs("#date").value,
            category: qs("#categorySelect").value,
            merchant: qs("#merchant").value,
            amount: parseFloat(qs("#amount").value),
            notes: qs("#notes").value
        };

        await fetch(`${API}/expenses`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem("token")}`
            },
            body: JSON.stringify(payload)
        });

        form.reset();
        loadExpensesTable();
        refreshDashboard();
    });
}

async function loadExpensesTable() {
    const r = await fetch(`${API}/expenses`, {
        headers: {
            "Authorization": `Bearer ${localStorage.getItem("token")}`
        }
    });
    const data = await r.json();

    const tbody = qs("#expensesTable");
    tbody.innerHTML = "";

    data.forEach(e => {
        tbody.innerHTML += `
            <tr>
                <td>${e.date}</td>
                <td>${e.category}</td>
                <td>${e.merchant}</td>
                <td>₹${e.amount}</td>
            </tr>
        `;
    });
}


// ------------------- CATEGORIES -------------------
function bindCategoryActions() {
    qs("#addCategoryBtn").addEventListener("click", addCategory);
}

async function addCategory() {
    const input = qs("#newCategory");
    const name = input.value.trim();

    if (!name) return;

    await fetch(`${API}/categories`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem("token")}`
        },
        body: JSON.stringify({ name })
    });

    input.value = "";
    loadCategories();
}

async function loadCategories() {
    const r = await fetch(`${API}/categories`, {
        headers: {
            "Authorization": `Bearer ${localStorage.getItem("token")}`
        }
    });
    const cats = await r.json();

    const select = qs("#categorySelect");
    select.innerHTML = cats.map(c => `<option>${c.name}</option>`).join("");

    const list = qs("#categoryList");
    list.innerHTML = cats.map(c => `<li>${c.name}</li>`).join("");
}


// ------------------- REPORTS -------------------
function bindReportRefresh() {
    qs("#refreshReport").addEventListener("click", refreshReports);
}

function normalizeMonth(v) {
    if (/^\d{4}-\d{2}$/.test(v)) return v;

    const d = new Date(v);
    return !isNaN(d) ? d.toISOString().slice(0, 7) : new Date().toISOString().slice(0, 7);
}

async function refreshReports() {
    const month = normalizeMonth(qs("#filterMonth").value);

    const r = await fetch(`${API}/reports/monthly?month=${month}`, {
        headers: {
            "Authorization": `Bearer ${localStorage.getItem("token")}`
        }
    });
    const data = await r.json();

    qs("#reportTotal").textContent = data.total;

    qs("#reportCategories").innerHTML = data.breakdown
        .map(x => `<li>${x.category}: ₹${x.total}</li>`).join("");

    qs("#reportDaily").innerHTML = data.daily
        .map(x => `<li>${x.date}: ₹${x.total}</li>`).join("");
}


// ------------------- DASHBOARD SUMMARY -------------------
async function refreshDashboard() {
    const r = await fetch(`${API}/reports/monthly?month=${currentMonth}`, {
        headers: {
            "Authorization": `Bearer ${localStorage.getItem("token")}`
        }
    });
    const data = await r.json();

    qs("#totalMonth").textContent = data.total;
    qs("#avgDay").textContent = Math.round(data.total / 30);
}


// ------------------- LOGOUT -------------------
const logoutBtn = document.querySelector("#logoutBtn");

if (logoutBtn) {
    logoutBtn.onclick = () => {
        localStorage.removeItem("token");
        window.location.href = "login.html";
    };
}
