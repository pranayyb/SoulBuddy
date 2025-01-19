# SoulBuddy

SoulBuddy is a conversational spiritual AI platform designed to provide intelligent, context-aware responses by leveraging cutting-edge natural language processing (NLP) models and vector-based search capabilities. It combines the power of HuggingFace embeddings, AstraDB Vector Store, and the ChatGroq model to deliver personalized and relevant responses to user queries.

---

## Features

- **HuggingFace Embeddings**: Leverages `sentence-transformers/all-MiniLM-L6-v2` for text embeddings, enabling high-quality semantic similarity searches.
- **AstraDB Vector Store**: Stores and retrieves document embeddings for efficient similarity search.
- **ChatGroq Model**: Utilizes `mixtral-8x7b-32768` for generating contextually rich and accurate responses.
- **Customizable User Data Integration**: Enhances response generation by incorporating user-specific data.
- **FastAPI Framework**: Provides a robust and scalable API to interact with the system.
- **CORS Support**: Enables secure cross-origin requests for seamless integration with web applications.

---

## Tech Stack

- **Programming Language**: Python
- **Web Framework**: FastAPI
- **NLP Libraries**: LangChain
- **Database**: AstraDB (by Datastax)
- **Response Model**: ChatGroq

---

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/pranayyb/SoulBuddy.git
   cd SoulBuddy
   ```

2. **Set Up Environment**:
   Install required dependencies by creating a virtual environment:

   ```bash
   python3 -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```

3. **Environment Variables**:
   Create a `.env` file in the root directory and add the following:

   ```env
   GROQ_API_KEY=groq-api-key
   ASTRA_DB_API_ENDPOINT=your-astra-db-endpoint
   ASTRA_DB_APPLICATION_TOKEN=your-astra-db-token
   BASE_API_URL=base-api-url
   LANGFLOW_ID=langflow-id
   FLOW_ID=flow-id
   APPLICATION_TOKEN=<YOUR_APPLICATION_TOKEN>
   ENDPOINT=endpoint
   ```

4. **Run the Application**:

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

---

## API Endpoints

### **POST** `/generate/`

Generates a response to a user query.

#### Request Body

```json
{
  "query": "string",
  "user_data": {
    "key1": "value1",
    "key2": "value2"
  }
}
```

#### Response

```json
{
  "response": "Generated response based on query and user data."
}
```

### **POST** `/langflow-query/`

Generates a response by utilizing LangFlow API.

#### Request Body

```json
{
  "query": "string",
  "flow_id": "string",
  "langflow_id": "string",
  "user_data": {
    "key1": "value1",
    "key2": "value2"
  }
}
```

#### Response

```json
{
  "response": "Generated response based on LangFlow query and user data."
}
```

---

## How It Works

1. **Query Input**: A user submits a query along with optional user-specific data.
2. **Semantic Search**: The query is processed using HuggingFace embeddings to find relevant documents from the AstraDB Vector Store.
3. **Response Generation**: The query, user data, and relevant documents are combined to form a rich prompt, which is passed to the ChatGroq model for response generation.
4. **Response Delivery**: The generated response is returned via the API.

For the `/langflow-query/` endpoint:

1. **LangFlow Query**: The query is routed to the LangFlow API using the specified `flow_id` and `langflow_id`.
2. **Processing**: The LangFlow service processes the query and integrates user data for a comprehensive response.
3. **Delivery**: The final response is sent back via the API.

---

## Example

### Input Query

```json
{
  "query": "What are gemstones?",
  "user_data": {
    "interest": "geology"
  }
}
```

### Output Response

```json
{
  "response": "Gemstones are precious stones that have been used throughout history for healing and spiritual rituals. They are considered to be storehouses of empowerment, transmitting their power to wearers through contact with their bodies. This power can be beneficial or detrimental, depending on how the gemstone is used. All gemstones have magnetic powers in varying degrees, and many of them are believed to have therapeutic cures due to the vibrations and frequencies they emit.\n\nA life stone, specifically, is a gemstone for the Lagna lord, which can be worn throughout a person's life to experience its mystic powers. Wearing a life stone can remove obstacles and bless an individual with happiness, success, and prosperity."
}
```

---

## Development Notes

- **CORS Configuration**: Be cautious when using `allow_origins="*"` in production. Restrict origins to trusted domains.
- **Error Handling**: Ensure proper handling of exceptions for smoother user experience.
- **Security**: Do not hardcode sensitive credentials. Use environment variables for configuration.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---
