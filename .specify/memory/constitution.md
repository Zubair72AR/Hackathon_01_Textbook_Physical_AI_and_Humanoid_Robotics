<!-- SYNC IMPACT REPORT
Version change: 1.0.0 → 1.1.0
Modified principles: [PRINCIPLE_1_NAME] → Accuracy, [PRINCIPLE_2_NAME] → Clarity, [PRINCIPLE_3_NAME] → Consistency, [PRINCIPLE_4_NAME] → RAG Fidelity, [PRINCIPLE_5_NAME] → Reproducibility
Added sections: Core Principles (completely redefined), Key Standards, Constraints, Success Criteria
Removed sections: Placeholder principle sections
Templates requiring updates: ⚠ pending - .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
Follow-up TODOs: None
-->

# Unified AI/Spec-Driven Book with Integrated RAG Chatbot Constitution

## Core Principles

### Accuracy
All book content and chatbot answers must be factually correct and verifiable. Information presented must be based on reliable sources, properly cited, and subject to verification. No unverified claims or speculative content should be included in the book or chatbot responses.

### Clarity
Content must be clear, engaging, and accessible to developers, AI enthusiasts, and technical readers. All explanations should be structured to maximize understanding, with appropriate examples, diagrams, and progressive complexity. Technical concepts should be explained in approachable language without sacrificing accuracy.

### Consistency
Follow a unified structure and style across the book, including headings, examples, and code snippets. All content must maintain consistent formatting, terminology, and presentation style. Code examples and technical instructions should follow the same patterns throughout the entire book and chatbot integration.

### RAG Fidelity
Chatbot must only provide answers based on the book content or user-selected text; hallucinations are unacceptable. The RAG system must strictly adhere to retrieving and referencing only the provided book content, with clear attribution and no fabrication of information.

### Reproducibility
All technical steps, code snippets, and instructions must be executable as documented. Every example, tutorial, and technical procedure must be tested and verified to work as described. Dependencies, environment setup, and execution steps must be complete and accurate.

### Technical Excellence
All embedded code should follow best practices and be runnable in examples provided. Code snippets must be well-documented, maintainable, and demonstrate proper implementation patterns. All technical components must meet professional standards for production readiness.

## Key Standards

Content writing: Use Spec-Kit Plus and Claude Code to generate book chapters. Citation & references: Where external sources are used, document them clearly (preferably markdown links or footnotes). Chatbot integration: Use OpenAI Agents/ChatKit SDK, FastAPI, Neon Serverless Postgres, and Qdrant Cloud; RAG must fetch answers reliably. Code quality: All embedded code should follow best practices and be runnable in examples provided. Deployment: Book must be ready for deployment via Docusaurus to GitHub Pages.

## Constraints

Book length: Minimum 150 pages or equivalent content in markdown. Chapter structure: Logical flow from fundamentals → advanced topics → examples → RAG chatbot integration. Interactivity: Embed working code snippets, examples, and chatbot interface references. Deployment-ready: Ensure all configurations, assets, and instructions are production-ready for GitHub Pages.

## Success Criteria

Fully written and reviewed book with consistent style and technical accuracy. Integrated RAG chatbot answers all content-related questions accurately. Book deployable to GitHub Pages without errors. Code examples execute successfully as documented. All references and sources properly documented; no plagiarism or inaccuracies.

## Governance

This constitution serves as the foundational governance document for the Unified AI/Spec-Driven Book with Integrated RAG Chatbot project. All development, content creation, and technical decisions must align with these principles. Any changes to the core principles require explicit approval and documentation of the rationale. All team members and contributors must acknowledge and adhere to these principles.

**Version**: 1.1.0 | **Ratified**: 2025-12-25 | **Last Amended**: 2025-12-25