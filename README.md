# rag_demo
demonstration of RAG using Project2025 data

WANT:

[starting with a very easy query byper tailored to the text]

Human Query: "What does project 2025 say about BLMs move west and how it saved money but effective management returned to D.C."

Augmented Query: "What does project 2025 say about BLMs move west and how it saved money but effective management returned to D.C., given the following chunk pulled from project 2025 pdf: {(insert from paeg 526)}"

(info from Page Page 559 — 526 - from p2025.txt)

DB Return: 526
GPT Reutn: " Project 2025 states that the Bureau of Land Management's (BLM) move west saved $3.5 million in 2022, projected to increase to $10.3 million the following year, which could be used for wildfire risk reduction, recreational opportunities, and conservation efforts. However, it criticizes the Biden Administration for returning senior employees to Washington, D.C., arguing that effective management and responsiveness have been lost as key leaders are no longer close to the field operations in the West, thereby undermining the benefits of the original move."

