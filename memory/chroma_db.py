import os
import chromadb
import logging
from config.settings import DB_DIR

logger = logging.getLogger(__name__)

class MemoryManager:
    def __init__(self):
        try:
            self.client = chromadb.PersistentClient(path=str(DB_DIR))
            # We use a default collection for all memories. 
            self.collection = self.client.get_or_create_collection(name="agent_memory")
            logger.info("ChromaDB initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            self.client = None

    def save_memory(self, memory_id: str, content: str, metadata: dict = None):
        """Save a new memory or update an existing one"""
        if not self.client:
            return "Memory DB not available."
        
        try:
            self.collection.upsert(
                documents=[content],
                metadatas=[metadata or {}],
                ids=[memory_id]
            )
            return f"Memory '{memory_id}' saved successfully."
        except Exception as e:
            logger.error(f"Error saving memory: {e}")
            return f"Error saving memory: {e}"

    def search_memory(self, query: str, n_results: int = 3):
        """Search for relevant memories"""
        if not self.client:
            return []
            
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            memories = []
            if results['documents'] and len(results['documents']) > 0:
                for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
                    memories.append({"content": doc, "metadata": meta})
            return memories
        except Exception as e:
            logger.error(f"Error searching memory: {e}")
            return []

    def delete_memory(self, memory_id: str):
        """Delete a memory by ID"""
        if not self.client:
            return "Memory DB not available."
            
        try:
            self.collection.delete(ids=[memory_id])
            return f"Memory '{memory_id}' deleted."
        except Exception as e:
            logger.error(f"Error deleting memory: {e}")
            return f"Error deleting memory: {e}"

memory_db = MemoryManager()
