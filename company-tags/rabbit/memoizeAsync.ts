function memoizeAsync<T>(
    fn: (signal: AbortSignal) => Promise<T>
): (signal: AbortSignal) => Promise<T> {
    // Creating a cache to store the results
    const cache = new Map<AbortSignal, Promise<T>>();

    // Returning the memoized function
    return async (signal: AbortSignal) => {
        // If the result for this signal is already in the cache, return it
        if (cache.has(signal)) {
            return cache.get(signal)!;
        }

        // Otherwise, call the function and store the result in the cache
        const result = fn(signal);
        cache.set(signal, result);

        // Return the result
        return result;
    };
}

async function expensiveFunction(signal: AbortSignal): Promise<string> {
    const response = await fetch("https://example.com", { signal });
    return await response.text();
}

const memoizedFn = memoizeAsync(expensiveFunction);
const controller = new AbortController();
const signal = controller.signal;

await memoizedFn(signal); // Fetches then returns the response
await memoizedFn(signal); // Returns immediately as the result was cached

