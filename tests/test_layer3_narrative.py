from layer3_communication import generate_narrative


def test_narrative():
    s = generate_narrative({"topic": "astro", "score": 1.23})
    assert "astro" in s and "1.23" in s
