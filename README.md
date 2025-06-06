# Instagram Non-Followers Checker

A Python script that helps you identify Instagram accounts you follow but who don't follow you back, using the `instaloader` library.

## Features

- 🔒 Secure login via Instagram credentials (entered at runtime; **never stored**)
- 🔐 Two-factor authentication (2FA) support
- 📊 Retrieves and compares followers and followees
- 📝 Outputs usernames who don't follow you back
- 💾 Saves results locally in `not_following_back.txt`

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/instagram-unfollow.git
cd instagram-unfollow
```

2. Install the required package:
```bash
pip install instaloader
```

## Usage

1. Run the script:
```bash
python check_nonfollowers.py
```

2. Enter your Instagram credentials when prompted:
   - Username
   - Password
   - 2FA code (if enabled)

3. The script will:
   - Fetch your followers and following lists
   - Compare them to identify non-followers
   - Display results in the console
   - Save results to `not_following_back.txt`

## Privacy & Security

This project is designed with privacy and security as top priorities:

- **No Credential Storage**
  - Credentials are requested only at runtime
  - Never saved or logged
  - No persistent storage of sensitive data

- **Local Data Processing**
  - All processing happens on your machine
  - No data transmission to external servers
  - Results stored only in local text file

- **Security Best Practices**
  - Avoid hardcoding credentials
  - Don't commit sensitive files to repositories
  - Use `.gitignore` for session files and tokens
  - Enable 2FA for your Instagram account

## Disclaimer

This tool is provided "as is" without warranty. Use at your own risk. The author is not responsible for any misuse or consequences resulting from use of this script.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [instaloader](https://instaloader.github.io/) - The library that makes this possible
- All contributors who have helped improve this project

---

By using this tool, you acknowledge that you understand and accept the privacy and security practices outlined above.
