# Code Judge Frontend

A LeetCode-style coding platform frontend with multiple language support.

## Features

- ✅ Multiple programming languages (C++, Python, JavaScript, Java)
- ✅ Real-time code execution via Piston API
- ✅ Test case evaluation
- ✅ Problem selection
- ✅ Code editor with syntax highlighting
- ✅ Results panel with detailed feedback

## Quick Start

### 1. Start the Frontend Server

```bash
cd frontend
python server.py
```

Or if using Python 3 explicitly:
```bash
python3 server.py
```

The server will start on `http://localhost:8000`

### 2. Start Your Piston API

Make sure your Piston API is running:

```bash
# Local API
docker-compose up -d

# Or Railway API URL
# Set it in the frontend dropdown
```

### 3. Open in Browser

Navigate to: `http://localhost:8000`

## Usage

1. **Select a Problem**: Click on a problem from the sidebar
2. **Choose Language**: Select your preferred language from the dropdown
3. **Write Code**: Write your solution in the code editor
4. **Run**: Click "Run" to test with the first test case
5. **Submit**: Click "Submit" to test with all test cases

## API Configuration

The frontend can connect to:
- Local API: `http://localhost:2000` (via NGINX) or `http://localhost:2001` (direct)
- Railway API: Enter your Railway URL in the custom field

## Problems

### Problem 1: Print Hello N Times
- Reads a number `n` and prints "Hello" `n` times
- Uses test cases from `test_cases/` folder (input1.txt - input11.txt)

### Problem 2: Sum of Two Numbers
- Reads two integers and prints their sum

### Problem 3: Find Maximum
- Reads `n` integers and prints the maximum value

## File Structure

```
frontend/
├── index.html      # Main HTML file
├── styles.css      # Styling
├── app.js          # Application logic
├── server.py       # Development server
└── README.md       # This file
```

## Testing

The frontend will:
1. Load test cases from `test_cases/` folder (for Problem 1)
2. Execute code via Piston API
3. Compare outputs with expected results
4. Show detailed results for each test case

## Troubleshooting

**Test cases not loading?**
- Make sure `server.py` is running
- Check that `test_cases/` folder exists in parent directory

**API connection failed?**
- Verify Piston API is running: `curl http://localhost:2001/api/v2/runtimes`
- Check API URL in the frontend dropdown
- Check browser console for CORS errors

**Code execution fails?**
- Check browser console for errors
- Verify the selected language is supported
- Check Piston API logs: `docker logs piston-api`

