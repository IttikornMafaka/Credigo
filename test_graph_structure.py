from agent.graph import graph


def test_graph_nodes():

    nodes = set(graph.get_graph().nodes.keys())

    expected_nodes = {
        "retrieve_customer",
        "validation",
        "prediction",
        "policy_retrieval",
        "evidence_aggregation",
        "analysis",
        "reflection",
        "policy_assessment",
        "evidence_builder",
        "credit_risk_report",
        "report_validation",
    }

    assert expected_nodes.issubset(nodes)


def test_graph_can_be_compiled():

    assert graph is not None