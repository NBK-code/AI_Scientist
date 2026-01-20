from typing import List
from openai import OpenAI

from src.schemas import DiscoveryRecord

# -----------------------------
# Prompts
# -----------------------------

SYSTEM_PROMPT = """You are an expert research scientist writing a literature review.

Rules you must follow strictly:
- Use ONLY the provided paper abstracts and metadata.
- Do NOT use any external knowledge.
- Do NOT invent papers, results, or citations.
- Cite papers using numeric references [n] corresponding to the provided IDs.
- Ignore papers whose abstracts are vague or uninformative.
- Prefer historically influential and highly cited papers when discussing foundations.
- Prefer recent papers when discussing the current state of the art.
- If the abstracts do not support a claim, do not make that claim.
"""

USER_PROMPT_TEMPLATE = """Topic: {TOPIC}

You are given a set of academic papers related to the topic above.
Each paper is identified by a numeric ID.

Using ONLY the information in the abstracts and metadata provided below,
write a concise literature review with the following structure:

## Overview
Briefly describe the research area and its overall goal.

## Historical Development
Describe how the field evolved over time.
Focus on early and foundational ideas.

## Key Milestones
List and explain major conceptual or methodological milestones.
Cite the relevant papers using [n].

## Current State of the Art
Summarize the dominant approaches and trends in recent years.

## Open Directions
Based strictly on limitations or gaps mentioned in the abstracts,
outline possible future research directions.

## References
List all cited papers in numeric order using the format:
[n] Title (Year)

Here are the papers:

{PAPERS_BLOCK}
"""

# -----------------------------
# LLM Interface
# -----------------------------

client = OpenAI()


def synthesize_literature_from_abstracts(
    topic: str,
    papers: List[DiscoveryRecord],
    model: str = "gpt-4.1-mini",
) -> str:
    """
    Generate a structured markdown literature review from paper abstracts.

    Args:
        topic: Research topic.
        papers: List of DiscoveryRecord objects (abstracts only).
        model: OpenAI model name.

    Returns:
        Markdown-formatted literature review.
    """

    # Build paper block with numeric IDs
    paper_blocks = []
    for idx, p in enumerate(papers, start=1):
        if not p.abstract_or_snippet:
            continue

        paper_blocks.append(
            f"""[{idx}]
Title: {p.title}
Authors: {", ".join(p.authors)}
Year: {p.year}
Citations: {p.citations}
Abstract: {p.abstract_or_snippet}
"""
        )

    user_prompt = USER_PROMPT_TEMPLATE.format(
        TOPIC=topic,
        PAPERS_BLOCK="\n".join(paper_blocks),
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content
