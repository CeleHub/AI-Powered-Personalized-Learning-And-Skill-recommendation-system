// State Management
let currentStep = 1;

// Deployment Configuration
// IMPORTANT: Once you deploy your backend to Render, replace the placeholder below with your Render URL
// Example: "https://your-api-name.onrender.com"
const PRODUCTION_API_URL = "https://ai-powered-personalized-learning-and.onrender.com";

const getApiBaseUrl = () => {
    if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") {
        return "http://localhost:8000";
    }
    return PRODUCTION_API_URL;
};

function nextStep(step) {
    document.getElementById(`step-${currentStep}`).classList.remove('active');
    document.getElementById(`step-${step}`).classList.add('active');

    // Update progress bar
    const steps = document.querySelectorAll('.progress-step');
    for (let i = 0; i < steps.length; i++) {
        if (i < step) {
            steps[i].classList.add('active');
        } else {
            steps[i].classList.remove('active');
        }
    }

    currentStep = step;
}

function prevStep(step) {
    nextStep(step);
}

function toggleAcademicFields() {
    const type = document.getElementById('academic-type').value;
    if (type === 'PRE_UNIVERSITY') {
        document.getElementById('pre-uni-fields').style.display = 'block';
        document.getElementById('uni-fields').style.display = 'none';
    } else {
        document.getElementById('pre-uni-fields').style.display = 'none';
        document.getElementById('uni-fields').style.display = 'block';
    }
}

async function submitProfile() {
    const loader = document.getElementById('loading');
    const finalizeBtn = document.getElementById('finalize-btn');

    loader.style.display = 'block';
    finalizeBtn.disabled = true;

    // Collect Data
    const name = document.getElementById('name').value;
    const academicType = document.getElementById('academic-type').value;
    const interests = document.getElementById('interests').value.split(',').map(i => i.trim());
    const careerGoal = document.getElementById('career-goal').value;

    let academicPerformance = {};
    if (academicType === 'PRE_UNIVERSITY') {
        const subjects = {
            "Mathematics": document.getElementById('math-grade').value,
            "English": document.getElementById('english-grade').value
        };
        // Parse extra subjects
        const extraText = document.getElementById('extra-subjects').value;
        if (extraText) {
            extraText.split(',').forEach(item => {
                const parts = item.split(':');
                if (parts.length === 2) {
                    subjects[parts[0].trim()] = parts[1].trim();
                }
            });
        }
        academicPerformance = { subjects };
    } else {
        academicPerformance = { gpa: document.getElementById('gpa').value };
    }

    // Parse skills
    const skillsText = document.getElementById('current-skills').value;
    const skills = skillsText.split(',').map(item => {
        const match = item.match(/(.+)\((.+)\)/);
        if (match) {
            return { name: match[1].trim(), level: match[2].trim() };
        }
        return { name: item.trim(), level: 'Beginner' };
    });

    const profile = {
        name,
        academic_type: academicType,
        academic_performance: academicPerformance,
        interests,
        career_goal: careerGoal,
        skills
    };

    try {
        const apiBaseUrl = getApiBaseUrl();
        const response = await fetch(`${apiBaseUrl}/recommend`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(profile)
        });

        const data = await response.json();
        renderResults(data);
    } catch (error) {
        console.error('Error:', error);
        alert('Could not connect to the backend server. Make sure it is running on port 8000.');
    } finally {
        loader.style.display = 'none';
        finalizeBtn.disabled = false;
    }
}

function renderResults(data) {
    const dashboard = document.getElementById('dashboard-content');
    dashboard.innerHTML = '';

    const statusBanner = document.getElementById('api-status-banner');
    if (data.api_status === 'fallback') {
        statusBanner.classList.remove('hidden');
    } else {
        statusBanner.classList.add('hidden');
    }

    document.getElementById('result-title').innerText = `Recommendations for ${data.user_name}`;

    // 1. Skill Gaps Card
    const skillCard = createBentoCard('Skill Roadmap', 'card-large');
    skillCard.innerHTML += `<p>Based on your goal, you need to focus on these skills:</p>`;
    const tagsDiv = document.createElement('div');
    tagsDiv.className = 'tags';
    data.target_skills.forEach(skill => {
        tagsDiv.innerHTML += `<span class="tag">${skill}</span>`;
    });
    skillCard.appendChild(tagsDiv);
    dashboard.appendChild(skillCard);

    // 2. University Recommendation Card (if exists)
    if (data.university_recommendation) {
        const uniCard = createBentoCard('University Pathway', '');
        uniCard.innerHTML += `<h3>${data.university_recommendation}</h3>`;
        uniCard.innerHTML += `<p class="${data.eligibility.eligible ? 'success' : 'error'}" style="color: ${data.eligibility.eligible ? 'var(--success-color)' : 'var(--error-color)'}; font-size: 0.8rem; margin-top: 10px;">
            ${data.eligibility.message}
        </p>`;
        dashboard.appendChild(uniCard);
    }

    // 3. Online Courses
    data.course_recommendations.forEach((course, index) => {
        const cardClass = index === 0 ? 'card-large' : '';
        const courseCard = createBentoCard(course.title, cardClass);
        courseCard.innerHTML += `
            <p style="font-size: 0.9rem; color: var(--text-secondary)">${course.provider} | ${course.duration}</p>
            <div class="tags" style="margin: 10px 0">
                <span class="tag" style="background: rgba(3, 218, 198, 0.1); border-color: rgba(3, 218, 198, 0.3); color: var(--success-color)">${course.difficulty}</span>
            </div>
            <p style="font-size: 0.8rem">${course.skills}</p>
        `;
        dashboard.appendChild(courseCard);
    });

    nextStep('result');
}

function createBentoCard(title, className) {
    const div = document.createElement('div');
    div.className = `bento-card ${className}`;
    div.innerHTML = `<h3>${title}</h3>`;
    return div;
}

// Background Animation
const canvas = document.getElementById('bg-animation');
const ctx = canvas.getContext('2d');

function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}

window.addEventListener('resize', resize);
resize();

const particles = [];
for (let i = 0; i < 50; i++) {
    particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        vx: (Math.random() - 0.5) * 0.5,
        vy: (Math.random() - 0.5) * 0.5,
        radius: Math.random() * 2
    });
}

function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = 'rgba(187, 134, 252, 0.2)';

    particles.forEach(p => {
        p.x += p.vx;
        p.y += p.vy;

        if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
        if (p.y < 0 || p.y > canvas.height) p.vy *= -1;

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fill();
    });

    requestAnimationFrame(animate);
}

animate();
