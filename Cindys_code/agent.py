# backend/agent.py
# This file implements a RAG (Retrieval-Augmented Generation) system for company FAQs
# using the BeeAI framework, ChromaDB for vector storage, and OpenAI for LLM responses.

import asyncio
import os
# Disable tokenizer parallelism to avoid warnings and potential conflicts
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from typing import List

# Import BeeAI framework components for building the agent system
from beeai_framework.backend.chat import ChatModel  # For LLM integration (OpenAI)
from beeai_framework.tools.tool import Tool  # Base class for creating tools
from beeai_framework.workflows.agent import AgentWorkflow, AgentWorkflowInput  # Workflow management
from beeai_framework.emitter.emitter import Emitter  # Event emission system
from pydantic import BaseModel, Field  # Data validation and schema definition

# Import external libraries for RAG functionality
from sentence_transformers import SentenceTransformer  # For creating text embeddings
import chromadb  # Vector database for storing and searching FAQ embeddings

# Configuration constants for the RAG system
EMBEDDING_MODEL_NAME = 'all-MiniLM-L6-v2'  # Lightweight but effective embedding model
CHROMA_PERSIST_PATH = "./my_chroma_db"  # Local path for ChromaDB storage
CHROMA_COLLECTION_NAME = "company_faqs"  # Collection name in ChromaDB

# Global variables to store initialized components (singleton pattern)
# These are initialized once and reused across multiple requests
_embedding_model = None  # SentenceTransformer model for creating embeddings
_chroma_collection = None  # ChromaDB collection for FAQ storage
_llm = None  # OpenAI chat model instance
_faq_tool_instance = None  # FAQTool instance for searching FAQs
_agent_workflow = None  # AgentWorkflow for orchestrating the FAQ agent

def _setup_rag_system():
    """
    Initializes all RAG system components and stores them globally.
    
    This function implements a singleton pattern - it only initializes components
    once and reuses them for subsequent requests, improving performance.
    
    Returns:
        bool: True if setup successful, False otherwise
    """
    global _embedding_model, _chroma_collection, _llm, _faq_tool_instance, _agent_workflow

    # Check if all components are already initialized
    if _embedding_model and _chroma_collection and _llm and _faq_tool_instance and _agent_workflow:
        print("RAG system already set up.")
        return True

    print("Setting up RAG system components...")
    
    # Step 1: Initialize the embedding model for converting text to vectors
    try:
        _embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        print("Embedding model loaded.")
    except Exception as e:
        print(f"Error loading embedding model: {e}")
        return False

    # Step 2: Initialize ChromaDB for vector storage and retrieval
    try:
        chroma_client = chromadb.PersistentClient(path=CHROMA_PERSIST_PATH)
        _chroma_collection = chroma_client.get_or_create_collection(name=CHROMA_COLLECTION_NAME)
        print(f"ChromaDB collection '{CHROMA_COLLECTION_NAME}' ready with {_chroma_collection.count()} documents.")
    except Exception as e:
        print(f"Error connecting to ChromaDB: {e}")
        return False

    # Step 3: Initialize the OpenAI LLM for generating responses
    try:
        _llm = ChatModel.from_name(os.environ.get("OPENAI_MODEL", "openai:gpt-4o"))
        print("OpenAI LLM initialized.")
    except Exception as e:
        print(f"Error initializing LLM: {e}")
        return False

    # Step 4: Create the FAQ tool instance that combines embedding and search
    _faq_tool_instance = FAQTool(embedding_model=_embedding_model, chroma_collection=_chroma_collection)
    print("FAQTool instance created.")

    # Step 5: Create the agent workflow that orchestrates the FAQ answering process
    _agent_workflow = AgentWorkflow(name="Company FAQ Assistant")
    _agent_workflow.add_agent(
        name="FAQAgent",
        role="An expert in company FAQs.",
        instructions=(
            "You are an expert in company FAQs. Your primary goal is to answer questions based on the provided company FAQ information. "
            "If company FAQ information is provided in the input, prioritize using it to answer the user's question. "
            "If no relevant company FAQ information is provided or found, state that you cannot find the answer in the company FAQs. "
            "Do NOT try to use the 'faq_lookup_tool' on your own if context is already provided, as the information has already been retrieved for you."
        ),
        tools=[_faq_tool_instance],  # Give the agent access to the FAQ search tool
        llm=_llm,  # Provide the LLM for generating responses
    )
    print("Agent workflow created and agent added.")
    return True

class FAQTool(Tool):
    """
    A custom tool that extends the BeeAI Tool class to provide FAQ search functionality.
    
    This tool uses semantic search to find relevant FAQ information by:
    1. Converting user queries to embeddings
    2. Searching the ChromaDB collection for similar FAQ embeddings
    3. Returning the most relevant FAQ content
    """
    
    # Tool metadata for the BeeAI framework
    name: str = "faq_lookup_tool"
    description: str = "Searches the company's frequently asked questions for relevant answers using semantic search. Use this tool when the user asks a question about company policies, products, or general FAQs. Input should be a question string."

    class FAQToolInput(BaseModel):
        """
        Input schema for the FAQ tool, defining the expected input structure.
        
        This ensures that the tool receives properly formatted input data.
        """
        query: str = Field(description="The question to lookup in the company FAQs.")

    @property
    def input_schema(self) -> type[BaseModel]:
        """Returns the input schema class for validation."""
        return self.FAQToolInput

    def _create_emitter(self) -> Emitter | None:
        """Creates an emitter for tracking tool execution events."""
        return Emitter()

    def __init__(self, embedding_model: SentenceTransformer, chroma_collection: chromadb.Collection):
        """
        Initialize the FAQ tool with required components.
        
        Args:
            embedding_model: Model for converting text to embeddings
            chroma_collection: ChromaDB collection containing FAQ data
        """
        super().__init__()
        self.embedding_model = embedding_model
        self.chroma_collection = chroma_collection

    async def _run(self, query: str) -> str:
        """
        Main execution method for the FAQ tool.
        
        This method performs semantic search by:
        1. Converting the query to embeddings
        2. Searching ChromaDB for similar FAQ content
        3. Formatting and returning the results
        
        Args:
            query: The user's question to search for
            
        Returns:
            str: Formatted FAQ information or error message
        """
        # Step 1: Convert the user query to embeddings for semantic search
        try:
            query_embedding = self.embedding_model.encode(query).tolist()
        except Exception as e:
            return f"Error processing query for FAQ lookup: {e}"

        # Step 2: Search ChromaDB for similar FAQ content using vector similarity
        try:
            results = self.chroma_collection.query(
                query_embeddings=[query_embedding],  # Search using the query embedding
                n_results=3,  # Return top 3 most similar results
                include=['documents', 'metadatas']  # Include both content and metadata
            )
        except Exception as e:
            return f"Error retrieving information from FAQs: {e}"

        # Step 3: Process and format the search results
        retrieved_contexts = []
        if results and results.get('documents') and results['documents'][0]:
            # Iterate through the retrieved documents and format them
            for i in range(len(results['documents'][0])):
                doc_content = results['documents'][0][i]  # The FAQ content
                metadata = results['metadatas'][0][i]     # Associated metadata
                question = metadata.get('question', 'N/A')  # Extract question from metadata
                answer = metadata.get('answer', doc_content)  # Extract answer or use content
                retrieved_contexts.append(f"Question: {question}\nAnswer: {answer}")

        # Step 4: Handle case where no relevant information is found
        if not retrieved_contexts:
            return "No relevant information found in the FAQs."

        # Step 5: Combine all retrieved contexts into a single formatted string
        context_string = "\n\n".join(retrieved_contexts)
        return context_string

async def run_faq_agent(user_query: str) -> str:
    """
    Main function to run the FAQ agent workflow.
    
    This function orchestrates the entire FAQ answering process:
    1. Ensures the RAG system is properly initialized
    2. Searches for relevant FAQ information
    3. Generates a comprehensive answer using the LLM
    
    Args:
        user_query: The user's question about company FAQs
        
    Returns:
        str: The agent's response to the user's question
    """
    # Ensure the RAG system is set up before processing
    if not _setup_rag_system():
        return "Backend RAG system failed to initialize. Please check server logs."

    # Step 1: Manually call the FAQ tool to retrieve relevant information
    print("Calling the faq_lookup_tool...")
    retrieved_info = await _faq_tool_instance._run(user_query)
   
    # Step 2: Build a comprehensive prompt combining retrieved info and user question
    # This gives the LLM context about relevant FAQs before asking it to answer
    prompt_for_agent = f"Retrieved Company FAQ Information:\n{retrieved_info}\n\nUser Question: {user_query}"

    # Step 3: Run the agent workflow to generate the final answer
    try:
        response = await _agent_workflow.run(
            inputs=[
                AgentWorkflowInput(
                    prompt=prompt_for_agent,  # Send the combined prompt to the agent
                )
            ]
        )
        return response.result.final_answer  # Extract the agent's response
    except Exception as e:
        print(f"Error running agent workflow: {e}")
        return f"An error occurred while processing your request: {e}"