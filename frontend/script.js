const API_URL = window.location.origin;

const totalInterviews = document.getElementById("totalInterviews");
const averageScore = document.getElementById("averageScore");
const highestScore = document.getElementById("highestScore");
const mostPracticedRole = document.getElementById("mostPracticedRole");
const roleSelect = document.getElementById("roleSelect");
const difficultySelect = document.getElementById("difficultySelect");
const generateButton = document.getElementById("generateButton");
const questionText = document.getElementById("questionText");
const questionDifficultyLabel = document.getElementById("questionDifficultyLabel");
const answerText = document.getElementById("answerText");
const characterCount = document.getElementById("characterCount");
const submitAnswerButton = document.getElementById("submitAnswerButton");
const evaluationStatus = document.getElementById("evaluationStatus");
const scoreText = document.getElementById("scoreText");
const scoreDisplay = document.getElementById("scoreDisplay");
const scoreProgressBar = document.getElementById("scoreProgressBar");
const feedbackText = document.getElementById("feedbackText");
const strengthsList = document.getElementById("strengthsList");
const improvementsList = document.getElementById("improvementsList");
const sampleAnswerText = document.getElementById("sampleAnswerText");
const feedbackSection = document.getElementById("feedbackSection");
const historyList = document.getElementById("historyList");
const historyMessage = document.getElementById("historyMessage");
const stepItems = [...document.querySelectorAll(".step-item")];

let currentQuestion = "";
let statusTimer = null;
const recentQuestions = new Map();

function setActiveStep(stepNumber) {
    stepItems.forEach((item, index) => {
        item.classList.toggle("active", index < stepNumber);
        item.classList.toggle("current", index === stepNumber - 1);
    });
}

function updateCharacterCount() {
    const count = answerText.value.length;
    characterCount.textContent = `${count.toLocaleString()} / 1,500 characters`;
    characterCount.classList.toggle("near-limit", count >= 1300);
}

function resetFeedback() {
    scoreText.textContent = "—";
    scoreProgressBar.style.width = "0%";
    scoreDisplay.className = "score-display";
    feedbackText.textContent = "Submit your answer to receive feedback.";
    strengthsList.innerHTML = "<li>No feedback yet.</li>";
    improvementsList.innerHTML = "<li>No feedback yet.</li>";
    sampleAnswerText.textContent = "A suggested answer will appear here.";
    feedbackSection.classList.remove("feedback-visible");
}

function setGenerateButtonLoading(isLoading) {
    const buttonText = generateButton.querySelector("span");
    generateButton.disabled = isLoading;
    generateButton.classList.toggle("is-loading", isLoading);
    buttonText.textContent = isLoading ? "Generating..." : "Generate Question";
}

function startEvaluationStatus() {
    const messages = [
        "Analyzing your answer...",
        "Checking technical accuracy...",
        "Reviewing clarity and completeness...",
        "Preparing personalized feedback...",
    ];
    let index = 0;
    evaluationStatus.textContent = messages[index];
    evaluationStatus.classList.add("visible");
    statusTimer = window.setInterval(() => {
        index = (index + 1) % messages.length;
        evaluationStatus.textContent = messages[index];
    }, 1400);
}

function stopEvaluationStatus() {
    if (statusTimer) window.clearInterval(statusTimer);
    statusTimer = null;
    evaluationStatus.classList.remove("visible");
    evaluationStatus.textContent = "";
}

function setSubmitButtonLoading(isLoading) {
    const buttonText = submitAnswerButton.querySelector("span:not(.button-shine)");
    submitAnswerButton.disabled = isLoading;
    submitAnswerButton.classList.toggle("is-loading", isLoading);
    buttonText.textContent = isLoading ? "Evaluating..." : "Evaluate My Answer";
    if (isLoading) startEvaluationStatus(); else stopEvaluationStatus();
}

function formatDate(dateValue) {
    const date = new Date(dateValue);
    if (Number.isNaN(date.getTime())) return "Unknown date";
    return date.toLocaleString([], {
        month: "short", day: "numeric", year: "numeric",
        hour: "numeric", minute: "2-digit",
    });
}

function getScoreLevel(score) {
    if (score >= 9) return "excellent";
    if (score >= 7) return "good";
    if (score >= 4) return "fair";
    return "low";
}

function renderScore(score, animate = true) {
    const safeScore = Math.max(0, Math.min(10, Number(score) || 0));
    const level = getScoreLevel(safeScore);

    let badge = "";

switch (level) {
    case "excellent":
        badge = "🏆 Excellent";
        break;
    case "good":
        badge = "✅ Good";
        break;
    case "fair":
        badge = "⚡ Fair";
        break;
    default:
        badge = "📘 Needs Practice";
}

    scoreDisplay.className = `score-display score-${level}`;
    scoreProgressBar.style.width = `${safeScore * 10}%`;

    if (!animate) {
scoreText.innerHTML = `
    <div class="score-number">${safeScore}/10</div>
<div class="score-percent">${safeScore * 10}%</div>
<div class="score-badge">${badge}</div>`;        return;
    }

    let current = 0;
    const duration = 650;
    const start = performance.now();
    function tick(now) {
        const progress = Math.min((now - start) / duration, 1);
        current = Math.round(safeScore * progress);
scoreText.innerHTML = `
    <div class="score-number">${current}/10</div>
<div class="score-percent">${current * 10}%</div>
<div class="score-badge">${badge}</div>`;        if (progress < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
}

function fillList(element, values, fallback) {
    element.innerHTML = "";
    const entries = Array.isArray(values) && values.length ? values : [fallback];
    entries.forEach((value) => {
        const item = document.createElement("li");
        item.textContent = value;
        element.appendChild(item);
    });
}

function animateQuestion() {
    const display = questionText.closest(".question-display");
    display.classList.remove("question-enter");
    void display.offsetWidth;
    display.classList.add("question-enter");
}

function animateCounter(element, target, suffix = "") {
    const numericTarget = Number(target) || 0;
    const start = performance.now();
    const duration = 700;
    function tick(now) {
        const progress = Math.min((now - start) / duration, 1);
        const value = numericTarget * progress;
        element.textContent = `${Number.isInteger(numericTarget) ? Math.round(value) : value.toFixed(1)}${suffix}`;
        if (progress < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
}

async function loadRoles() {
    try {
        const response = await fetch(`${API_URL}/roles`);
        if (!response.ok) throw new Error("Could not load interview roles.");
        const data = await response.json();
        roleSelect.innerHTML = '<option value="">Select a career path</option>';
        data.roles.forEach((role) => {
            const option = document.createElement("option");
            option.value = role;
            option.textContent = role;
            roleSelect.appendChild(option);
        });
    } catch (error) {
        questionText.textContent = error.message;
    }
}

async function generateQuestion() {
    const selectedRole = roleSelect.value;
    const selectedDifficulty = difficultySelect.value;
    if (!selectedRole) {
        questionText.textContent = "Please select an interview role.";
        animateQuestion();
        return;
    }

    setGenerateButtonLoading(true);
    try {
        const historyKey = `${selectedRole}:${selectedDifficulty}`;
        const excludedQuestions = recentQuestions.get(historyKey) || [];
        const response = await fetch(`${API_URL}/question`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                role: selectedRole,
                difficulty: selectedDifficulty,
                exclude_questions: excludedQuestions,
            }),
        });
        if (!response.ok) throw new Error("Could not generate a question.");
        const data = await response.json();
        currentQuestion = data.question;
        recentQuestions.set(
            historyKey,
            [...excludedQuestions, currentQuestion].slice(-10),
        );
        questionText.textContent = currentQuestion;
        questionDifficultyLabel.textContent = `${data.difficulty} difficulty`;
        animateQuestion();
        answerText.value = "";
        updateCharacterCount();
        resetFeedback();
        setActiveStep(2);
        answerText.focus();
    } catch (error) {
        questionText.textContent = error.message;
        animateQuestion();
    } finally {
        setGenerateButtonLoading(false);
    }
}

async function submitAnswer() {
    const selectedRole = roleSelect.value;
    const userAnswer = answerText.value.trim();
    if (!selectedRole) return void (feedbackText.textContent = "Please select an interview role.");
    if (!currentQuestion) return void (feedbackText.textContent = "Please generate a question first.");
    if (!userAnswer) return void (feedbackText.textContent = "Please enter an answer.");

    setSubmitButtonLoading(true);
    setActiveStep(3);
    try {
        const response = await fetch(`${API_URL}/feedback`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ role: selectedRole, question: currentQuestion, answer: userAnswer }),
        });
        if (!response.ok) throw new Error("Could not evaluate your answer.");
        const data = await response.json();
        renderScore(data.score);
        feedbackText.textContent = `${data.overall_feedback} Your answer contained ${data.word_count} words.`;
        fillList(strengthsList, data.strengths, "No specific strengths were returned.");
        fillList(improvementsList, data.improvements, "Add more detail and a practical example.");
        sampleAnswerText.textContent = data.sample_answer || "No suggested answer was returned.";
        feedbackSection.classList.add("feedback-visible");
        setActiveStep(4);
        feedbackSection.scrollIntoView({ behavior: "smooth", block: "start" });
        await Promise.all([loadHistory(), loadAnalytics()]);
    } catch (error) {
        feedbackText.textContent = error.message;
    } finally {
        setSubmitButtonLoading(false);
    }
}

function createHistoryCard(attempt, index) {
    const card = document.createElement("article");
    card.className = "history-item history-enter";
    card.style.animationDelay = `${Math.min(index * 70, 350)}ms`;

    const header = document.createElement("div");
    header.className = "history-item-header";
    const role = document.createElement("h4");
    role.textContent = attempt.role;
    const score = document.createElement("span");
    score.className = `history-score score-${getScoreLevel(Number(attempt.score))}`;
    score.textContent = `${attempt.score}/10`;
    header.append(role, score);

    const question = document.createElement("p");
    question.className = "history-question";
    question.textContent = attempt.question;
    const date = document.createElement("p");
    date.className = "history-date";
    date.textContent = formatDate(attempt.created_at);

    const actions = document.createElement("div");
    actions.className = "history-actions";
    const viewButton = document.createElement("button");
    viewButton.type = "button";
    viewButton.className = "history-view-button";
    viewButton.textContent = "View Details";
    viewButton.addEventListener("click", () => showHistoryDetails(attempt));
    const deleteButton = document.createElement("button");
    deleteButton.type = "button";
    deleteButton.className = "history-delete-button";
    deleteButton.textContent = "Delete";
    deleteButton.addEventListener("click", () => deleteHistoryItem(attempt.id, card));
    actions.append(viewButton, deleteButton);
    card.append(header, question, date, actions);
    return card;
}

function showHistorySkeletons() {
    historyList.innerHTML = "";
    for (let i = 0; i < 4; i += 1) {
        const skeleton = document.createElement("div");
        skeleton.className = "history-skeleton";
        skeleton.innerHTML = '<span></span><span></span><span></span>';
        historyList.appendChild(skeleton);
    }
}

async function loadHistory() {
    if (!historyList || !historyMessage) return;
    historyMessage.textContent = "Loading interview history...";
    showHistorySkeletons();
    try {
        const response = await fetch(`${API_URL}/history`);
        if (!response.ok) throw new Error("Could not load interview history.");
        const attempts = await response.json();
        historyList.innerHTML = "";
        if (!attempts.length) {
            historyMessage.textContent = "No interview attempts have been saved yet.";
            return;
        }
        historyMessage.textContent = "";
        attempts.forEach((attempt, index) => historyList.appendChild(createHistoryCard(attempt, index)));
    } catch (error) {
        historyList.innerHTML = "";
        historyMessage.textContent = error.message;
    }
}

function showHistoryDetails(attempt) {
    roleSelect.value = attempt.role;
    currentQuestion = attempt.question;
    questionText.textContent = attempt.question;
    answerText.value = attempt.answer || "";
    updateCharacterCount();
    renderScore(attempt.score, false);
    feedbackText.textContent = attempt.overall_feedback || "No overall feedback was saved.";
    fillList(strengthsList, attempt.strengths, "Detailed strengths were not saved for this attempt.");
    fillList(improvementsList, attempt.improvements, "Review the overall feedback and improve your answer.");
    sampleAnswerText.textContent = attempt.sample_answer || "Suggested answers were not stored for this attempt.";
    feedbackSection.classList.add("feedback-visible");
    setActiveStep(4);
    animateQuestion();
    feedbackSection.scrollIntoView({ behavior: "smooth", block: "start" });
}

async function deleteHistoryItem(attemptId, card) {
    if (!window.confirm("Are you sure you want to delete this interview attempt?")) return;
    try {
        const response = await fetch(`${API_URL}/history/${attemptId}`, { method: "DELETE" });
        if (!response.ok) throw new Error("Could not delete the interview attempt.");
        card.classList.add("history-removing");
        await new Promise((resolve) => setTimeout(resolve, 220));
        await Promise.all([loadHistory(), loadAnalytics()]);
    } catch (error) {
        historyMessage.textContent = error.message;
    }
}

async function loadAnalytics() {
    try {
        const response = await fetch(`${API_URL}/analytics`);
        if (!response.ok) throw new Error("Could not load analytics.");
        const data = await response.json();
        animateCounter(totalInterviews, data.total_interviews);
        animateCounter(averageScore, data.average_score, "/10");
        animateCounter(highestScore, data.highest_score, "/10");
        mostPracticedRole.textContent = data.most_practiced_role ?? "—";
    } catch (error) {
        console.error("Analytics error:", error);
    }
}

roleSelect.addEventListener("change", () => setActiveStep(roleSelect.value ? 1 : 0));
generateButton.addEventListener("click", generateQuestion);
submitAnswerButton.addEventListener("click", submitAnswer);
answerText.addEventListener("input", updateCharacterCount);
answerText.addEventListener("keydown", (event) => {
    if ((event.ctrlKey || event.metaKey) && event.key === "Enter") submitAnswer();
});

updateCharacterCount();
setActiveStep(1);
loadRoles();
loadHistory();
loadAnalytics();
