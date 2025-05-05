## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/avtomatik/marine_cargo.git
   cd marine_cargo
   ```

2. Create a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:

   ```bash
   pip install --no-cache-dir -r requirements.txt
   ```

4. Set up environment variables:

   Create a `.env` file based on the provided `.env.example` and configure your environment variables accordingly.

## Usage

Run the following commands to load initial data and start the development server:

```bash
python3 manage.py load_samples   # You Shall Have All Your Back-Up .csv's
python3 manage.py runserver
```

Ensure that your environment variables are properly configured before running the application.

## Contributing

Contributions are welcome! Please fork the repository, create a new branch, and submit a pull request with your proposed changes.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

---
