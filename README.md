# Summarify

**AI-Powered PDF Summarization Application**

Summarify is an intelligent web application that automatically extracts and summarizes content from PDF documents using advanced AI models. Built with Django REST Framework and Hugging Face Transformers.

---

## 🚀 Features

- **User Authentication**: Secure JWT-based authentication system
- **PDF Upload**: Upload PDF documents through RESTful API
- **Automatic Text Extraction**: Extract text content from PDF files
- **AI Summarization**: Generate concise summaries using BART-large-CNN model
- **Document Management**: View, list, and delete uploaded PDFs
- **Custom Summarization**: Re-generate summaries with customizable length parameters

---

## 📋 Table of Contents

- [Backend Setup](#backend-setup)
- [API Documentation](#api-documentation)
- [AI Model Information](#ai-model-information)
- [Project Structure](#project-structure)
- [Technologies](#technologies)
- [Future Enhancements](#future-enhancements)

---

## 🔧 Backend Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/Mohammed-Mahmoud0/Summarify.git
   cd Summarify/Backend
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv env
   # Windows
   .\env\Scripts\activate
   # Linux/Mac
   source env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment (Optional)**
   
   To store AI models on a different drive, set environment variable:
   ```bash
   # Windows
   setx HF_HOME "D:\huggingface_cache"
   # Linux/Mac
   export HF_HOME="/path/to/cache"
   ```

5. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser (Optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000`

---

## 📚 API Documentation

### Authentication Endpoints

#### Register User
```http
POST /api/auth/register/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

#### Login
```http
POST /api/auth/login/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}

Response:
{
    "access": "jwt_access_token",
    "refresh": "jwt_refresh_token"
}
```

#### Refresh Token
```http
POST /api/auth/token/refresh/
Content-Type: application/json

{
    "refresh": "jwt_refresh_token"
}
```

### PDF Summarizer Endpoints

**Note**: All summarizer endpoints require authentication. Include JWT token in header:
```
Authorization: Bearer <your_access_token>
```

#### Upload PDF
```http
POST /api/summarizer/pdfs/
Content-Type: multipart/form-data
Authorization: Bearer <token>

FormData:
- file: <pdf_file>

Response:
{
    "id": 1,
    "file": "http://localhost:8000/media/pdfs/document.pdf",
    "extracted_text": "Full extracted text...",
    "summary": "AI-generated summary...",
    "created_at": "2025-12-10T10:30:00Z"
}
```

#### List All PDFs
```http
GET /api/summarizer/pdfs/
Authorization: Bearer <token>

Response:
[
    {
        "id": 1,
        "file": "http://localhost:8000/media/pdfs/document.pdf",
        "extracted_text": "Full text...",
        "summary": "Summary...",
        "created_at": "2025-12-10T10:30:00Z"
    }
]
```

#### Get Specific PDF
```http
GET /api/summarizer/pdfs/{id}/
Authorization: Bearer <token>
```

#### Delete PDF
```http
DELETE /api/summarizer/pdfs/{id}/
Authorization: Bearer <token>
```

#### Re-Summarize PDF
```http
POST /api/summarizer/pdfs/{id}/summarize/
Content-Type: application/json
Authorization: Bearer <token>

{
    "max_length": 200,
    "min_length": 50
}

Response:
{
    "id": 1,
    "summary": "Updated summary...",
    ...
}
```

---

## 🤖 AI Model Information

### Model Details
- **Model**: `facebook/bart-large-cnn`
- **Type**: Sequence-to-sequence transformer for abstractive summarization
- **Size**: ~1.6 GB
- **Training Data**: CNN/DailyMail dataset
- **Language**: English

### How It Works

1. **Text Extraction**: PyPDF2 extracts raw text from uploaded PDF
2. **Text Cleaning**: Removes extra whitespace and normalizes formatting
3. **Chunking**: Long documents are split into 1024-token chunks (BART's limit)
4. **Summarization**: Each chunk is summarized independently
5. **Combination**: Chunk summaries are merged and re-summarized if needed
6. **Optimization**: Model is loaded once and cached for subsequent requests

### Model Caching
- **First Run**: Downloads model (~1.6GB) to cache directory
- **Subsequent Runs**: Uses cached model (instant loading)
- **Default Cache**: `C:\Users\<username>\.cache\huggingface\`
- **Custom Cache**: Set `HF_HOME` environment variable

### Performance
- **First Request**: 5-10 seconds (model loading)
- **Subsequent Requests**: 2-5 seconds (inference only)
- **Memory Usage**: ~2-3 GB RAM

### Limitations
- **Language**: Optimized for English text only
- **Input Length**: Best results with documents under 10,000 words
- **Quality**: Depends on PDF text extraction quality

---

## 📁 Project Structure

```
Summarify/
├── Backend/
│   ├── accounts/               # User authentication app
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── config/                 # Django project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── summarizer/             # PDF summarization app
│   │   ├── models.py           # PDFDocument model
│   │   ├── serializers.py      # API serializers
│   │   ├── views.py            # ViewSets
│   │   ├── urls.py             # API routing
│   │   └── utils/
│   │       ├── ai_engine.py    # AI summarization logic
│   │       └── utils.py        # PDF extraction utilities
│   ├── manage.py
│   └── requirements.txt
├── Frontend/                   # (Future implementation)
└── README.md
```

---

## 🛠️ Technologies

### Backend
- **Django 6.0**: Web framework
- **Django REST Framework 3.16**: API development
- **djangorestframework-simplejwt 5.5**: JWT authentication

### AI & ML
- **Transformers 4.x**: Hugging Face library
- **PyTorch**: Deep learning framework
- **facebook/bart-large-cnn**: Summarization model

### PDF Processing
- **PyPDF2 3.0**: PDF text extraction

### Database
- **SQLite**: Development database (default)
- **PostgreSQL**: Production (recommended)

---

## 🔮 Future Enhancements

### Planned Features
- [ ] Frontend web interface (React)
- [ ] Support for multiple languages (Arabic, Spanish, etc.)
- [ ] Batch PDF processing
- [ ] Export summaries to Word/PDF
- [ ] Summary history and comparison
- [ ] Adjustable summary styles (brief, detailed, bullet points)
- [ ] Support for scanned PDFs (OCR integration)
- [ ] User usage analytics and statistics

---

## 📝 License

MIT License

---

## 👤 Author

**Mohammed Mahmoud**
- GitHub: [@Mohammed-Mahmoud0](https://github.com/Mohammed-Mahmoud0)

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

---

**Note**: This project is under active development. The frontend will be added in future updates.
