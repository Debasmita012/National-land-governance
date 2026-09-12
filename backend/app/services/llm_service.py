import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


class LLMService:

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")

        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None

    def generate_grounded_answer(
        self,
        question: str,
        evidence_context: str
    ) -> str:
        """
        Generate an answer using the available LLM.

        If the LLM API is unavailable, return the retrieved
        evidence instead of failing.
        """

        if not question or not question.strip():
            raise ValueError("Question cannot be empty.")

        if not evidence_context or not evidence_context.strip():
            return "No supporting evidence was found."

        # --------------------------------------------------
        # FALLBACK MODE
        # --------------------------------------------------

        if self.client is None:
            return self._fallback_answer(
                evidence_context
            )

        # --------------------------------------------------
        # LLM MODE
        # --------------------------------------------------

        prompt = f"""
You are a research assistant for a national land-governance
decision-support platform.

Answer the user's question using ONLY the supplied evidence.

Do not invent facts.
Do not introduce information that is not supported by
the supplied evidence.

If the evidence is insufficient, explicitly say:

"The available evidence is insufficient to answer this."

Preserve uncertainty where appropriate.

USER QUESTION:
{question}

SUPPLIED EVIDENCE:
{evidence_context}

Provide a concise, evidence-grounded answer.

Refer to the supplied sources using:
[SOURCE 1], [SOURCE 2], etc.
"""

        try:

            response = self.client.responses.create(
                model="gpt-5.6-luna",
                input=prompt
            )

            return response.output_text

        except Exception as error:

            print(
                f"LLM unavailable. Using fallback mode: {error}"
            )

            return self._fallback_answer(
                evidence_context
            )

    def _fallback_answer(
        self,
        evidence_context: str
    ) -> str:
        """
        Evidence-only fallback when no LLM is available.
        """

        return (
            "LLM generation is currently unavailable. "
            "The following evidence was retrieved for the "
            "question:\n\n"
            + evidence_context
        )