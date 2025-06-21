# 🚢 Cargo Seal — Marine Cargo Insurance Tracker

A FastAPI-based backend for tracking marine cargo insurance, supporting features like vessel data services, bills of lading, policy coverage, and declaration processing from Excel files.

---

## 📦 Features

- Upload and process shipment declarations from Excel
- Manage vessel and cargo coverage data
- Expose RESTful APIs for coverage, policies, and vessels
- Render data using HTML templates (e.g. sheet names, operator info)

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/cargo-seal.git
cd cargo-seal
````

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Server

```bash
uvicorn app.main:app --reload
```

* The app will be live at: [http://127.0.0.1:8000](http://127.0.0.1:8000)
* API docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📁 Project Structure

```
cargo-seal/
├── app/
│   ├── main.py               # FastAPI app entrypoint
│   ├── routers/              # API route handlers
│   ├── services/             # Business logic (ExcelReader, etc.)
│   ├── schemas.py            # Pydantic models
│   ├── crud.py               # DB access functions
│   └── ...
├── templates/                # Jinja2 HTML templates
│   └── shipment_result.html
├── config/                   # Config and mapping files
│   └── column_map.json
├── requirements.txt
└── README.md
```

---

## 📝 Example API Usage

**Upload Shipment File:**

```http
POST /api/coverage/push
Content-Type: multipart/form-data
Body:
  file: your_excel_file.xlsx
```

Returns: HTML with sheet names and operator, or JSON depending on the endpoint.

---

## 📚 Tech Stack

* [FastAPI](https://fastapi.tiangolo.com/)
* [Pydantic](https://docs.pydantic.dev/)
* [Uvicorn](https://www.uvicorn.org/)
* [Pandas + openpyxl](https://pandas.pydata.org/) for Excel handling
* [Jinja2](https://jinja.palletsprojects.com/) for HTML rendering

---

## 🛡 License

MIT License. See [LICENSE](./LICENSE) for more info.
