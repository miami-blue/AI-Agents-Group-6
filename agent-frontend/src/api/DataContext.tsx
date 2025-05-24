import { createContext, useContext, type ReactNode } from 'react';
import { useFetchGoals } from './useFetchGoals';

export interface DataFetchResponse<T> {
  data: T;
  error?: string;
  isLoading: boolean;
  refetch: () => void;
}

interface DataContextType {
  goalsResponse: DataFetchResponse<Record<string, any>[]>;
}

// Create the context
const DataContext = createContext<DataContextType | undefined>(undefined);

// Create the provider component
export const DataProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const goalsResponse = useFetchGoals();

  return (
    <DataContext.Provider value={{ goalsResponse }}>
      {children}
    </DataContext.Provider>
  );
};

// Custom hook to use the DataContext
export const useDataContext = (): DataContextType => {
  const context = useContext(DataContext);
  if (!context) {
    throw new Error('useDataContext must be used within a DataProvider');
  }
  return context;
};
