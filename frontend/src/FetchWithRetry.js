    // Retry logic without timeout
    export const fetchWithRetry = async (url, options, retries = 3, delay = 1000) => {
        for (let i = 0; i < retries; i++) {
            try {
                const response = await fetch(url, options);
                if (!response.ok) {
                    throw new Error('Failed to fetch data');
                }
                return response;
            } catch (err) {
                if (i < retries - 1) {
                    console.log(`Retrying... (${i + 1})`);
                    await new Promise(res => setTimeout(res, delay)); // Wait before retrying
                } else {
                    throw err; // No more retries, throw the last error
                }
            }
        }
    };