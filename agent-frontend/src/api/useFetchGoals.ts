import { useState, useEffect, useCallback } from 'react';
import { JSON_SERVER_URL } from './apiVariables';
import type { DataFetchResponse } from './DataContext';

export const useFetchGoals = (): DataFetchResponse<Record<string, any>[]> => {
  const [data, setData] = useState<Record<string, any>[]>([]); // Replace `any[]` with the appropriate type if available
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | undefined>();
  const [refetchIndex, setRefetchIndex] = useState<number>(0); // Tracks refetch requests

  const fetchGoals = useCallback(async () => {
    try {
      setIsLoading(true);
      const response = await fetch(`${JSON_SERVER_URL}/goals`);
      if (!response.ok) {
        setError(`Failed to fetch goals: ${response.statusText}`);
      }
      const data = await response.json();
      setData(data);
      setError(undefined); // Clear any previous errors
    } catch (err: any) {
      setError(err.message || 'An unknown error occurred');
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchGoals();
  }, [fetchGoals, refetchIndex]); // Refetch when refetchIndex changes

  const refetch = () => {
    setRefetchIndex((prev) => prev + 1); // Trigger a refetch by incrementing the index
  };

  return { data, isLoading, error, refetch };
};
