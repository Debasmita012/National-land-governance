from typing import Dict, List

from app.services.search_service import SearchService
from app.services.llm_service import LLMService


class RAGService:

    def __init__(self):
        self.search_service = SearchService()
        self.llm_service = LLMService()

    def retrieve_evidence(
        self,
        question: str,
        n_results: int = 5
    ) -> List[Dict]:

        if not question or not question.strip():
            raise ValueError("Question cannot be empty.")

        return self.search_service.search(
            query=question,
            n_results=n_results
        )

    def build_context(
        self,
        results: List[Dict]
    ) -> str:

        if not results:
            return "No supporting evidence was found."

        context_parts = []

        for index, result in enumerate(results, start=1):

            metadata = result.get("metadata", {})

            title = metadata.get(
                "document_title",
                "Unknown document"
            )

            document_id = metadata.get(
                "document_id",
                "Unknown"
            )

            chunk_index = metadata.get(
                "chunk_index",
                "Unknown"
            )

            text = result.get("text", "")

            context_parts.append(
                f"[SOURCE {index}]\n"
                f"Document: {title}\n"
                f"Document ID: {document_id}\n"
                f"Chunk: {chunk_index}\n"
                f"Evidence:\n{text}"
            )

        return "\n\n".join(context_parts)

    def answer(
        self,
        question: str,
        n_results: int = 5
    ) -> Dict:

        results = self.retrieve_evidence(
            question=question,
            n_results=n_results
        )

        context = self.build_context(results)

        answer = self.llm_service.generate_grounded_answer(
            question=question,
            evidence_context=context
        )

        citations = []

        for index, result in enumerate(results, start=1):

            metadata = result.get("metadata", {})

            citations.append(
    {
        "source_number": index,
        "document_id": metadata.get(
            "document_id"
        ),
        "document_title": metadata.get(
            "document_title"
        ),
        "chunk_index": metadata.get(
            "chunk_index"
        ),
        "distance": result.get(
            "distance"
        ),
        "evidence_text": result.get(
            "text",
            ""
        )
    }
)

        return {
            "question": question,
            "answer": answer,
            "citations": citations,
            "evidence_count": len(results)
        }