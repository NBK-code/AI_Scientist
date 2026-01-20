from typing import List, Optional, Literal
from pydantic import BaseModel, Field, HttpUrl


# ---- Core Discovery Record ----
class DiscoveryRecord(BaseModel):
    """
    Canonical representation of a discovered research artifact
    (paper, survey, blog, or benchmark).

    This schema is source-agnostic and is the fundamental data
    contract across the entire system.
    """

    title: str = Field(..., description="Title of the paper or resource")

    authors: List[str] = Field(
        default_factory=list,
        description="List of authors (empty if unknown)",
    )

    year: Optional[int] = Field(
        default=None,
        description="Year of publication (if available)",
        ge=1900,
    )

    type: Literal["survey", "paper", "blog", "benchmark"] = Field(
        ...,
        description="Type of the discovered resource",
    )

    source: Literal["arxiv", "semantic_scholar", "openalex", "duckduckgo"] = Field(
        ...,
        description="Source from which this record was retrieved",
    )

    citations: Optional[int] = Field(
        default=None,
        description="Citation count if available",
        ge=0,
    )

    url: HttpUrl = Field(
        ...,
        description="Canonical URL to the resource",
    )

    abstract_or_snippet: Optional[str] = Field(
        default=None,
        description="Abstract (papers) or snippet (blogs/search results)",
    )



class DiscoveryResult(BaseModel):
    """
    Output schema for the v0 literature discovery pipeline.
    """

    topic: str = Field(..., description="User-provided research topic")

    results: List[DiscoveryRecord] = Field(
        default_factory=list,
        description="Ranked list of discovered resources",
    )
