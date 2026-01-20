from typing import List
from openai import OpenAI
from src.schemas import DiscoveryRecord

client = OpenAI()

SYSTEM_PROMPT = """You are a research scientist assisting a human researcher.

Your task is to propose NEW literature search queries.

Rules:
- Use ONLY the provided abstracts and metadata.
- Do NOT repeat the original topic verbatim.
- Do NOT propose overly broad queries.
- Propose specific, research-oriented queries.
- Explain why each query is relevant based on gaps or underexplored themes.
- Do NOT execute searches.
"""

USER_PROMPT_TEMPLATE = """Original topic: {TOPIC}

Based on the following paper abstracts, propose up to {MAX_QUERIES}
new literature search queries.

For each query, provide:
- "query"
- "rationale" (3–4 lines)

Return ONLY valid JSON (a list of objects).

Papers:
{PAPERS_BLOCK}
"""


def propose_search_queries(
    topic: str,
    papers: List[DiscoveryRecord],
    max_queries: int = 3,
) -> List[dict]:
    papers_block = []
    for p in papers:
        if not p.abstract_or_snippet:
            continue
        papers_block.append(
            f"""Title: {p.title}
Year: {p.year}
Citations: {p.citations}
Abstract: {p.abstract_or_snippet}
"""
        )

    user_prompt = USER_PROMPT_TEMPLATE.format(
        TOPIC=topic,
        MAX_QUERIES=max_queries,
        PAPERS_BLOCK="\n".join(papers_block),
    )

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
    )

    return eval(response.choices[0].message.content)
