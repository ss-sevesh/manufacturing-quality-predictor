import axios from 'axios';
import toast from 'react-hot-toast';

const client = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
});

client.interceptors.request.use(
  (config) => config,
  (error) => {
    toast.error('Request failed to send');
    return Promise.reject(error);
  }
);

client.interceptors.response.use(
  (response) => response,
  (error) => {
    const message =
      error.response?.data?.detail ||
      error.response?.statusText ||
      'Network error — is the API running?';
    toast.error(message);
    return Promise.reject(error);
  }
);

export default client;
