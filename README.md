# LangChain - FastAPI

## Configuration
docker-compose.yml environment OpenAI API key
```yml
OPENAI_API_KEY=<YOUR-OPENAI-API-KEY>
```

## Start
```bash
docker-compose up
```

## Example
### URL

```bash
curl --location 'http://localhost:8000/url' \
--header 'Content-Type: application/json' \
--data '{
    "question": "カスタマイズ性があるのはどっち？",
    "urls": ["https://toyota.jp/gr86/", "https://toyota.jp/supra/"]
}'
```

### Format

```bash
curl --location 'http://localhost:8000/format' \
--header 'Content-Type: application/json' \
--data '{
    "message": "速い"
}'
```
