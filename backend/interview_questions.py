import random


DIFFICULTIES = ("Easy", "Medium", "Hard", "Mix")


QUESTIONS = {
    "Software Engineer": {
        "Easy": [
            "Explain what a REST API is.",
            "What is the difference between a list and a tuple in Python?",
            "What is object-oriented programming?",
            "Explain the difference between GET and POST requests.",
            "What is the purpose of version control?",
            "What is the difference between a class and an object?",
            "What is inheritance in object-oriented programming?",
            "What is encapsulation?",
            "What is an HTTP status code?",
            "What is the difference between frontend and backend development?",
        ],
        "Medium": [
            "What is polymorphism, and when is it useful?",
            "What is the difference between == and is in Python?",
            "What is exception handling, and why is it useful?",
            "Explain the difference between PUT and PATCH.",
            "What is dependency injection, and what problem does it solve?",
            "What is the purpose of a virtual environment in Python?",
            "What is the difference between synchronous and asynchronous code?",
            "What is database normalization, and why is it important?",
            "How would you debug an application that is not working correctly?",
            "How would you design and test a CRUD API endpoint?",
        ],
        "Hard": [
            "How would you identify and fix a performance bottleneck in a web API?",
            "Explain how database indexes improve reads and affect writes.",
            "How would you prevent race conditions when multiple requests update the same record?",
            "Describe how you would design a scalable URL-shortening service.",
            "How would you secure an API that handles sensitive user data?",
            "Explain the tradeoffs between a monolith and microservices.",
            "How would you make a distributed operation idempotent?",
            "What causes an N+1 query problem, and how would you resolve it?",
            "How would you add caching to an application without serving stale data incorrectly?",
            "Describe a safe strategy for deploying a database schema change with no downtime.",
        ],
    },
    "Data Analyst": {
        "Easy": [
            "What is the difference between INNER JOIN and LEFT JOIN?",
            "Explain the GROUP BY clause in SQL.",
            "What does a Pandas DataFrame represent?",
            "What is the difference between WHERE and HAVING in SQL?",
            "What is a primary key?",
            "What is a foreign key?",
            "What is the purpose of ORDER BY in SQL?",
            "What is the difference between mean, median, and mode?",
            "What is data cleaning?",
            "What is the difference between loc and iloc in Pandas?",
        ],
        "Medium": [
            "How do you handle missing data?",
            "What is the difference between DELETE, TRUNCATE, and DROP?",
            "How would you identify duplicate records in a dataset?",
            "What is standard deviation, and what does it tell you?",
            "What is the difference between correlation and causation?",
            "How do you validate the accuracy of a dataset?",
            "How do you decide whether to remove, cap, or keep an outlier?",
            "How would you explain a dashboard to a nontechnical stakeholder?",
            "Describe the steps you would take to analyze a new dataset.",
            "How would you use a SQL window function to rank results within each group?",
        ],
        "Hard": [
            "A KPI suddenly drops by 20%. How would you determine whether the change is real or a data issue?",
            "How would you design an A/B test and determine whether its result is statistically significant?",
            "How would you optimize a slow SQL query that joins several large tables?",
            "How would you build a reliable data-quality monitoring process for a recurring report?",
            "Explain selection bias and how it can lead to a misleading business conclusion.",
            "How would you choose between a star schema and a normalized model for analytics?",
            "How would you measure customer retention when users can become inactive and later return?",
            "Two dashboards report different values for the same KPI. How would you reconcile them?",
            "How would you forecast a metric with strong seasonality and limited historical data?",
            "Describe how you would translate an ambiguous business question into a reproducible analysis.",
        ],
    },
    "Business Analyst": {
        "Easy": [
            "What is SWOT analysis?",
            "How do you gather business requirements?",
            "What is the purpose of a KPI?",
            "What is a business requirements document?",
            "What is process mapping?",
            "What is a use case?",
            "What is gap analysis?",
            "What is stakeholder analysis?",
            "What is root-cause analysis?",
            "What is the purpose of user acceptance testing?",
        ],
        "Medium": [
            "Explain the difference between functional and non-functional requirements.",
            "How would you handle conflicting stakeholder requirements?",
            "How do you prioritize business requirements?",
            "How would you communicate a technical issue to a business stakeholder?",
            "What is the difference between a requirement and a solution?",
            "How do you determine whether a project was successful?",
            "Describe a time you improved a business process.",
            "How would you respond when project requirements change?",
            "What information should be included in a project status report?",
            "How do you ensure that requirements are clear and testable?",
        ],
        "Hard": [
            "How would you build a business case for a project whose benefits are difficult to quantify?",
            "A project is on schedule but stakeholders are dissatisfied. How would you diagnose the problem?",
            "How would you manage scope when an executive requests a major feature late in delivery?",
            "Describe how you would redesign a process that crosses several departments with competing goals.",
            "How would you define acceptance criteria for a complex workflow with multiple exceptions?",
            "How would you evaluate whether to build, buy, or improve an existing business system?",
            "A new system improves efficiency but adoption is low. How would you investigate and respond?",
            "How would you trace a regulatory requirement through design, implementation, and testing?",
            "How would you prioritize a backlog when value, risk, effort, and urgency point in different directions?",
            "How would you measure whether a process change created lasting improvement rather than a temporary gain?",
        ],
    },
}


def get_available_roles() -> list[str]:
    """Return all available interview roles."""
    return list(QUESTIONS.keys())


def get_available_difficulties() -> list[str]:
    """Return the supported difficulty choices."""
    return list(DIFFICULTIES)


def get_random_question(
    role: str,
    difficulty: str = "Mix",
    excluded_questions: list[str] | None = None,
) -> tuple[str, str] | None:
    """Return a question and its actual difficulty for the selected role."""
    role_questions = QUESTIONS.get(role)
    if not role_questions or difficulty not in DIFFICULTIES:
        return None

    selected_difficulty = (
        random.choice(DIFFICULTIES[:-1])
        if difficulty == "Mix"
        else difficulty
    )
    question_pool = role_questions[selected_difficulty]
    excluded = set(excluded_questions or [])
    available_questions = [
        question for question in question_pool
        if question not in excluded
    ]

    # Once every question in a level has appeared, start a fresh cycle.
    if not available_questions:
        available_questions = question_pool

    return random.choice(available_questions), selected_difficulty
