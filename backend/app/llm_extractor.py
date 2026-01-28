"""
LLM Integration Module

Handles entity extraction using OpenAI's LLM.
"""
from typing import List, Optional
import os
from openai import OpenAI
import json


class EntityExtractor:
    """Extract entities from text using LLM."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """
        Initialize entity extractor.
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            model: OpenAI model to use
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None
    
    def extract_entities(self, text: str, entity_types: Optional[List[str]] = None) -> List[str]:
        """
        Extract entities from text using LLM.
        
        Args:
            text: Text to extract entities from
            entity_types: Optional list of entity types to extract
                         (e.g., ['PERSON', 'ORGANIZATION', 'DATE'])
        
        Returns:
            List of extracted entities
            
        Raises:
            ValueError: If OpenAI API key is not configured
        """
        if not self.client:
            raise ValueError(
                "OpenAI API key not configured. "
                "Set OPENAI_API_KEY environment variable or pass api_key parameter."
            )
        
        # Limit text length to prevent excessive API costs and token limit issues
        max_length = 4000  # Approximate token limit safety margin
        if len(text) > max_length:
            text = text[:max_length] + "..."
        
        # Build prompt
        entity_types_str = ", ".join(entity_types) if entity_types else "all relevant entities"
        
        prompt = f"""Extract {entity_types_str} from the following text.
Return the result as a JSON array of strings containing only the entity values.

Text:
{text}

Example output format:
["entity1", "entity2", "entity3"]

Return only the JSON array, no additional text."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts entities from text and returns them in JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            content = response.choices[0].message.content.strip()
            
            # Parse JSON response
            entities = json.loads(content)
            
            return entities if isinstance(entities, list) else []
            
        except json.JSONDecodeError as e:
            # Log the error and return empty list
            print(f"Warning: Failed to parse LLM response as JSON: {str(e)}")
            print(f"Response content: {content}")
            return []
        except Exception as e:
            raise Exception(f"Error extracting entities: {str(e)}")
    
    def extract_named_entities(self, text: str) -> dict:
        """
        Extract named entities with their types.
        
        Args:
            text: Text to extract entities from
        
        Returns:
            Dictionary mapping entity types to lists of entities
        """
        if not self.client:
            raise ValueError("OpenAI API key not configured")
        
        # Limit text length to prevent excessive API costs
        max_length = 4000
        if len(text) > max_length:
            text = text[:max_length] + "..."
        
        prompt = f"""Extract named entities from the following text and categorize them.
Return the result as a JSON object with entity types as keys and arrays of entity values.

Text:
{text}

Example output format:
{{
  "PERSON": ["John Doe", "Jane Smith"],
  "ORGANIZATION": ["Acme Corp"],
  "DATE": ["January 1, 2024"],
  "LOCATION": ["New York"]
}}

Return only the JSON object, no additional text."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts and categorizes named entities from text."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=800
            )
            
            content = response.choices[0].message.content.strip()
            entities = json.loads(content)
            
            return entities if isinstance(entities, dict) else {}
            
        except json.JSONDecodeError as e:
            print(f"Warning: Failed to parse LLM response as JSON: {str(e)}")
            print(f"Response content: {content}")
            return {}
        except Exception as e:
            raise Exception(f"Error extracting named entities: {str(e)}")
