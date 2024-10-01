from haystack import Pipeline
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.components.builders import PromptBuilder
from haystack_integrations.components.embedders.cohere import CohereTextEmbedder
from haystack.components.generators import OpenAIGenerator
from haystack.utils.auth import Secret
from haystack.document_stores.in_memory import InMemoryDocumentStore
from raghaystack.prompts.simple_prompt import PROMPT


class Inference:
    def __init__(self, doc_store_path: str):
        self.doc_store_path = doc_store_path
        self.pipeline = Pipeline()
        self.retriever = InMemoryEmbeddingRetriever(
            document_store=InMemoryDocumentStore().load_from_disk(doc_store_path)
        )
        self.prompt_builder = PromptBuilder()
        self.query_embedder = CohereTextEmbedder()
        self.llm = OpenAIGenerator(
            api_key=Secret.from_env_var("GROQ_API_KEY"),
            api_base_url="https://api.groq.com/openai/v1",
            model="llama3-8b-8192",
            generation_kwargs={"max_tokens": 512},
        )

    def get_pipeline(self):
        self.pipeline.add_component("retriever", self.retriever),
        self.pipeline.add_component("query_embedder", self.query_embedder)
        self.pipeline.add_component("prompt_builder", self.prompt_builder)
        self.pipeline.add_component("llm", self.llm)

        self.pipeline.connect("query_embedder.embedding", "retriever.query_embedding")
        self.pipeline.connect("retriever.documents", "prompt_builder.documents")
        self.pipeline.connect("prompt_builder", "llm.prompt")

        return self.pipeline

    def get_docs(self, path):
        self.doc_store.load_from_disk(path=path)
        return self.doc_store

    def run(self, query: str):
        pipeline = self.get_pipeline()
        result = pipeline.run(
            {
                "query_embedder": {"text": query},
                "retriever": {"top_k": 1},
                "prompt": {"query": query},
            }
        )

        print(result["llm"]["replies"][0])


if __name__ == "__main__":
    inference = Inference(
        doc_store_path="/home/amadgakkhar/code/Haystack/data/sample_pdf.pdf"
    )
    inference.run("Who is the author")
