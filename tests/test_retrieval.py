from app.components.hybrid_retriever import HybridRetriever


def test_hybrid_retriever_placeholder_roundtrip() -> None:
    retriever = HybridRetriever()
    assert retriever.retrieve("hello") == ["hello"]
