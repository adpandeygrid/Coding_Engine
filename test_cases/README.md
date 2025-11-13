# Test Cases for Rate Limiting and Concurrency Testing

## Purpose

These test cases are designed to test:
1. **Rate Limiting**: Multiple rapid requests (20 req/s limit)
2. **Concurrency**: Multiple simultaneous requests (10 concurrent limit)
3. **API Stability**: Handling multiple requests without errors

## Test Case Design

### Test Cases 1-10
- **Input**: Numbers from 1 to 25
- **Output**: "Hello" printed that many times
- **Purpose**: 
  - Test basic functionality
  - Test rate limiting (10 test cases = 10 requests)
  - Test concurrency (10 concurrent requests with 10 concurrent limit)

## How It Tests Rate Limits

When you run `python main.py`:

1. **10 test cases** = 10 API requests
2. **Default settings**: 10 concurrent, 20 req/s
3. **Expected behavior**:
   - All 10 requests should execute concurrently (up to 10 at once)
   - Requests should be rate-limited to ~20 per second
   - Total time should reflect concurrency (not sequential)

## Testing Different Limits

### Test with Higher Concurrency
```bash
MAX_CONCURRENT=20 REQUESTS_PER_SECOND=50 python main.py
```

### Test with Lower Limits (Stress Test)
```bash
MAX_CONCURRENT=5 REQUESTS_PER_SECOND=10 python main.py
```

### Test Rate Limiting (Many Requests)
```bash
# Create more test cases (input11.txt, input12.txt, etc.)
# Then run with lower limits to see rate limiting in action
MAX_CONCURRENT=3 REQUESTS_PER_SECOND=5 python main.py
```

## Expected Results

With 10 test cases and default settings (10 concurrent, 20 req/s):
- **All tests should pass** ✅
- **Execution time**: ~1-2 seconds (due to concurrency)
- **No rate limit errors** (429 status codes)
- **All outputs match expected outputs**

## Adding More Test Cases

To test more aggressive rate limiting:
1. Create more input/output pairs (input11.txt, output11.txt, etc.)
2. Run with lower limits to see rate limiting behavior
3. Monitor for 429 errors in the output

## Test Case Format

- **Input files**: `inputN.txt` - Contains the number to print "Hello" that many times
- **Output files**: `outputN.txt` - Contains expected output (N lines of "Hello")

