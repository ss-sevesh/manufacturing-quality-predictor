import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import client from '../api/client';
import { loadHistory, saveHistory } from '../utils/helpers';

export function useHealth() {
  return useQuery({
    queryKey: ['health'],
    queryFn: () => client.get('/health').then((r) => r.data),
    refetchInterval: 5000,
    retry: 1,
  });
}

export function useModelInfo() {
  return useQuery({
    queryKey: ['modelInfo'],
    queryFn: () => client.get('/model/info').then((r) => r.data),
    retry: 1,
  });
}

export function usePredict() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payload) => client.post('/predict', payload).then((r) => r.data),
    onSuccess: (data, variables) => {
      const entry = {
        ...variables,
        quality_score: data.quality_score,
        confidence: data.confidence,
        status: data.status,
        timestamp: new Date().toISOString(),
      };
      const history = loadHistory();
      history.unshift(entry);
      saveHistory(history);
      queryClient.invalidateQueries({ queryKey: ['history'] });
    },
  });
}

export function useHistory() {
  return useQuery({
    queryKey: ['history'],
    queryFn: () => loadHistory(),
  });
}
