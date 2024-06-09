# clinical-agent

This project is designed for a simple LLM agent with tools on a clinical knowledge graph in Neo4j.

![Workflow diagram](https://raw.githubusercontent.com/tomasonjo/clinical-agent/main/static/clinical.png)

## Setup

1. Download and restore the [Clinical database dump](https://drive.google.com/file/d/1r5mHYuDjl-ilB8_vqgCqMUnziqGbOete/view?usp=drive_link).

2. Set environment variables in `.env`.

3. Run the following command:

```
docker compose up 
```

## Example questions

*  What are associated foods with cancer?
*  What are known clinically relevant gene variants for gene CLN3?
*  In which tissues are expressed proteins associated with prostate carcinoma?

## Todo

* Better entity mapping from input to database (Using a combination of keyword search and/or biomedical text embeddings)
* More tools

## Contributions

Contributions are welcomed