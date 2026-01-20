"""
LangGraph-based multi-agent research pipeline.

NOTE:
All external capabilities (search, ranking, synthesis, evaluation)
are executed via an MCP server.

LangGraph + agents handle reasoning and control flow only.
"""

from dotenv import load_dotenv
load_dotenv()

import json
from langgraph.graph import StateGraph, END

from src.langgraph_state import DiscoveryState
from src.mcp_client import mcp
from src.agents.query_proposer import propose_search_queries



def initial_search_node(state: DiscoveryState):
    print("\n[DEBUG] Entering initial_search_node")

    records = (
        mcp.call_tool(
            "search_arxiv",
            {"query": state["topic"], "max_results": 15},
        )
        + mcp.call_tool(
            "search_semantic_scholar",
            {"query": state["topic"], "max_results": 15},
        )
    )

    print(f"[DEBUG] initial records collected = {len(records)}")

    return {
        "records": records,
        "iteration": 0,
        "pending_queries": [],
        "current_query_index": 0,
        "approved_query": None,
        "decision": None,
    }


def query_proposer_node(state: DiscoveryState):
    print("\n[DEBUG] Entering query_proposer_node")
    print(f"[DEBUG] iteration = {state['iteration']}")
    print(f"[DEBUG] total records = {len(state['records'])}")

    proposals = propose_search_queries(
        topic=state["topic"],
        papers=state["records"],
        max_queries=3,
    )

    print(f"[DEBUG] proposed {len(proposals)} new queries")

    return {
        "pending_queries": proposals,
        "current_query_index": 0,
        "approved_query": None,
        "decision": None,
    }


def human_decision_node(state: DiscoveryState):
    print("\n[DEBUG] Entering human_decision_node")
    print(f"[DEBUG] iteration = {state['iteration']}")
    print(f"[DEBUG] current_query_index = {state['current_query_index']}")
    print(f"[DEBUG] pending_queries = {len(state['pending_queries'])}")
    print(f"[DEBUG] decision (incoming) = {state.get('decision')}")

    idx = state["current_query_index"]
    proposals = state["pending_queries"]

    if idx >= len(proposals):
        print("[DEBUG] Batch exhausted → requesting new batch")
        return {"decision": "exhausted"}

    proposal = proposals[idx]

    print("\n===================================")
    print("Proposed search query:")
    print(proposal["query"])
    print("\nRationale:")
    print(proposal["rationale"])
    print("===================================")

    decision = input("Approve / Reject / Stop ? ").strip().lower()

    if decision == "approve":
        return {
            "approved_query": proposal["query"],
            "decision": "approve",
        }

    if decision == "reject":
        return {
            "current_query_index": idx + 1,
            "decision": "reject",
        }

    return {"decision": "stop"}


def search_executor_node(state: DiscoveryState):
    print("\n[DEBUG] Entering search_executor_node")
    print(f"[DEBUG] approved_query = {state['approved_query']}")

    query = state["approved_query"]
    if not query:
        print("[DEBUG] No approved query — skipping search")
        return {}

    new_records = (
        mcp.call_tool(
            "search_arxiv",
            {"query": query, "max_results": 10},
        )
        + mcp.call_tool(
            "search_semantic_scholar",
            {"query": query, "max_results": 10},
        )
    )

    print(f"[DEBUG] added {len(new_records)} new records")

    return {
        "records": state["records"] + new_records,
        "iteration": state["iteration"] + 1,
        "approved_query": None,
        "decision": None,
    }


def dedup_node(state: DiscoveryState):
    print("\n[DEBUG] Entering dedup_node")

    deduped = mcp.call_tool(
        "deduplicate_records",
        {"records": state["records"]},
    )

    print(f"[DEBUG] deduped records = {len(deduped)}")
    return {"deduped_records": deduped}


def ranking_node(state: DiscoveryState):
    print("\n[DEBUG] Entering ranking_node")

    ranked = mcp.call_tool(
        "rank_discovery_records",
        {"records": state["deduped_records"]},
    )

    return {"ranked_views": ranked}


def synthesis_node(state: DiscoveryState):
    print("\n[DEBUG] Entering synthesis_node")

    papers = (
        state["ranked_views"].get("top_all_time_cited", [])
        + state["ranked_views"].get("top_recent_cited", [])
    )

    print(f"[DEBUG] synthesizing from {len(papers)} papers")

    markdown = mcp.call_tool(
        "synthesize_from_abstracts",
        {
            "topic": state["topic"],
            "papers": papers,
        },
    )

    return {"synthesis_markdown": markdown}


def evaluation_node(state: DiscoveryState):
    print("\n[DEBUG] Entering evaluation_node")

    papers = (
        state["ranked_views"].get("top_all_time_cited", [])
        + state["ranked_views"].get("top_recent_cited", [])
    )

    evaluation = mcp.call_tool(
        "evaluate_synthesis",
        {
            "topic": state["topic"],
            "synthesis_markdown": state["synthesis_markdown"],
            "papers": papers,
        },
    )

    return {"evaluation_report": evaluation}



def build_discovery_graph():
    graph = StateGraph(DiscoveryState)

    graph.add_node("initial_search", initial_search_node)
    graph.add_node("query_proposer", query_proposer_node)
    graph.add_node("human_decision", human_decision_node)
    graph.add_node("search_executor", search_executor_node)
    graph.add_node("dedup", dedup_node)
    graph.add_node("rank", ranking_node)
    graph.add_node("synthesis", synthesis_node)
    graph.add_node("evaluation", evaluation_node)

    graph.set_entry_point("initial_search")

    graph.add_edge("initial_search", "query_proposer")
    graph.add_edge("query_proposer", "human_decision")

    graph.add_conditional_edges(
        "human_decision",
        lambda state: state["decision"],
        {
            "approve": "search_executor",
            "reject": "human_decision",
            "exhausted": "query_proposer",
            "stop": "dedup",
        },
    )

    graph.add_edge("search_executor", "query_proposer")

    graph.add_edge("dedup", "rank")
    graph.add_edge("rank", "synthesis")
    graph.add_edge("synthesis", "evaluation")
    graph.add_edge("evaluation", END)

    return graph.compile()



if __name__ == "__main__":
    graph = build_discovery_graph()

    result = graph.invoke(
        {
            "topic": "continual learning",
            "records": [],
            "iteration": 0,
            "max_iterations": 3,
        }
    )

    print("\n=========== FINAL SYNTHESIS ===========\n")
    print(result["synthesis_markdown"])

    print("\n=========== EVALUATION REPORT ===========\n")
    print(json.dumps(result["evaluation_report"], indent=2))
