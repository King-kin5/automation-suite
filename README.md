# Social Engagement Automation

A Python-based automation tool for social media engagement. Currently supports Instagram, with plans to expand to other platforms.

## Features

- Automated likes, comments, and saves on Instagram posts and reels
- Human-like behavior with random delays and natural typing
- Session management to avoid frequent logins
- Robust error handling and logging
- Configurable engagement settings
- Support for both posts and reels

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/social-engagement-automation.git
cd social-engagement-automation
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with your Instagram credentials:
```
IG_USERNAME=your_username
IG_PASSWORD=your_password
IG_COMMENT=Your default comment (optional)
```

## Usage

Run the script:
```bash
python src/main.py
```

The script will:
1. Try to use a saved session if available
2. Log in if needed
3. Process the most recent posts/reels from the target profile
4. Log out and close the browser

## Configuration

You can modify the following settings in `src/utils/config.py`:
- `PROFILE`: Target Instagram profile
- `MAX_POSTS_TO_PROCESS`: Number of posts to process
- `COMMENT_VARIATIONS`: List of comment variations
- Chrome options and other settings

## Logs

Logs are stored in the `logs` directory:
- `error_log.txt`: Detailed error messages
- `failed_posts.txt`: URLs of posts that failed to process
- `success_log.txt`: Successful actions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 