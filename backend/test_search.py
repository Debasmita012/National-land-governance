from app.services.search_service import SearchService


search_service = SearchService()


query = "What are the major challenges in land governance in India?"


results = search_service.search(
    query=query,
    n_results=3
)


print("\nSEARCH QUERY")
print("=" * 60)
print(query)


print("\nSEARCH RESULTS")
print("=" * 60)


for index, result in enumerate(results, start=1):

    print(f"\nRESULT {index}")
    print("-" * 60)

    print("Document:")
    print(result["metadata"]["document_title"])

    print("\nChunk:")
    print(result["text"][:1000])

    print("\nDistance:")
    print(result["distance"])