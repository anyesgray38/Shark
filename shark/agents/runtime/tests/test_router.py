from shark.agents.runtime.router import discover, route, validate_contract


def test_all_contracts_are_nonempty():
    agents = discover()
    assert agents
    assert all(not validate_contract(agent) for agent in agents.values())


def test_research_routes_to_research():
    names = [a.name for a in route("research XAUUSD macro and geopolitical evidence")]
    assert "research" in names


def test_design_routes_to_design():
    names = [a.name for a in route("build a Penpot trading dashboard")]
    assert "design" in names
