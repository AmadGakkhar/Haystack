import os
from dotenv import load_dotenv
from haystack import Pipeline
from haystack.utils.auth import Secret
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.converters import PyPDFToDocument
from haystack.components.preprocessors import DocumentCleaner, DocumentSplitter
from haystack.components.writers import DocumentWriter
from haystack_integrations.components.embedders.cohere import CohereDocumentEmbedder

# components: classes that are used as building blocks for pipelines.
# Examples include Converters, DocumentStores, Retrievers, Routers, and Readers.
# nodes: objects that are used to build the pipeline. Can be either a Component or a Pipeline itself.


class DataIngestion:
    def __init__(self):
        """
        Initialize the DataIngestion object.

        This method initializes the following instance variables for the DataIngestion object:

        - self.cleaner: A DocumentCleaner object to clean the text.
        - self.splitter: A DocumentSplitter object to split the text into documents.
        - self.converter: A PyPDFToDocument converter to convert the PDF into a Haystack document.
        - self.embedder: A CohereDocumentEmbedder to generate embeddings for the documents.
        - self.document_store: An InMemoryDocumentStore to store the documents.
        - self.writer: A DocumentWriter to write the documents to the document store.
        """
        self.cleaner = DocumentCleaner(
            remove_empty_lines=True,
            remove_extra_whitespaces=True,
            remove_repeated_substrings=True,
        )
        self.splitter = DocumentSplitter(
            split_by="word", split_overlap=10, split_length=200
        )
        self.converter = PyPDFToDocument()
        self.embedder = CohereDocumentEmbedder()
        self.document_store = InMemoryDocumentStore()
        self.writer = DocumentWriter(self.document_store)

    def get_indexing_pipeline(self):
        """
        Create and return an indexing pipeline.

        This method creates an indexing pipeline by instantiating a Pipeline object, adding the components and connecting them.

        Returns:
            Pipeline: The created pipeline.
        """
        self.pipeline = Pipeline()
        self.pipeline.add_component("converter", self.converter)
        self.pipeline.add_component("cleaner", self.cleaner)
        self.pipeline.add_component("splitter", self.splitter)
        self.pipeline.add_component("embedder", self.embedder)
        self.pipeline.add_component("writer", self.writer)

        self.pipeline.connect("converter", "cleaner")
        self.pipeline.connect("cleaner", "splitter")
        self.pipeline.connect("splitter", "embedder")
        self.pipeline.connect("embedder", "writer")

        return self.pipeline

    def save_ds(self):
        """
        Save the document store to disk.

        This method saves the document store to disk, which stores the documents that have been processed.

        The document store is saved to the "./artifacts/document_store" directory.
        """
        self.document_store.save_to_disk("./artifacts/document_store")

    def load_ds(self, path):
        return InMemoryDocumentStore().load_from_disk(path)

    def run(self):
        """
        Run the indexing pipeline.

        This method runs the indexing pipeline, which processes the documents in the document store and saves the embeddings to disk.

        The pipeline is run with a single source, which is the "sample_pdf.pdf" file in the "./data" directory.
        """
        pipeline = self.get_indexing_pipeline()
        pipeline.run(
            {
                "sources": [os.path.join("data", "sample_pdf.pdf")],
            }
        )
        self.save_ds()


if __name__ == "__main__":
    load_dotenv()
    ingestion = DataIngestion()
    ingestion.run()
    ingestion.load_ds("./artifacts/document_store")
    print("Doc store load successful")
