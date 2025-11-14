// Problems database
const problems = [
    {
        id: 1,
        title: "Print Hello N Times",
        difficulty: "easy",
        description: `
            <h3>Problem</h3>
            <p>Write a program that reads a number <code>n</code> from stdin and prints "Hello" <code>n</code> times, each on a new line.</p>
            
            <h3>Example</h3>
            <p><strong>Input:</strong></p>
            <pre>5</pre>
            
            <p><strong>Output:</strong></p>
            <pre>Hello
Hello
Hello
Hello
Hello</pre>
            
            <h3>Constraints</h3>
            <ul>
                <li>1 ≤ n ≤ 100</li>
            </ul>
        `,
        testCaseFiles: [
            { input: "input1.txt", output: "output1.txt" },
            { input: "input2.txt", output: "output2.txt" },
            { input: "input3.txt", output: "output3.txt" },
            { input: "input4.txt", output: "output4.txt" },
            { input: "input5.txt", output: "output5.txt" },
            { input: "input6.txt", output: "output6.txt" },
            { input: "input7.txt", output: "output7.txt" },
            { input: "input8.txt", output: "output8.txt" },
            { input: "input9.txt", output: "output9.txt" },
            { input: "input10.txt", output: "output10.txt" },
            { input: "input11.txt", output: "output11.txt" }
        ],
        starterCode: {
            cpp: `#include <iostream>

int main() {
    int n;
    std::cin >> n;
    
    for (int i = 0; i < n; i++) {
        std::cout << "Hello" << std::endl;
    }
    
    return 0;
}`,
            python: `n = int(input())

for i in range(n):
    print("Hello")`,
            javascript: `const readline = require('readline');
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

rl.on('line', (n) => {
    const num = parseInt(n);
    for (let i = 0; i < num; i++) {
        console.log("Hello");
    }
    rl.close();
});`,
            java: `import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        
        for (int i = 0; i < n; i++) {
            System.out.println("Hello");
        }
    }
}`
        }
    },
    {
        id: 2,
        title: "Sum of Two Numbers",
        difficulty: "easy",
        description: `
            <h3>Problem</h3>
            <p>Write a program that reads two integers <code>a</code> and <code>b</code> from stdin and prints their sum.</p>
            
            <h3>Example</h3>
            <p><strong>Input:</strong></p>
            <pre>5 10</pre>
            
            <p><strong>Output:</strong></p>
            <pre>15</pre>
            
            <h3>Constraints</h3>
            <ul>
                <li>-1000 ≤ a, b ≤ 1000</li>
            </ul>
        `,
        testCaseFiles: [
            { input: "5 10", output: "15" },
            { input: "-5 10", output: "5" },
            { input: "100 200", output: "300" },
            { input: "0 0", output: "0" }
        ],
        starterCode: {
            cpp: `#include <iostream>

int main() {
    int a, b;
    std::cin >> a >> b;
    
    std::cout << a + b << std::endl;
    
    return 0;
}`,
            python: `a, b = map(int, input().split())
print(a + b)`,
            javascript: `const readline = require('readline');
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

rl.on('line', (line) => {
    const [a, b] = line.split(' ').map(Number);
    console.log(a + b);
    rl.close();
});`,
            java: `import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int a = scanner.nextInt();
        int b = scanner.nextInt();
        
        System.out.println(a + b);
    }
}`
        }
    },
    {
        id: 3,
        title: "Find Maximum",
        difficulty: "medium",
        description: `
            <h3>Problem</h3>
            <p>Write a program that reads <code>n</code> integers from stdin and prints the maximum value.</p>
            
            <h3>Example</h3>
            <p><strong>Input:</strong></p>
            <pre>5
1 5 3 9 2</pre>
            
            <p><strong>Output:</strong></p>
            <pre>9</pre>
            
            <h3>Constraints</h3>
            <ul>
                <li>1 ≤ n ≤ 1000</li>
                <li>-1000 ≤ each number ≤ 1000</li>
            </ul>
        `,
        testCaseFiles: [
            { input: "5\n1 5 3 9 2", output: "9" },
            { input: "3\n-1 -5 -3", output: "-1" },
            { input: "1\n42", output: "42" }
        ],
        starterCode: {
            cpp: `#include <iostream>
#include <algorithm>
#include <vector>

int main() {
    int n;
    std::cin >> n;
    
    std::vector<int> numbers(n);
    for (int i = 0; i < n; i++) {
        std::cin >> numbers[i];
    }
    
    int maxVal = *std::max_element(numbers.begin(), numbers.end());
    std::cout << maxVal << std::endl;
    
    return 0;
}`,
            python: `n = int(input())
numbers = list(map(int, input().split()))
print(max(numbers))`,
            javascript: `const readline = require('readline');
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

let n;
rl.on('line', (line) => {
    if (!n) {
        n = parseInt(line);
    } else {
        const numbers = line.split(' ').map(Number);
        console.log(Math.max(...numbers));
        rl.close();
    }
});`,
            java: `import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        
        int max = Integer.MIN_VALUE;
        for (int i = 0; i < n; i++) {
            int num = scanner.nextInt();
            if (num > max) {
                max = num;
            }
        }
        
        System.out.println(max);
    }
}`
        }
    }
];

// Application state
let currentProblem = null;
let currentLanguage = 'cpp';
let apiUrl = 'http://localhost:2000';
let testCases = [];

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    initializeProblems();
    setupEventListeners();
    loadProblem(problems[0]);
});

function initializeProblems() {
    const problemList = document.getElementById('problemList');
    problems.forEach(problem => {
        const li = document.createElement('li');
        li.textContent = `${problem.id}. ${problem.title}`;
        li.dataset.problemId = problem.id;
        li.addEventListener('click', () => loadProblem(problem));
        problemList.appendChild(li);
    });
}

function setupEventListeners() {
    document.getElementById('runBtn').addEventListener('click', runCode);
    document.getElementById('submitBtn').addEventListener('click', submitCode);
    document.getElementById('languageSelect').addEventListener('change', (e) => {
        currentLanguage = e.target.value;
        updateEditorLanguage();
    });
    document.getElementById('apiUrl').addEventListener('change', (e) => {
        if (e.target.value === '') {
            document.getElementById('customApiUrl').style.display = 'block';
        } else {
            document.getElementById('customApiUrl').style.display = 'none';
            apiUrl = e.target.value;
            console.log('API URL set to:', apiUrl); // Debug log
            // Reload test cases if a problem is loaded (they may need to switch from local to GitHub or vice versa)
            if (currentProblem) {
                loadTestCases(currentProblem);
            }
        }
    });
    document.getElementById('customApiUrl').addEventListener('input', (e) => {
        let url = e.target.value.trim();
        // If URL doesn't start with http:// or https://, add https://
        if (url && !/^https?:\/\//.test(url)) {
            url = 'https://' + url;
            e.target.value = url; // Update the input field
        }
        const oldApiUrl = apiUrl;
        apiUrl = url || 'http://localhost:2000';
        console.log('API URL set to:', apiUrl); // Debug log
        // Reload test cases if API URL changed and a problem is loaded
        if (currentProblem && oldApiUrl !== apiUrl) {
            loadTestCases(currentProblem);
        }
    });
    document.getElementById('clearResults').addEventListener('click', () => {
        document.getElementById('resultsContent').innerHTML = '<p class="placeholder">Run or submit your code to see results here.</p>';
    });
}

async function loadProblem(problem) {
    currentProblem = problem;
    
    // Update active problem in list
    document.querySelectorAll('#problemList li').forEach(li => {
        li.classList.remove('active');
        if (parseInt(li.dataset.problemId) === problem.id) {
            li.classList.add('active');
        }
    });
    
    // Update problem display
    document.getElementById('problemTitle').textContent = problem.title;
    document.getElementById('problemDifficulty').textContent = problem.difficulty.charAt(0).toUpperCase() + problem.difficulty.slice(1);
    document.getElementById('problemDifficulty').className = `difficulty ${problem.difficulty}`;
    document.getElementById('problemDescription').innerHTML = problem.description;
    
    // Load test cases
    await loadTestCases(problem);
    
    // Update editor with starter code
    updateEditorLanguage();
}

async function loadTestCases(problem) {
    testCases = [];
    const testCasesPreview = document.getElementById('testCasesPreview');
    testCasesPreview.innerHTML = '<p>Loading test cases...</p>';
    
    if (problem.id === 1) {
        // Load from files for problem 1
        try {
            // Determine test case base URL
            // If using Railway/custom API, load from GitHub; otherwise use local paths
            const isLocalhost = apiUrl.includes('localhost') || apiUrl.includes('127.0.0.1');
            const testCaseBaseUrl = isLocalhost 
                ? '/test_cases'  // Local server
                : 'https://raw.githubusercontent.com/adpandeygrid/Coding_Engine/main/test_cases';  // GitHub raw URLs
            
            for (let i = 1; i <= 11; i++) {
                try {
                    const inputUrl = `${testCaseBaseUrl}/input${i}.txt`;
                    const outputUrl = `${testCaseBaseUrl}/output${i}.txt`;
                    
                    const inputResponse = await fetch(inputUrl);
                    const outputResponse = await fetch(outputUrl);
                    
                    if (inputResponse.ok && outputResponse.ok) {
                        let input = await inputResponse.text();
                        let output = await outputResponse.text();
                        // Trim input to remove trailing newlines (but keep the actual input value)
                        input = input.trim();
                        // Store output as-is (with trailing newlines), normalization happens during comparison
                        // Debug: log what we're storing
                        console.log(`Loaded test case ${i} from ${isLocalhost ? 'local' : 'GitHub'}:`, {
                            input: input,
                            outputLength: output.length,
                            outputEndsWithNewline: output.endsWith('\n'),
                            outputPreview: output.substring(0, 20) + '...'
                        });
                        testCases.push({ input: input, output: output });
                    }
                } catch (e) {
                    console.warn(`Could not load test case ${i}:`, e);
                }
            }
        } catch (e) {
            console.warn('Could not load test cases from files, using defaults');
            // Fallback to default test cases
            testCases = problem.testCaseFiles.map(tc => ({
                input: typeof tc.input === 'string' ? tc.input : '',
                output: typeof tc.output === 'string' ? tc.output : ''
            }));
        }
    } else {
        // Use inline test cases for other problems
        testCases = problem.testCaseFiles.map(tc => ({
            input: tc.input,
            output: tc.output
        }));
    }
    
    // Update preview
    testCasesPreview.innerHTML = '';
    testCases.forEach((testCase, index) => {
        const div = document.createElement('div');
        div.className = 'test-case-item';
        div.innerHTML = `
            <h4>Test Case ${index + 1}</h4>
            <p><strong>Input:</strong></p>
            <pre>${testCase.input}</pre>
            <p><strong>Expected Output:</strong></p>
            <pre>${testCase.output}</pre>
        `;
        testCasesPreview.appendChild(div);
    });
}

function updateEditorLanguage() {
    if (currentProblem && currentProblem.starterCode[currentLanguage]) {
        document.getElementById('codeEditor').value = currentProblem.starterCode[currentLanguage];
    }
}

async function runCode() {
    const code = document.getElementById('codeEditor').value;
    if (!code.trim()) {
        showError('Please write some code first!');
        return;
    }
    
    if (!currentProblem || testCases.length === 0) {
        showError('Please wait for test cases to load!');
        return;
    }
    
    const resultsContent = document.getElementById('resultsContent');
    resultsContent.innerHTML = '<div class="loading"></div> <span>Running code...</span>';
    
    try {
        // Run with first test case
        const testCase = testCases[0];
        const result = await executeCode(code, testCase.input);
        
        const normalizedActual = normalizeOutput(result.stdout);
        const normalizedExpected = normalizeOutput(testCase.output);
        const outputMatch = normalizedActual === normalizedExpected;
        
        // Debug logging
        console.log('Output comparison:', {
            rawActual: result.stdout,
            rawExpected: testCase.output,
            normalizedActual: normalizedActual,
            normalizedExpected: normalizedExpected,
            match: outputMatch,
            actualLength: normalizedActual.length,
            expectedLength: normalizedExpected.length
        });
        
        // Debug: log the success check
        console.log('Result success check:', {
            resultSuccess: result.success,
            outputMatch: outputMatch,
            exitCode: result.exitCode,
            combined: outputMatch && result.success
        });
        
        const testPassed = outputMatch && result.success;
        
        resultsContent.innerHTML = `
            <h4>Test Case 1 Result</h4>
            <div class="test-result ${testPassed ? 'passed' : 'failed'}">
                <div class="test-result-header">
                    <span class="test-result-title">Test Case 1</span>
                    <span class="test-result-status ${testPassed ? 'passed' : 'failed'}">
                        ${testPassed ? 'PASSED' : 'FAILED'}
                    </span>
                </div>
                <div class="test-result-details">
                    <p><strong>Input:</strong></p>
                    <pre>${testCase.input}</pre>
                    <p><strong>Your Output:</strong></p>
                    <pre>${result.stdout || '(empty)'}</pre>
                    <p><strong>Expected Output:</strong></p>
                    <pre>${testCase.output}</pre>
                    ${result.stderr ? `<p><strong>Error:</strong></p><pre>${result.stderr}</pre>` : ''}
                    ${!outputMatch ? `<p style="color: #ff6b6b;"><strong>Output mismatch!</strong></p>` : ''}
                </div>
            </div>
        `;
    } catch (error) {
        showError(`Execution failed: ${error.message}`);
    }
}

async function submitCode() {
    const code = document.getElementById('codeEditor').value;
    if (!code.trim()) {
        showError('Please write some code first!');
        return;
    }
    
    if (!currentProblem || testCases.length === 0) {
        showError('Please wait for test cases to load!');
        return;
    }
    
    const resultsContent = document.getElementById('resultsContent');
    resultsContent.innerHTML = '<div class="loading"></div> <span>Submitting and testing all cases...</span>';
    
    const results = [];
    let passed = 0;
    let failed = 0;
    
    console.log(`Starting submission with ${testCases.length} test cases`);
    
    // Clear the initial loading message and prepare for results
    resultsContent.innerHTML = '';
    
    // Run all test cases
    for (let i = 0; i < testCases.length; i++) {
        const testCase = testCases[i];
        const resultDiv = document.createElement('div');
        resultDiv.className = 'test-result running';
        resultDiv.innerHTML = `
            <div class="test-result-header">
                <span class="test-result-title">Test Case ${i + 1}</span>
                <span class="test-result-status">Running...</span>
            </div>
        `;
        resultsContent.appendChild(resultDiv);
        
        try {
            console.log(`Running test case ${i + 1}/${testCases.length}...`);
            const result = await executeCode(code, testCase.input);
            const normalizedActual = normalizeOutput(result.stdout);
            const normalizedExpected = normalizeOutput(testCase.output);
            const outputMatch = normalizedActual === normalizedExpected;
            const success = result.success && outputMatch;
            
            console.log(`Test Case ${i + 1} result:`, {
                success: success,
                resultSuccess: result.success,
                outputMatch: outputMatch,
                exitCode: result.exitCode
            });
            
            // Debug logging for failed cases
            if (!outputMatch) {
                console.log(`Test Case ${i + 1} failed:`, {
                    rawActual: result.stdout,
                    rawExpected: testCase.output,
                    normalizedActual: normalizedActual,
                    normalizedExpected: normalizedExpected,
                    actualLength: normalizedActual.length,
                    expectedLength: normalizedExpected.length
                });
            }
            
            if (success) passed++;
            else failed++;
            
            resultDiv.className = `test-result ${success ? 'passed' : 'failed'}`;
            resultDiv.innerHTML = `
                <div class="test-result-header">
                    <span class="test-result-title">Test Case ${i + 1}</span>
                    <span class="test-result-status ${success ? 'passed' : 'failed'}">
                        ${success ? 'PASSED' : 'FAILED'}
                    </span>
                </div>
                <div class="test-result-details">
                    <p><strong>Input:</strong></p>
                    <pre>${testCase.input}</pre>
                    <p><strong>Your Output:</strong></p>
                    <pre>${result.stdout || '(empty)'}</pre>
                    <p><strong>Expected Output:</strong></p>
                    <pre>${testCase.output}</pre>
                    ${result.stderr ? `<p><strong>Error:</strong></p><pre>${result.stderr}</pre>` : ''}
                    ${!outputMatch ? `<p style="color: #ff6b6b;"><strong>Output mismatch!</strong></p>` : ''}
                </div>
            `;
            
            results.push({ success, result, testCase });
        } catch (error) {
            console.error(`Test Case ${i + 1} error:`, error);
            failed++;
            resultDiv.className = 'test-result failed';
            resultDiv.innerHTML = `
                <div class="test-result-header">
                    <span class="test-result-title">Test Case ${i + 1}</span>
                    <span class="test-result-status failed">ERROR</span>
                </div>
                <div class="test-result-details">
                    <p style="color: #ff6b6b;">${error.message}</p>
                </div>
            `;
        }
    }
    
    console.log(`All test cases completed. Passed: ${passed}, Failed: ${failed}`);
    
    // Add summary
    const summary = document.createElement('div');
    summary.className = 'summary';
    summary.innerHTML = `
        <h4>Summary</h4>
        <p>Passed: <strong style="color: #51cf66;">${passed}/${testCases.length}</strong></p>
        <p>Failed: <strong style="color: #ff6b6b;">${failed}/${testCases.length}</strong></p>
        ${passed === testCases.length ? 
            '<div class="success-message">🎉 All test cases passed! Great job!</div>' :
            '<div class="error-message">❌ Some test cases failed. Please review your solution.</div>'
        }
    `;
    resultsContent.appendChild(summary);
}

async function executeCode(code, input) {
    const languageMap = {
        'cpp': { language: 'c++', version: '*' },  // Piston API uses 'c++' not 'cpp'
        'python': { language: 'python', version: '*' },
        'javascript': { language: 'javascript', version: '*' },
        'java': { language: 'java', version: '*' }
    };
    
    const langConfig = languageMap[currentLanguage];
    if (!langConfig) {
        throw new Error(`Unsupported language: ${currentLanguage}`);
    }
    
    // Handle different languages
    let files = [];
    if (currentLanguage === 'javascript') {
        // For JavaScript, ensure proper stdin handling
        if (!code.includes('readline')) {
            code = `const readline = require('readline');
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

rl.on('line', (line) => {
    ${code}
    rl.close();
});`;
        }
        files.push({ content: code });
    } else if (currentLanguage === 'java') {
        files.push({ content: code, name: 'Main.java' });
    } else {
        files.push({ content: code });
    }
    
    const payload = {
        language: langConfig.language,
        version: langConfig.version,
        files: files,
        stdin: input
    };
    
    const apiEndpoint = apiUrl.endsWith('/') ? apiUrl.slice(0, -1) : apiUrl;
    const executeUrl = apiEndpoint.includes('emkc.org') 
        ? `${apiEndpoint}/execute`
        : `${apiEndpoint}/api/v2/execute`;
    
    const response = await fetch(executeUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    });
    
    if (!response.ok) {
        if (response.status === 429) {
            throw new Error('Rate limit exceeded. Please wait a moment and try again.');
        }
        const errorText = await response.text();
        throw new Error(`API error: ${response.status} ${response.statusText}. ${errorText}`);
    }
    
    const data = await response.json();
    
    // Debug: log full API response structure
    console.log('API Response:', {
        hasCompile: !!data.compile,
        hasRun: !!data.run,
        compileStderr: data.compile?.stderr,
        runCode: data.run?.code,
        runCodeType: typeof data.run?.code,
        runCodeValue: data.run?.code,
        runStdout: data.run?.stdout?.substring(0, 50),
        fullData: data
    });
    
    // Check for compilation errors
    if (data.compile && data.compile.stderr) {
        return {
            success: false,
            stdout: '',
            stderr: `Compilation Error: ${data.compile.stderr}`,
            compileError: data.compile.stderr
        };
    }
    
    // Check for runtime errors
    const run = data.run || {};
    // Handle exitCode: 0 is a valid success code, so we need to check for null/undefined specifically
    const exitCode = (run.code !== undefined && run.code !== null) ? run.code : -1;
    const stdout = run.stdout || '';
    const stderr = run.stderr || '';
    
    const success = exitCode === 0;
    
    // Debug: log execution result
    console.log('Execution result:', {
        exitCode: exitCode,
        exitCodeType: typeof exitCode,
        success: success,
        stdoutLength: stdout.length,
        stderrLength: stderr.length,
        hasStderr: !!stderr
    });
    
    return {
        success: success,
        stdout: stdout,
        stderr: stderr,
        exitCode: exitCode
    };
}

function normalizeOutput(output) {
    if (!output) return '';
    // Normalize line endings first
    let normalized = output.replace(/\r\n/g, '\n').replace(/\r/g, '\n');
    // Split into lines, trim each line, filter out empty lines at the end
    let lines = normalized.split('\n');
    // Remove trailing empty lines
    while (lines.length > 0 && lines[lines.length - 1].trim() === '') {
        lines.pop();
    }
    // Trim each line and rejoin
    normalized = lines.map(line => line.trimEnd()).join('\n');
    return normalized;
}

function showError(message) {
    const resultsContent = document.getElementById('resultsContent');
    resultsContent.innerHTML = `<div class="error-message">${message}</div>`;
}

function showSuccess(message) {
    const resultsContent = document.getElementById('resultsContent');
    resultsContent.innerHTML = `<div class="success-message">${message}</div>`;
}
