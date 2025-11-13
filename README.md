# Code Judge - Online Coding Platform

A LeetCode-style online coding platform with real-time code execution and automated test case evaluation. Supports multiple programming languages (C++, Python, JavaScript, Java) with a modern web interface.

## Features

- ✅ **Multi-language Support**: C++, Python, JavaScript, Java
- ✅ **Real-time Code Execution**: Execute code instantly via Piston API
- ✅ **Automated Test Case Evaluation**: Automatic testing with detailed results
- ✅ **Modern Web Interface**: Clean, responsive UI inspired by LeetCode
- ✅ **Self-hosted or Cloud Deployed**: Run locally or deploy to Railway
- ✅ **Rate Limiting**: Configurable rate limits (200 req/s default)
- ✅ **Test Case Management**: File-based test cases for scalability

## Project Structure

```
Testing Code/
├── frontend/                    # Frontend application
│   ├── index.html              # Main HTML file
│   ├── styles.css              # Styling
│   ├── app.js                  # Application logic
│   ├── server.py               # Development server
│   ├── debug.html              # Debug/testing page
│   └── README.md               # Frontend documentation
│
├── test_cases/                  # Test case files
│   ├── input1.txt ... input11.txt    # Test inputs
│   └── output1.txt ... output11.txt  # Expected outputs
│
├── language-packages/            # Pre-built runtime packages
│   ├── gcc/10.2.0/             # GCC compiler
│   ├── python/3.12.0/          # Python interpreter
│   ├── node/20.11.1/           # Node.js runtime
│   └── java/15.0.2/            # Java runtime
│
├── docker-compose.yml          # Docker services configuration
├── nginx.conf                  # NGINX reverse proxy config
├── Dockerfile.railway          # Railway deployment Dockerfile
├── railway.json                # Railway configuration
├── .railwayignore              # Railway ignore patterns
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for frontend server)
- Node.js (optional, for development)

### 1. Start the Piston API

```bash
# Start Piston API with NGINX reverse proxy
docker-compose up -d

# Verify API is running
curl http://localhost:2001/api/v2/runtimes
```

The API will be available at:
- `http://localhost:2000` (via NGINX with rate limiting)
- `http://localhost:2001` (direct access, bypassing NGINX)

### 2. Start the Frontend Server

```bash
# Create virtual environment (if not exists)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the frontend server
cd frontend
python server.py
```

The frontend will be available at `http://localhost:8000`

### 3. Open in Browser

Navigate to `http://localhost:8000` and start coding!

## Usage

### Running Code

1. **Select a Problem**: Click on a problem from the sidebar
2. **Choose Language**: Select your preferred language (C++, Python, JavaScript, Java)
3. **Write Code**: Write your solution in the code editor
4. **Run**: Click "Run" to test with the first test case
5. **Submit**: Click "Submit" to test with all test cases

### API Configuration

The frontend can connect to:
- **Local API**: `http://localhost:2000` (via NGINX) or `http://localhost:2001` (direct)
- **Railway API**: Enter your Railway URL in the custom field

### Test Cases

- Problem 1 uses file-based test cases (`test_cases/input*.txt` and `test_cases/output*.txt`)
- Other problems use inline test cases defined in `app.js`

## Problems

### Problem 1: Print Hello N Times
- **Difficulty**: Easy
- **Description**: Read a number `n` and print "Hello" `n` times
- **Test Cases**: 11 test cases (from files)

### Problem 2: Sum of Two Numbers
- **Difficulty**: Easy
- **Description**: Read two integers and print their sum

### Problem 3: Find Maximum
- **Difficulty**: Medium
- **Description**: Read `n` integers and print the maximum value

## Configuration

### Rate Limiting

Default rate limits (configured in `nginx.conf`):
- **Rate**: 200 requests per second
- **Burst**: 400 requests

To modify rate limits, edit `nginx.conf`:
```nginx
limit_req_zone $binary_remote_addr zone=piston_zone:10m rate=200r/s;
```

Then restart NGINX:
```bash
docker-compose restart nginx
```

### Environment Variables

The frontend supports environment variables for API URL:
```bash
export PISTON_API_URL=http://localhost:2000
```

## Deployment

### Railway Deployment

1. **Prepare for Deployment**:
   ```bash
   # Ensure language-packages directory has all runtimes
   ls language-packages/
   ```

2. **Deploy to Railway**:
   - Connect your GitHub repository to Railway
   - Railway will automatically detect `railway.json` and `Dockerfile.railway`
   - The deployment will include pre-installed runtimes

3. **Configure Railway**:
   - Set the port to `2000` (or Railway's assigned port)
   - The API will be available at your Railway URL

### Docker Deployment

For production Docker deployment:
```bash
# Build the image
docker build -f Dockerfile.railway -t code-judge-api .

# Run the container
docker run -p 2000:2000 code-judge-api
```

## API Endpoints

### Piston API Endpoints

- `GET /api/v2/runtimes` - List available runtimes
- `POST /api/v2/execute` - Execute code
  ```json
  {
    "language": "python",
    "version": "3.12.0",
    "files": [{"content": "print('Hello')"}],
    "stdin": ""
  }
  ```

### Frontend Server Endpoints

- `GET /` - Main frontend page
- `GET /test_cases/input*.txt` - Test case inputs
- `GET /test_cases/output*.txt` - Test case outputs

## Development

### Running Tests

```bash
# Test frontend integration
python test_frontend_integration.py

# Test frontend server
./test_frontend.sh
```

### Debugging

Access the debug page at `http://localhost:8000/debug.html` for detailed output comparison and testing.

### Adding New Problems

Edit `frontend/app.js` and add a new problem object to the `problems` array:

```javascript
{
    id: 4,
    title: "Your Problem Title",
    difficulty: "medium",
    description: `<h3>Problem</h3><p>Description...</p>`,
    testCaseFiles: [
        { input: "1 2", output: "3" },
        // ... more test cases
    ],
    starterCode: {
        cpp: `// C++ starter code`,
        python: `# Python starter code`,
        // ... other languages
    }
}
```

## Troubleshooting

### API Not Accessible

```bash
# Check if containers are running
docker ps

# Check API logs
docker logs piston-api

# Check NGINX logs
docker logs piston-nginx
```

### Test Cases Not Loading

- Ensure `frontend/server.py` is running
- Check that `test_cases/` directory exists
- Verify file permissions

### Code Execution Fails

- Check browser console for errors
- Verify the selected language is supported
- Check Piston API logs: `docker logs piston-api`
- Ensure runtimes are installed: `curl http://localhost:2001/api/v2/runtimes`

### Rate Limit Errors

- Check NGINX rate limit configuration
- Verify you're not exceeding 200 req/s
- Check NGINX logs for 429 errors

## Architecture

### Components

1. **Frontend** (Browser)
   - HTML/CSS/JavaScript application
   - Code editor and problem display
   - Results panel

2. **Frontend Server** (Python)
   - Serves static files
   - Serves test case files
   - Development server

3. **NGINX** (Reverse Proxy)
   - Rate limiting
   - Request routing
   - CORS headers

4. **Piston API** (Docker)
   - Code execution engine
   - Runtime management
   - Sandboxed execution

### Data Flow

```
User Browser
    ↓
Frontend Server (Port 8000)
    ↓
Test Cases (input*.txt, output*.txt)
    ↓
User Browser
    ↓
NGINX (Port 2000) → Piston API (Port 2000)
    ↓
Code Execution
    ↓
Results → User Browser
```

## Technologies Used

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Backend**: Python 3.11, Node.js (Piston API)
- **Containerization**: Docker, Docker Compose
- **Reverse Proxy**: NGINX
- **Deployment**: Railway
- **Code Execution**: Piston API

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available for educational purposes.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the logs (`docker logs`)
3. Check browser console for frontend errors
4. Verify all services are running

## Acknowledgments

- [Piston API](https://github.com/engineer-man/piston) - Code execution engine
- [Railway](https://railway.app) - Deployment platform

---

**Note**: This project requires Docker and Docker Compose to run the Piston API. The frontend can run independently for development, but requires the API for code execution.
