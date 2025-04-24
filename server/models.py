from pydantic import BaseModel, Field

class DataIngestionRequest(BaseModel):
    """
    Request model for ingesting data from a remote source.

    This model represents the input payload required to fetch the content 
    from a given URL, process the text content, generate vector embeddings 
    from it, and store the resulting embeddings in a vector database for 
    future semantic search and retrieval.
    """
    url: str = Field(
        ...,
        description=(
            "A publicly accessible URL pointing to a web page or document. "
            "The system will download the content from this URL, extract and clean the textual data, "
            "generate high-dimensional vector embeddings using a language model, "
            "and persist these embeddings in the vector database for semantic search operations."
        )
    )


class RetrieveDocumentRequest(BaseModel):
    """
    Request model for retrieving documents based on a semantic search query.

    This model encapsulates the user's natural language query which will be 
    transformed into vector form and used to search against the vector database 
    to find and return the most contextually relevant documents.
    """
    query: str = Field(
        ...,
        description=(
            "A natural language query provided by the user. "
            "This query will be converted into a vector representation and used "
            "to perform a similarity search against stored document embeddings "
            "in the vector database, retrieving the most relevant matches."
        )
    )