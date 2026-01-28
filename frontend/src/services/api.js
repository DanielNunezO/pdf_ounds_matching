/**
 * API Service
 * 
 * Handles all API calls to the backend
 */
import axios from 'axios';

// Use environment variable for API URL, fallback to localhost
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

class APIService {
  /**
   * Upload PDF file
   */
  async uploadPDF(file) {
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await axios.post(`${API_BASE_URL}/upload-pdf`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      return response.data;
    } catch (error) {
      console.error('Error uploading PDF:', error);
      throw new Error(error.response?.data?.detail || 'Failed to upload PDF');
    }
  }

  /**
   * Extract text from uploaded PDF
   */
  async extractText(fileId) {
    try {
      const response = await axios.get(`${API_BASE_URL}/extract-text/${fileId}`);
      return response.data;
    } catch (error) {
      console.error('Error extracting text:', error);
      throw new Error(error.response?.data?.detail || 'Failed to extract text');
    }
  }

  /**
   * Extract entities using LLM
   */
  async extractEntities(text, entityTypes = null) {
    try {
      const response = await axios.post(`${API_BASE_URL}/extract-entities`, {
        text,
        entity_types: entityTypes,
      });
      return response.data;
    } catch (error) {
      console.error('Error extracting entities:', error);
      throw new Error(error.response?.data?.detail || 'Failed to extract entities');
    }
  }

  /**
   * Extract named entities with categories
   */
  async extractNamedEntities(text) {
    try {
      const response = await axios.post(`${API_BASE_URL}/extract-named-entities`, {
        text,
      });
      return response.data;
    } catch (error) {
      console.error('Error extracting named entities:', error);
      throw new Error(error.response?.data?.detail || 'Failed to extract named entities');
    }
  }

  /**
   * Match entity in PDF
   */
  async matchEntity(fileId, entity, strategy = 'exact', options = {}) {
    try {
      const response = await axios.post(`${API_BASE_URL}/match/${fileId}`, {
        entity,
        strategy,
        threshold: options.threshold || 80.0,
        context_window: options.context_window || 3,
      });
      return response.data;
    } catch (error) {
      console.error('Error matching entity:', error);
      throw new Error(error.response?.data?.detail || 'Failed to match entity');
    }
  }

  /**
   * Get available strategies
   */
  async getStrategies() {
    try {
      const response = await axios.get(`${API_BASE_URL}/strategies`);
      return response.data;
    } catch (error) {
      console.error('Error getting strategies:', error);
      throw new Error(error.response?.data?.detail || 'Failed to get strategies');
    }
  }

  /**
   * Clean up uploaded PDF
   */
  async cleanupPDF(fileId) {
    try {
      const response = await axios.delete(`${API_BASE_URL}/cleanup/${fileId}`);
      return response.data;
    } catch (error) {
      console.error('Error cleaning up PDF:', error);
      // Don't throw error for cleanup failures
      return null;
    }
  }
}

export default new APIService();
