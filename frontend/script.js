const API_URL = "http://127.0.0.1:8000";


const totalInterviews =
    document.getElementById("totalInterviews");

const averageScore =
    document.getElementById("averageScore");

const highestScore =
    document.getElementById("highestScore");

const mostPracticedRole =
    document.getElementById("mostPracticedRole");

const roleSelect = document.getElementById("roleSelect");
const generateButton = document.getElementById("generateButton");
const questionText = document.getElementById("questionText");

const answerText = document.getElementById("answerText");
const submitAnswerButton =
    document.getElementById("submitAnswerButton");

const scoreText = document.getElementById("scoreText");
const feedbackText = document.getElementById("feedbackText");

const strengthsList = document.getElementById("strengthsList");
const improvementsList =
    document.getElementById("improvementsList");

const sampleAnswerText =
    document.getElementById("sampleAnswerText");

const feedbackSection =
    document.getElementById("feedbackSection");

const historyList =
    document.getElementById("historyList");

const historyMessage =
    document.getElementById("historyMessage");

let currentQuestion = "";


function resetFeedback() {
    scoreText.textContent = "—";

    feedbackText.textContent =
        "Submit your answer to receive feedback.";

    strengthsList.innerHTML =
        "<li>No feedback yet.</li>";

    improvementsList.innerHTML =
        "<li>No feedback yet.</li>";

    sampleAnswerText.textContent =
        "A suggested answer will appear here.";
}


function setGenerateButtonLoading(isLoading) {
    const buttonText =
        generateButton.querySelector("span");

    generateButton.disabled = isLoading;

    buttonText.textContent = isLoading
        ? "Loading..."
        : "Generate Question";
}


function setSubmitButtonLoading(isLoading) {
    const buttonText =
        submitAnswerButton.querySelector(
            "span:not(.button-shine)"
        );

    submitAnswerButton.disabled = isLoading;

    buttonText.textContent = isLoading
        ? "Evaluating..."
        : "Evaluate My Answer";
}


function formatDate(dateValue) {
    const date = new Date(dateValue);

    if (Number.isNaN(date.getTime())) {
        return "Unknown date";
    }

    return date.toLocaleString();
}


async function loadRoles() {
    try {
        const response = await fetch(`${API_URL}/roles`);

        if (!response.ok) {
            throw new Error(
                "Could not load interview roles."
            );
        }

        const data = await response.json();

        data.roles.forEach((role) => {
            const option =
                document.createElement("option");

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

    if (!selectedRole) {
        questionText.textContent =
            "Please select an interview role.";

        return;
    }

    setGenerateButtonLoading(true);

    try {
        const response = await fetch(
            `${API_URL}/question`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    role: selectedRole,
                }),
            }
        );

        if (!response.ok) {
            throw new Error(
                "Could not generate a question."
            );
        }

        const data = await response.json();

        currentQuestion = data.question;
        questionText.textContent = currentQuestion;

        answerText.value = "";

        resetFeedback();
    } catch (error) {
        questionText.textContent = error.message;
    } finally {
        setGenerateButtonLoading(false);
    }
}


async function submitAnswer() {
    const selectedRole = roleSelect.value;
    const userAnswer = answerText.value.trim();

    if (!selectedRole) {
        feedbackText.textContent =
            "Please select an interview role.";

        return;
    }

    if (!currentQuestion) {
        feedbackText.textContent =
            "Please generate a question first.";

        return;
    }

    if (!userAnswer) {
        feedbackText.textContent =
            "Please enter an answer.";

        return;
    }

    setSubmitButtonLoading(true);

    try {
        const response = await fetch(
            `${API_URL}/feedback`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    role: selectedRole,
                    question: currentQuestion,
                    answer: userAnswer,
                }),
            }
        );

        if (!response.ok) {
            throw new Error(
                "Could not evaluate your answer."
            );
        }

        const data = await response.json();

        scoreText.textContent = `${data.score}/10`;

        feedbackText.textContent =
            `${data.overall_feedback} ` +
            `Your answer contained ` +
            `${data.word_count} words.`;

        strengthsList.innerHTML = "";

        data.strengths.forEach((strength) => {
            const item =
                document.createElement("li");

            item.textContent = strength;
            strengthsList.appendChild(item);
        });

        improvementsList.innerHTML = "";

        data.improvements.forEach((improvement) => {
            const item =
                document.createElement("li");

            item.textContent = improvement;
            improvementsList.appendChild(item);
        });

        sampleAnswerText.textContent =
            data.sample_answer;

        feedbackSection.scrollIntoView({
            behavior: "smooth",
            block: "start",
        });

        await loadHistory();
await loadAnalytics();
    } catch (error) {
        feedbackText.textContent = error.message;
    } finally {
        setSubmitButtonLoading(false);
    }
}


function createHistoryCard(attempt) {
    const card = document.createElement("article");
    card.className = "history-item";

    const header = document.createElement("div");
    header.className = "history-item-header";

    const role = document.createElement("h4");
    role.textContent = attempt.role;

    const score = document.createElement("span");
    score.className = "history-score";
    score.textContent = `${attempt.score}/10`;

    header.appendChild(role);
    header.appendChild(score);

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

    viewButton.addEventListener("click", () => {
        showHistoryDetails(attempt);
    });

    const deleteButton = document.createElement("button");
    deleteButton.type = "button";
    deleteButton.className = "history-delete-button";
    deleteButton.textContent = "Delete";

    deleteButton.addEventListener("click", () => {
        deleteHistoryItem(attempt.id);
    });

    actions.appendChild(viewButton);
    actions.appendChild(deleteButton);

    card.appendChild(header);
    card.appendChild(question);
    card.appendChild(date);
    card.appendChild(actions);

    return card;
}


async function loadHistory() {
    if (!historyList || !historyMessage) {
        return;
    }

    historyMessage.textContent =
        "Loading interview history...";

    historyList.innerHTML = "";

    try {
        const response = await fetch(`${API_URL}/history`);

        if (!response.ok) {
            throw new Error(
                "Could not load interview history."
            );
        }

        const attempts = await response.json();

        if (attempts.length === 0) {
            historyMessage.textContent =
                "No interview attempts have been saved yet.";

            return;
        }

        historyMessage.textContent = "";

        attempts.forEach((attempt) => {
            const card = createHistoryCard(attempt);
            historyList.appendChild(card);
        });
    } catch (error) {
        historyMessage.textContent = error.message;
    }
}


function showHistoryDetails(attempt) {
    roleSelect.value = attempt.role;

    currentQuestion = attempt.question;
    questionText.textContent = attempt.question;
    answerText.value = attempt.answer;

    scoreText.textContent = `${attempt.score}/10`;
    feedbackText.textContent =
        attempt.overall_feedback;

    strengthsList.innerHTML =
        "<li>Detailed strengths were not saved for this attempt.</li>";

    improvementsList.innerHTML =
        "<li>Review the overall feedback and improve your answer.</li>";

    sampleAnswerText.textContent =
        "Suggested answers were not stored for this attempt.";

    feedbackSection.scrollIntoView({
        behavior: "smooth",
        block: "start",
    });
}


async function deleteHistoryItem(attemptId) {
    const confirmed = window.confirm(
        "Are you sure you want to delete this interview attempt?"
    );

    if (!confirmed) {
        return;
    }

    try {
        const response = await fetch(
            `${API_URL}/history/${attemptId}`,
            {
                method: "DELETE",
            }
        );

        if (!response.ok) {
            throw new Error(
                "Could not delete the interview attempt."
            );
        }

        await loadHistory();
        await loadAnalytics();
        
    } catch (error) {
        historyMessage.textContent = error.message;
    }
}


generateButton.addEventListener(
    "click",
    generateQuestion
);

submitAnswerButton.addEventListener(
    "click",
    submitAnswer
);


async function loadAnalytics() {
    try {
        const response = await fetch(
            `${API_URL}/analytics`
        );

        if (!response.ok) {
            throw new Error(
                "Could not load analytics."
            );
        }

        const data = await response.json();

        totalInterviews.textContent =
            data.total_interviews;

        averageScore.textContent =
            `${data.average_score}/10`;

        highestScore.textContent =
            `${data.highest_score}/10`;

        mostPracticedRole.textContent =
            data.most_practiced_role ?? "—";
    } catch (error) {
        console.error(
            "Analytics error:",
            error
        );
    }
}

loadRoles();
loadHistory();
loadAnalytics();