import asyncio
from pathlib import Path
import time
import os
import aiohttp

async def run_test_case(session, piston_url, language, source_code, test_input, max_retries=3, retry_delay=1):
    """
    Runs a single test case with the provided source code and input.
    Uses self-hosted Piston API to avoid rate limits.
    
    Args:
        session: aiohttp ClientSession instance
        piston_url: Base URL of the self-hosted Piston API
        language: Programming language (e.g., "cpp", "python", "java", "rust")
        source_code: String containing the user's source code
        test_input: String containing the test case input (stdin)
        max_retries: Maximum number of retry attempts (kept for compatibility)
        retry_delay: Initial delay in seconds for retries (exponentially increases)
    
    Returns:
        Dictionary with stdout, stderr, and execution status
    """
    for attempt in range(max_retries + 1):
        try:
            # Prepare the request payload for Piston API
            payload = {
                "language": language,
                "version": "*",  # Use latest version
                "files": [{
                    "name": get_filename_for_language(language),
                    "content": source_code
                }],
                "stdin": test_input
            }
            
            # Make POST request to Piston API
            # Public API uses /api/v2/piston/execute, self-hosted uses /api/v2/execute
            if piston_url.startswith('https://emkc.org'):
                api_url = f"{piston_url}/execute"
            else:
                api_url = f"{piston_url}/api/v2/execute"
            async with session.post(api_url, json=payload) as response:
                if response.status == 429:
                    # Rate limit (unlikely with self-hosted, but handle it)
                    if attempt < max_retries:
                        wait_time = retry_delay * (2 ** attempt)
                        print(f"Rate limit detected, waiting {wait_time} seconds before retry {attempt + 1}/{max_retries}...")
                        await asyncio.sleep(wait_time)
                        continue
                    else:
                        return {
                            'stdout': '',
                            'stderr': '',
                            'compile_error': None,
                            'runtime_error': 'Rate limit exceeded',
                            'success': False
                        }
                
                response.raise_for_status()
                result_data = await response.json()
            
            # Process the output from Piston API
            result = {
                'stdout': '',
                'stderr': '',
                'compile_error': None,
                'runtime_error': None,
                'success': False
            }
            
            # Piston API returns a dictionary with 'run' key
            if 'run' in result_data:
                run_data = result_data['run']
                result['stdout'] = run_data.get('stdout', '')
                result['stderr'] = run_data.get('stderr', '')
                
                # Check for exit code (0 means success)
                exit_code = run_data.get('code', -1)
                result['success'] = exit_code == 0
                
                # If exit code is non-zero, treat as runtime error
                if exit_code != 0 and not result['stderr']:
                    result['runtime_error'] = f"Process exited with code {exit_code}"
                    result['success'] = False
            
            # Check for compilation errors
            if 'compile' in result_data:
                compile_data = result_data['compile']
                if compile_data.get('stderr'):
                    result['compile_error'] = compile_data['stderr']
                    result['success'] = False
                elif compile_data.get('code', 0) != 0:
                    result['compile_error'] = compile_data.get('stdout', '') or 'Compilation failed'
                    result['success'] = False
            
            # If no run data, something went wrong
            if 'run' not in result_data:
                result['runtime_error'] = 'No execution output received'
                result['success'] = False
            
            return result
            
        except aiohttp.ClientError as e:
            error_str = str(e).lower()
            # Check if it's a rate limit error (unlikely with self-hosted, but keep for safety)
            is_rate_limit = (
                'rate limit' in error_str or 
                'ratelimit' in error_str or
                '429' in error_str or 
                'too many requests' in error_str
            )
            if is_rate_limit and attempt < max_retries:
                wait_time = retry_delay * (2 ** attempt)  # Exponential backoff
                print(f"Rate limit exception, waiting {wait_time} seconds before retry {attempt + 1}/{max_retries}...")
                await asyncio.sleep(wait_time)
                continue
            else:
                # Not a rate limit error or max retries reached, return error
                return {
                    'stdout': '',
                    'stderr': '',
                    'compile_error': None,
                    'runtime_error': f"HTTP error: {str(e)}",
                    'success': False
                }
        except Exception as e:
            # Other exceptions
            return {
                'stdout': '',
                'stderr': '',
                'compile_error': None,
                'runtime_error': str(e),
                'success': False
            }
    
    # If we got here without output, something went wrong
    return {
        'stdout': '',
        'stderr': '',
        'compile_error': None,
        'runtime_error': 'Failed to execute after retries',
        'success': False
    }

def get_filename_for_language(language):
    """
    Returns the appropriate filename for a given programming language.
    """
    filename_map = {
        'python': 'main.py',
        'python3': 'main.py',
        'cpp': 'main.cpp',
        'c++': 'main.cpp',
        'c': 'main.c',
        'java': 'Main.java',
        'rust': 'main.rs',
        'javascript': 'main.js',
        'js': 'main.js',
        'go': 'main.go',
        'ruby': 'main.rb',
        'php': 'main.php',
        'swift': 'main.swift',
        'kotlin': 'Main.kt',
        'scala': 'main.scala',
        'r': 'main.R',
        'bash': 'main.sh',
        'sh': 'main.sh',
    }
    return filename_map.get(language.lower(), 'main.txt')

def normalize_output(output):
    """
    Normalizes output by stripping trailing whitespace and newlines for comparison.
    """
    if output is None:
        return ""
    return output.rstrip()

def compare_outputs(actual, expected):
    """
    Compares actual output with expected output.
    
    Returns:
        Tuple (bool, str): (match, message)
    """
    actual_normalized = normalize_output(actual)
    expected_normalized = normalize_output(expected)
    
    if actual_normalized == expected_normalized:
        return True, "Output matches expected result"
    else:
        return False, f"Output mismatch\nExpected:\n{expected_normalized}\n\nGot:\n{actual_normalized}"

def get_test_case_files(test_cases_dir="test_cases"):
    """
    Finds all input files in the test_cases directory and returns pairs of (input_file, output_file).
    
    Args:
        test_cases_dir: Directory containing test case files
    
    Returns:
        List of tuples: [(input_file_path, expected_output_file_path), ...]
    """
    test_cases_dir = Path(test_cases_dir)
    if not test_cases_dir.exists():
        return []
    
    # Find all input files (input1.txt, input2.txt, etc.)
    input_files = sorted(test_cases_dir.glob("input*.txt"))
    test_pairs = []
    
    for input_file in input_files:
        # Extract test number from filename (e.g., "input1.txt" -> "1")
        test_num = input_file.stem.replace("input", "")
        output_file = test_cases_dir / f"output{test_num}.txt"
        
        if output_file.exists():
            test_pairs.append((input_file, output_file))
        else:
            print(f"Warning: {output_file} not found for {input_file}")
    
    return test_pairs

async def process_single_test_case(session, piston_url, language, source_code, input_file, expected_output_file, test_index, semaphore, last_request_time, min_delay=0.25):
    """
    Processes a single test case: reads files, runs code, compares outputs.
    Uses self-hosted Piston API with minimal rate limiting.
    
    Args:
        session: aiohttp ClientSession instance
        piston_url: Base URL of the self-hosted Piston API
        language: Programming language
        source_code: String containing the user's source code
        input_file: Path to input file
        expected_output_file: Path to expected output file
        test_index: Index of the test case (for ordering results)
        semaphore: asyncio.Semaphore to limit concurrent requests
        last_request_time: List with last request timestamp [timestamp] for synchronization
        min_delay: Minimum delay in seconds between requests (default: 0.1s for 10 req/s)
    
    Returns:
        Dictionary with test results including comparison and execution time
    """
    # Start timing
    start_time = time.time()
    
    # Read input file (outside semaphore - file I/O is fast)
    with open(input_file, 'r') as f:
        test_input = f.read()
    
    # Read expected output file (outside semaphore - file I/O is fast)
    with open(expected_output_file, 'r') as f:
        expected_output = f.read()
    
    # Track API call time separately
    api_start_time = time.time()
    
    # Acquire semaphore before making API call (light rate limiting for self-hosted)
    async with semaphore:
        # Ensure minimum delay between requests (much less restrictive for self-hosted)
        current_time = asyncio.get_event_loop().time()
        if last_request_time[0] is not None:
            time_since_last = current_time - last_request_time[0]
            if time_since_last < min_delay:
                wait_time = min_delay - time_since_last
                await asyncio.sleep(wait_time)
        
        # Run the test case using self-hosted Piston API
        result = await run_test_case(session, piston_url, language, source_code, test_input)
        
        # Update last request time
        last_request_time[0] = asyncio.get_event_loop().time()
    
    # Calculate API execution time
    api_end_time = time.time()
    api_execution_time = api_end_time - api_start_time
    
    # Compare outputs
    output_match, comparison_msg = compare_outputs(result['stdout'], expected_output)
    
    # Calculate total execution time
    end_time = time.time()
    total_execution_time = end_time - start_time
    
    # Add comparison results and timing
    result['expected_output'] = expected_output
    result['output_match'] = output_match
    result['comparison_msg'] = comparison_msg
    result['test_name'] = input_file.stem
    result['input_file'] = input_file
    result['expected_output_file'] = expected_output_file
    result['test_index'] = test_index
    result['test_input'] = test_input
    result['execution_time'] = total_execution_time
    result['api_execution_time'] = api_execution_time
    
    # Overall status (success if no errors AND output matches)
    result['overall_success'] = result['success'] and output_match and not result['compile_error']
    
    return result

async def run_test_cases_from_files(language, source_code, test_cases_dir="test_cases", max_concurrent=10, requests_per_second=20):
    """
    Runs multiple test cases from files. With self-hosted Piston API, 
    you can use higher concurrency without rate limit concerns.
    
    Args:
        language: Programming language
        source_code: String containing the user's source code
        test_cases_dir: Directory containing input*.txt and output*.txt files
        max_concurrent: Maximum number of concurrent requests (default: 10 for self-hosted)
        requests_per_second: Maximum requests per second (default: 20, can be higher with self-hosted)
    
    Returns:
        List of result dictionaries with comparison results (sorted by test index)
    """
    test_pairs = get_test_case_files(test_cases_dir)
    
    if not test_pairs:
        print(f"No test case files found in {test_cases_dir}/")
        print("Expected files: input1.txt, output1.txt, input2.txt, output2.txt, etc.")
        return []
    
    # Get Piston API URL from environment or use default
    # Use public API as fallback if local API doesn't have runtimes installed
    piston_url = os.getenv('PISTON_API_URL', 'http://localhost:2000')
    using_public_api = False
    
    # Check if local API has runtimes, if not, use public API
    try:
        import aiohttp
        async with aiohttp.ClientSession() as check_session:
            async with check_session.get(f"{piston_url}/api/v2/runtimes", timeout=aiohttp.ClientTimeout(total=2)) as resp:
                if resp.status == 200:
                    runtimes = await resp.json()
                    if not runtimes or len(runtimes) == 0:
                        print("⚠️  Warning: Local Piston API has no runtimes installed.")
                        print("   Using public Piston API (https://emkc.org/api/v2/piston) instead.")
                        print("   Note: Public API has strict rate limits (~5 req/s). Adjusting settings...")
                        piston_url = 'https://emkc.org/api/v2/piston'
                        using_public_api = True
                        # Adjust rate limits for public API (much stricter)
                        max_concurrent = 1  # Sequential requests only
                        requests_per_second = 4  # Conservative: 4 req/s (below public API limit of ~5 req/s)
                        min_delay = 1.0 / requests_per_second  # Recalculate delay
                        print(f"   Using conservative settings: {max_concurrent} concurrent, ~{requests_per_second} req/s")
    except Exception:
        # If local API is not accessible, use public API
        print("⚠️  Warning: Cannot connect to local Piston API.")
        print("   Using public Piston API (https://emkc.org/api/v2/piston) instead.")
        print("   Note: Public API has strict rate limits (~5 req/s). Adjusting settings...")
        piston_url = 'https://emkc.org/api/v2/piston'
        using_public_api = True
        # Adjust rate limits for public API (much stricter)
        max_concurrent = 1  # Sequential requests only
        requests_per_second = 4  # Conservative: 4 req/s
        min_delay = 1.0 / requests_per_second  # Recalculate delay
        print(f"   Using conservative settings: {max_concurrent} concurrent, ~{requests_per_second} req/s")
    
    if not using_public_api:
        print(f"Running {len(test_pairs)} test case(s) with self-hosted Piston API (max {max_concurrent} concurrent, ~{requests_per_second} req/s)...\n")
    else:
        print(f"Running {len(test_pairs)} test case(s) with public Piston API (max {max_concurrent} concurrent, ~{requests_per_second} req/s)...\n")
    
    # Start total execution time
    total_start_time = time.time()
    
    # Create a semaphore to limit concurrent requests
    semaphore = asyncio.Semaphore(max_concurrent)
    
    # Calculate minimum delay between requests (only if not already calculated for public API)
    if not using_public_api:
        min_delay = 1.0 / requests_per_second  # e.g., 1/4 = 0.25 seconds
    
    # Shared variable to track last request time
    last_request_time = [None]
    
    # Create aiohttp session for making HTTP requests
    async with aiohttp.ClientSession() as session:
        # Create tasks for all test cases
        tasks = [
            process_single_test_case(session, piston_url, language, source_code, input_file, expected_output_file, i, semaphore, last_request_time, min_delay)
            for i, (input_file, expected_output_file) in enumerate(test_pairs, 1)
        ]
        
        # Execute all test cases
        results = await asyncio.gather(*tasks)
    
    # Calculate total execution time
    total_end_time = time.time()
    total_execution_time = total_end_time - total_start_time
    
    # Sort results by test index to maintain order
    results.sort(key=lambda x: x['test_index'])
    
    # Display results in order
    for result in results:
        i = result['test_index']
        input_file = result['input_file']
        expected_output_file = result['expected_output_file']
        
        print(f"\n{'='*60}")
        print(f"TEST CASE {i}: {input_file.name} vs {expected_output_file.name}")
        print(f"{'='*60}")
        print(f"Input:\n{result['test_input']}")
        print(f"\n{'-'*60}")
        
        # Print results
        print("STDOUT:")
        print(result['stdout'] if result['stdout'] else "(empty)")
        
        print("\nEXPECTED OUTPUT:")
        print(result['expected_output'] if result['expected_output'] else "(empty)")
        
        print(f"\nCOMPARISON: {'✓ PASS' if result['output_match'] else '✗ FAIL'}")
        if not result['output_match']:
            print(result['comparison_msg'])
        
        if result['stderr']:
            print("\nSTDERR:")
            print(result['stderr'])
        
        if result['compile_error']:
            print("\nCOMPILATION ERROR:")
            print(result['compile_error'])
        
        if result['runtime_error']:
            print("\nRUNTIME ERROR:")
            print(result['runtime_error'])
        
        # Display execution times
        exec_time = result.get('execution_time', 0)
        api_time = result.get('api_execution_time', 0)
        print(f"\nExecution Time: {exec_time:.3f}s (API: {api_time:.3f}s)")
        
        print(f"\nStatus: {'SUCCESS' if result['overall_success'] else 'FAILED'}")
        print(f"{'='*60}")
    
    # Add total execution time to results metadata
    return results, total_execution_time

async def main():
    # Example: User's source code (solution to a problem)
    # This code reads a number from stdin and prints "Hello" that many times
    user_source_code = """
#include <iostream>

int main() {
    int num;
    std::cin >> num;
    
    for (int i = 0; i < num; i++) {
        std::cout << "Hello" << std::endl;
    }
    
    return 0;
}
"""
    
    # Language of the source code
    language = "cpp"
    
    # Test cases directory
    test_cases_dir = "test_cases"
    
    # Run all test cases from files
    # Rate limits can be customized via environment variables or function parameters
    # Default: 10 concurrent, 20 req/s (respects NGINX limit of 200 req/s)
    max_concurrent = int(os.getenv('MAX_CONCURRENT', '10'))
    requests_per_second = int(os.getenv('REQUESTS_PER_SECOND', '20'))
    results, total_execution_time = await run_test_cases_from_files(
        language, 
        user_source_code, 
        test_cases_dir,
        max_concurrent=max_concurrent,
        requests_per_second=requests_per_second
    )
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    if results:
        total = len(results)
        passed = sum(1 for r in results if r.get('overall_success', False))
        print(f"Total test cases: {total}")
        print(f"Passed: {passed}/{total}")
        print(f"Failed: {total - passed}/{total}")
        
        # Calculate timing statistics
        total_api_time = sum(r.get('api_execution_time', 0) for r in results)
        avg_exec_time = sum(r.get('execution_time', 0) for r in results) / total if total > 0 else 0
        avg_api_time = total_api_time / total if total > 0 else 0
        
        print(f"\nTiming Statistics:")
        print(f"  Total execution time: {total_execution_time:.3f}s")
        print(f"  Average per test case: {avg_exec_time:.3f}s")
        print(f"  Total API time: {total_api_time:.3f}s")
        print(f"  Average API time per test: {avg_api_time:.3f}s")
        
        # Show individual test case times
        print(f"\nIndividual Test Case Times:")
        for r in results:
            test_name = r.get('test_name', 'Unknown')
            exec_time = r.get('execution_time', 0)
            api_time = r.get('api_execution_time', 0)
            status = "✓" if r.get('overall_success', False) else "✗"
            print(f"  {status} {test_name}: {exec_time:.3f}s (API: {api_time:.3f}s)")
        
        # List failed test cases
        failed = [r for r in results if not r.get('overall_success', False)]
        if failed:
            print("\nFailed test cases:")
            for r in failed:
                test_name = r.get('test_name', 'Unknown')
                if r.get('compile_error'):
                    reason = "Compilation error"
                elif r.get('runtime_error'):
                    reason = "Runtime error"
                elif not r.get('output_match', False):
                    reason = "Output mismatch"
                else:
                    reason = "Execution failed"
                print(f"  - {test_name}: {reason}")
    else:
        print("No test cases found.")
    print(f"{'='*60}")

if __name__ == "__main__":
    asyncio.run(main())