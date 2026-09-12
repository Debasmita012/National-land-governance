from app.services.rag_service import RAGService


rag_service = RAGService()


question = (
    "What are the major challenges "
    "in land governance in India?"
)


result = rag_service.answer(
    question=question,
    n_results=3
)


print("\nQUESTION")
print("=" * 60)
print(result["question"])


print("\nRETRIEVED EVIDENCE")
print("=" * 60)
print(result["evidence_context"])


print("\nCITATIONS")
print("=" * 60)

for citation in result["citations"]:
    print(citation)