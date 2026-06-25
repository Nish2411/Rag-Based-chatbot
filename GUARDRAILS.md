**Version:** `v1.0.0`

# Guardrails.md

## Overview
This document defines the **Safety guardrails** implemented in the PDF-RAG-CHATBOT to ensure safe, ethical, and responsible usage.

## Core Principles

- **Truthfulness**: Prioritize information from the PDF when available
- **Safety First**: Never assist with harmful, illegal, or unethical requests
- **Transparency**: Clearly communicate when answering outside the document
- **Respectfulness**: Maintain professional and inclusive tone at all times

## Allowed Behaviour

- Answer questions related to Deep Learning concepts from the PDF
- Explain technical topics with examples and analogies
- Provide page citations when rferencing the documents
- Answer general AI/ML questions using its knowledge
- Politely redirect users to relevant topics in the book

## Prohibited Topics & Responses

The chatbot **must refuse** or **heavily restrict** responses on the following:

- **Harmful Content**: Violence, self-harm, hate speech, discrimination
- **Illegal Activities**: Hacking, piracy, drug manufacturing, etc.
- **Misinformation**: Deliberately creating false technical information
- **Personal Data**: Requests involving real personal information
- **Jailbreaking**: Attempts to override system instructions

**Response Strategy for Unsafe Queries:**
- Give a short, polite refusal
- Explain that the request violates usage policies
- Optionally suggest a safer, related topic

## Technical Guardrails Implemented

- **Input Validation**: Basic sanitization of user queries
- **Context Grounding**: RAG system encourages answers based on retrieved chunks
- **Citation Requirement**: Forces model to cite pages when using PDF content
- **Fallback Handling**: Graceful response when no relevant chunks are found
- **Model Safety**: Using Gemini 2.5 Flash with safety settings enabled

## Response Guidelines

| Scenario                        | Response Approach                          |
|-------------------------------|--------------------------------------------|
| Clear PDF-related question     | Answer with citation (`[Page X]`)         |
| Partially related question     | Use PDF context first, then general knowledge |
| Completely off-topic           | Answer normally but mention limitation    |
| Harmful / Unsafe query         | Polite refusal + short explanation        |
| Ambiguous question             | Ask for clarification