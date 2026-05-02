import { useState, useCallback } from 'react';

export function useLocalStorage(key, initialValue) {
  const [storedValue, setStoredValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch {
      return initialValue;
    }
  });

  // Fix: always use React's functional updater so chained calls
  // get the LATEST state value, not a stale closure snapshot.
  const setValue = useCallback((value) => {
    setStoredValue((prev) => {
      const next = value instanceof Function ? value(prev) : value;
      try {
        window.localStorage.setItem(key, JSON.stringify(next));
      } catch (error) {
        console.error(error);
      }
      return next;
    });
  }, [key]);

  return [storedValue, setValue];
}
