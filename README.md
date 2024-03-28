# Pyphoria
A reimagination of the lotgd framework in Python

## Development

### Setup

Install dependencies

```shell
poetry install --with=dev
```

The `dev` group contains uvicorn which can be used to start the webserver.

### Development Server

```shell
uvicorn pyphoria.main:app --reload
```

You can then navigate to <http://127.0.0.1:8000/docs/> to view the OpenAPI interface.
