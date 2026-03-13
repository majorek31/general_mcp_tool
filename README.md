# Installation

before connecting please uncomment lines 20-27 in tool_discovery_service.py

after first run, comment them back and start the program

this is made for now to simplyfy pgvector and not add redundant embeddings.

After that run program as is.

via py ./src/main.py

# 13.03.2026
## Problems
### `get weather for cieszyn`
    - Has returned python code instead of using tools

### Solve
    - Implement tool discovery and provide planner with tool name and description


### Embedding

Napotlaimsy problemy z reprezentacja sematyczna tooli 

- Retrival zwracał zle narzędzie
- Baza danych nam nie dzialala
- Kolizje miedzy toolami ( niektore sa podobne)

solution?

- Klasyfikacja zamiast retrival?

- (wpakować wszystkie toole???) - koncowo to zrobilismy

- Podejście oparte WYŁACZNIE na similarity search odpada, dopóki nie douczymy się lepiej tematu w pythonie.
