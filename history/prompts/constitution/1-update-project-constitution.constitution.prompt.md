---
id: 1
title: Update Project Constitution
stage: constitution
date: 2025-12-25
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 1-vla-cognitive-behavior
user: DELL
command: /sp.constitution
labels: [constitution, project-setup, governance]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
 - .specify/templates/plan-template.md
 - .specify/templates/spec-template.md
 - .specify/templates/tasks-template.md
tests:
 - none
---

## Prompt

```text
/sp.constitution

Project: Unified AI/Spec-Driven Book with Integrated RAG Chatbot

Core principles:

Accuracy: Ensure all book content and chatbot answers are factually correct and verifiable.

Clarity: Content must be clear, engaging, and accessible to developers, AI enthusiasts, and technical readers.

Consistency: Follow a unified structure and style across the book, including headings, examples, and code snippets.

RAG fidelity: Chatbot must only provide answers based on the book content or user-selected text; hallucinations are unacceptable.

Reproducibility: All technical steps, code snippets, and instructions must be executable as documented.

Key standards:

Content writing: Use Spec-Kit Plus and Claude Code to generate book chapters.

Citation & references: Where external sources are used, document them clearly (preferably markdown links or footnotes).

Chatbot integration: Use OpenAI Agents/ChatKit SDK, FastAPI, Neon Serverless Postgres, and Qdrant Cloud; RAG must fetch answers reliably.

Code quality: All embedded code should follow best practices and be runnable in examples provided.

Deployment: Book must be ready for deployment via Docusaurus to GitHub Pages.

Constraints:

Book length: Minimum 150 pages or equivalent content in markdown.

Chapter structure: Logical flow from fundamentals → advanced topics → examples → RAG chatbot integration.

Interactivity: Embed working code snippets, examples, and chatbot interface references.

Deployment-ready: Ensure all configurations, assets, and instructions are production-ready for GitHub Pages.

Success criteria:

Fully written and reviewed book with consistent style and technical accuracy.

Integrated RAG chatbot answers all content-related questions accurately.

Book deployable to GitHub Pages without errors.

Code examples execute successfully as documented.

All references and sources properly documented; no plagiarism or inaccuracies.
```

## Response snapshot

Constitution file created with project-specific principles and governance structure. Updated related templates to ensure consistency with the new constitution.

## Outcome

- ✅ Impact: Created project constitution with 6 core principles and governance structure
- 🧪 Tests: none
- 📁 Files: Updated constitution.md and 3 template files
- 🔁 Next prompts: Continue with project planning and specification
- 🧠 Reflection: Constitution now provides clear governance framework for the AI/Spec-Driven Book project

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A