// API Endpoint Configuration
const PRODUCTION_API_URL = "https://mtu-elective-advisor-api.onrender.com";

const getApiBaseUrl = () => {
    // If running via file:// protocol or local addresses, default to local backend port
    if (window.location.hostname === "localhost" ||
        window.location.hostname === "127.0.0.1" ||
        window.location.hostname === "" ||
        window.location.protocol === "file:") {
        return "http://localhost:8000";
    }
    return PRODUCTION_API_URL;
};

// Global App State
let activeStudent = null;

// Page Initialization
document.addEventListener("DOMContentLoaded", () => {
    // Check if user session exists in localStorage
    const savedSession = localStorage.getItem("mtu_student_session");
    if (savedSession) {
        activeStudent = JSON.parse(savedSession);
        showDashboard();
    } else {
        showAuth();
    }

    // Background Animation Init
    initBackgroundAnimation();
});

// View Controllers
function showAuth() {
    document.getElementById("auth-panel").classList.add("active");
    document.getElementById("dashboard-panel").classList.add("hidden");
    document.getElementById("dashboard-panel").classList.remove("active");
    document.getElementById("user-nav").classList.add("hidden");
}

function showDashboard() {
    document.getElementById("auth-panel").classList.remove("active");
    document.getElementById("dashboard-panel").classList.remove("hidden");
    document.getElementById("dashboard-panel").classList.add("active");
    document.getElementById("user-nav").classList.remove("hidden");

    // Populate static details
    document.getElementById("nav-student-name").innerText = activeStudent.name;
    document.getElementById("student-name").innerText = `Welcome, ${activeStudent.name}`;
    document.getElementById("student-matric").innerText = formatMatric(activeStudent.matric_number);

    // Extract entry year
    const entrySuffix = activeStudent.matric_number.substring(0, 2);
    document.getElementById("student-admission").innerText = `20${entrySuffix} Academic Session`;

    // Set form fields
    document.getElementById("dash-career").value = activeStudent.career_goal;
    document.getElementById("dash-interests").value = activeStudent.interests.join(", ");

    // Fetch Recommendations
    fetchRecommendations();
}

// Format Matric Number for Display: AA-BB-CC-DD-EEE
function formatMatric(matric) {
    if (matric.length === 11) {
        return `${matric.substring(0, 2)}-${matric.substring(2, 4)}-${matric.substring(4, 6)}-${matric.substring(6, 8)}-${matric.substring(8)}`;
    }
    return matric;
}

// Switch Authentication Tabs
function switchAuthTab(tab) {
    const tabLogin = document.getElementById("tab-login");
    const tabSignup = document.getElementById("tab-signup");
    const formLogin = document.getElementById("form-login");
    const formSignup = document.getElementById("form-signup");

    if (tab === "login") {
        tabLogin.classList.add("active");
        tabSignup.classList.remove("active");
        formLogin.classList.add("active");
        formSignup.classList.remove("active");
    } else {
        tabLogin.classList.remove("active");
        tabSignup.classList.add("active");
        formLogin.classList.remove("active");
        formSignup.classList.add("active");
    }
}

// Handle Student Signup
async function handleSignup(e) {
    e.preventDefault();
    showLoader(true, "Registering student account...");

    const name = document.getElementById("signup-name").value;
    const matricRaw = document.getElementById("signup-matric").value;
    const password = document.getElementById("signup-password").value;
    const career = document.getElementById("signup-career").value;
    const interests = document.getElementById("signup-interests").value.split(",").map(i => i.trim()).filter(Boolean);

    const matric = matricRaw.replace(/-/g, "").trim();

    try {
        const response = await fetch(`${getApiBaseUrl()}/signup`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                name,
                matric_number: matric,
                password,
                career_goal: career,
                interests
            })
        });

        const data = await response.json();
        if (response.ok) {
            alert("Account created successfully! Please sign in.");
            switchAuthTab("login");
            document.getElementById("login-matric").value = matric;
            document.getElementById("form-signup").reset();
        } else {
            alert(data.detail || "Registration failed. Verify your matric number layout.");
        }
    } catch (err) {
        console.error(err);
        alert("Server error connecting to backend.");
    } finally {
        showLoader(false);
    }
}

// Handle Student Login
async function handleLogin(e) {
    e.preventDefault();
    showLoader(true, "Signing in...");

    const matricRaw = document.getElementById("login-matric").value;
    const password = document.getElementById("login-password").value;
    const matric = matricRaw.replace(/-/g, "").trim();

    try {
        const response = await fetch(`${getApiBaseUrl()}/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                matric_number: matric,
                password
            })
        });

        const data = await response.json();
        if (response.ok) {
            activeStudent = data;
            localStorage.setItem("mtu_student_session", JSON.stringify(data));
            showDashboard();
        } else {
            alert(data.detail || "Invalid matric number or password.");
        }
    } catch (err) {
        console.error(err);
        alert("Failed to connect to authentication gateway.");
    } finally {
        showLoader(false);
    }
}

// Fetch Recommended Electives
async function fetchRecommendations() {
    showLoader(true, "Generating course pathway...");

    try {
        const response = await fetch(`${getApiBaseUrl()}/recommend`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                matric_number: activeStudent.matric_number,
                career_goal: activeStudent.career_goal,
                interests: activeStudent.interests
            })
        });

        const data = await response.json();
        if (response.ok) {
            renderElectives(data);
        } else {
            alert(data.detail || "Could not fetch recommendations.");
        }
    } catch (err) {
        console.error(err);
        alert("Error loading elective courses.");
    } finally {
        showLoader(false);
    }
}

// Update Local Profile and Re-fetch Recommendations
async function updateProfileAndRecs() {
    const career = document.getElementById("dash-career").value;
    const interests = document.getElementById("dash-interests").value.split(",").map(i => i.trim()).filter(Boolean);

    // Update active student model (locally since SQLite keeps it synchronized, we just pass the parameters in recommendation request)
    activeStudent.career_goal = career;
    activeStudent.interests = interests;
    localStorage.setItem("mtu_student_session", JSON.stringify(activeStudent));

    fetchRecommendations();
}

// Render Recommendations to UI
function renderElectives(data) {
    const level = data.level;
    document.getElementById("student-level").innerText = `${level} Level`;

    const statusBanner = document.getElementById("api-status-banner");
    if (data.api_status === "fallback") {
        statusBanner.classList.remove("hidden");
    } else {
        statusBanner.classList.add("hidden");
    }

    const compulsoryBlock = document.getElementById("compulsory-block");
    const container = document.getElementById("electives-container");
    const siwesNotice = document.getElementById("siwes-notice");
    const sem2List = document.getElementById("sem-2-list");

    // Hide or show layout based on level
    if (level === 100) {
        compulsoryBlock.classList.remove("hidden");
        container.classList.add("hidden");
        return;
    } else {
        compulsoryBlock.classList.add("hidden");
        container.classList.remove("hidden");
    }

    // Handle SIWES for 300L
    if (level === 300) {
        siwesNotice.classList.remove("hidden");
        sem2List.classList.add("hidden");
    } else {
        siwesNotice.classList.add("hidden");
        sem2List.classList.remove("hidden");
    }

    // Populate lists
    const sem1List = document.getElementById("sem-1-list");
    sem1List.innerHTML = "";
    sem2List.innerHTML = "";

    const electives = data.electives || [];

    // Separate semesters
    const sem1Electives = electives.filter(e => e.semester === 1);
    const sem2Electives = electives.filter(e => e.semester === 2);

    if (sem1Electives.length === 0) {
        sem1List.innerHTML = `<div class="empty-list">No electives listed for first semester.</div>`;
    } else {
        sem1Electives.forEach(course => {
            sem1List.appendChild(createCourseCard(course));
        });
    }

    if (level !== 300) {
        if (sem2Electives.length === 0) {
            sem2List.innerHTML = `<div class="empty-list">No electives listed for second semester.</div>`;
        } else {
            sem2Electives.forEach(course => {
                sem2List.appendChild(createCourseCard(course));
            });
        }
    }
}

// Create a Styled Bento Course Card
function createCourseCard(course) {
    const card = document.createElement("div");
    card.className = "course-card";

    // Format match score badge
    let badgeClass = "badge-low";
    if (course.match_score > 60) badgeClass = "badge-high";
    else if (course.match_score > 30) badgeClass = "badge-med";

    card.innerHTML = `
        <div class="card-header">
            <span class="course-code">${course.code}</span>
            <span class="course-units">${course.units} Units</span>
        </div>
        <h4>${course.title}</h4>
        <p class="course-justification">💡 ${course.justification}</p>
        <div class="skills-box">
            <span class="skills-label">Covers:</span>
            <div class="skills-tags">
                ${course.skills.split(",").map(s => `<span class="skill-tag">${s.trim()}</span>`).join("")}
            </div>
        </div>
        <div class="relevance-score">
            <span>Relevance Match:</span>
            <span class="score-badge ${badgeClass}">${course.match_score}%</span>
        </div>
    `;
    return card;
}

// Logout System
function logout() {
    activeStudent = null;
    localStorage.removeItem("mtu_student_session");
    showAuth();
}

// Loader state controller
function showLoader(visible, message = "Loading...") {
    const overlay = document.getElementById("loading-overlay");
    const text = overlay.querySelector("p");
    if (text) text.innerText = message;
    if (visible) overlay.classList.remove("hidden");
    else overlay.classList.add("hidden");
}

// Dynamic particle backdrop renderer (neural vibe)
function initBackgroundAnimation() {
    const canvas = document.getElementById("bg-animation");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");

    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    window.addEventListener("resize", resize);
    resize();

    const particles = [];
    // Reduced particle count for performance optimization (less canvas load)
    for (let i = 0; i < 25; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            vx: (Math.random() - 0.5) * 0.4,
            vy: (Math.random() - 0.5) * 0.4,
            radius: Math.random() * 2
        });
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "rgba(187, 134, 252, 0.15)";

        particles.forEach(p => {
            p.x += p.vx;
            p.y += p.vy;

            if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
            if (p.y < 0 || p.y > canvas.height) p.vy *= -1;

            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fill();
        });

        // Connections drawing loop removed to completely eliminate GPU/compositor lag under glassmorphism
        requestAnimationFrame(draw);
    }
    draw();
}
