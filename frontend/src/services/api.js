/**
 * API Service
 * 
 * Handles all API calls to the backend
 */
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

class APIService {
  /**
   * Upload PDF file
   */
  async uploadPDF(file) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post(`${API_BASE_URL}/upload-pdf`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  }

  /**
   * Extract text from uploaded PDF
   */
  async extractText(fileId) {
    const response = await axios.get(`${API_BASE_URL}/extract-text/${fileId}`);
    return response.data;
  }

  /**
   * Extract entities using LLM
   */
  async extractEntities(text, entityTypes = null) {
    const response = await axios.post(`${API_BASE_URL}/extract-entities`, {
      text,
      entity_types: entityTypes,
    });
    return response.data;
  }

  /**
   * Extract named entities with categories
   */
  async extractNamedEntities(text) {
    const response = await axios.post(`${API_BASE_URL}/extract-named-entities`, {
      text,
    });
    return response.data;
  }

  /**
   * Match entity in PDF
   */
  async matchEntity(fileId, entity, strategy = 'exact', options = {}) {
    const response = await axios.post(`${API_BASE_URL}/match/${fileId}`, {
      entity,
      strategy,
      threshold: options.threshold || 80.0,
      context_window: options.context_window || 3,
    });
    return response.data;
  }

  /**
   * Get available strategies
   */
  async getStrategies() {
    const response = await axios.get(`${API_BASE_URL}/strategies`);
    return response.data;
  }

  /**
   * Clean up uploaded PDF
   */
  async cleanupPDF(fileId) {
    const response = await axios.delete(`${API_BASE_URL}/cleanup/${fileId}`);
    return response.data;
  }
}

export default new APIService();
