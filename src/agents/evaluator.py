import json
from typing import List, Dict
from openai import OpenAI

from src.schemas import DiscoveryRecord

client = OpenAI()

# --------------------------------------------------
# Prompts
# --------------------------------------------------

SYSTEM_PROMPT = """You are a senior research reviewer evaluating a literature review.

Your task is to ASSESS the QUALITY of the review, not to rewrite it.

Rules:
- Base your evaluation ONLY on the provided synthesis and paper abstracts.
- Do NOT introduce new content.
- Do NOT suggest specific papers.
- Do NOT rewrite or improve the synthesis.
- Be conservative: if evidence is weak or uneven, say so.
- Identify strengths, weaknesses, and missing areas.
- Your output MUST follow the required JSON schema exactly.
"""

USER_PROMPT_TEMPLATE = """Topic: {TOPIC}

Below is a synthesized literature review based on paper abstracts.

--- SYNTHESIS ---
{SYNTHESIS}
------------------

The synthesis was based on the following papers:

{PAPERS_BLOCK}

Evaluate the synthesis using the following required JSON schema:

{{
  "overall_quality": "high | medium | low",
  "coverage": {{
    "historical_foundations": "good | partial | weak",
    "recent_advances": "good | partial | weak",
    "methodological_diversity": "good | partial | weak"
  }},
  "evidence_sufficiency": "sufficient | borderline | insufficient",
  "coherence": "clear | uneven | unclear",
  "missing_or_weak_areas": [
    "string"
  ],
  "confidence_explanation": "3–5 sentence explanation summarizing the assessment"
}}

Return ONLY valid JSON. Do not include any extra text.
"""


# --------------------------------------------------
# Evaluator Agent
# --------------------------------------------------

def evaluate_synthesis(
    topic: str,
    synthesis_markdown: str,
    papers: List[DiscoveryRecord],
) -> Dict:
    """
    Evaluates the quality of a synthesized literature review.

    Returns a structured evaluation report with explicit quality metrics.
    """

    papers_block = []
    for p in papers:
        block = f"""Title: {p.title}
Year: {p.year}
Citations: {p.citations}
Abstract: {p.abstract_or_snippet or "N/A"}
"""
        papers_block.append(block)

    user_prompt = USER_PROMPT_TEMPLATE.format(
        TOPIC=topic,
        SYNTHESIS=synthesis_markdown,
        PAPERS_BLOCK="\n".join(papers_block),
    )

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )

    # Strict JSON parse (fail loudly if malformed)
    content = response.choices[0].message.content
    return json.loads(content)
