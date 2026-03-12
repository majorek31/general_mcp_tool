Ten sam environment z użyciem uv

uv - https://docs.astral.sh/uv/


Poinstalować sobie paczuszki
- langchain
    - embeddings:
        - https://docs.langchain.com/oss/python/langchain/knowledge-base#pgvector
- langgraph
- openai (?)
- ... (?)

Setup środowiska devops
- docker-compose <-- baza danych, pgvector <- kwestia z przechowywaniem embeddingów ogarnięta


Schemat działania (Góra - Dól):

12.03.2026 - plan działania - 1 iteracja:

1. Na start aplikacji utworzyć bazę narzędzi (tools) i dodać ją do bazy danych, jako embeddingi (pgvector).
    - To będzie składać się nazwa_narzedzia, opis narzędzia, parametry (??), przykładowe użycie <-- zwalidować w trakcie testów manualnych.
    - Sprawdzić długość tych tekstów średnio ~. Najpopularniejsze wartości to 256,512,1024,1536,2048 <--- sprawdzić, czy nie przekraczamy tego górnego limtu.


2. Utworzyć workflow like this:

Serwer MCP
--------------
Expose one tool for everything:
    - create mcp tool
    - create proper describtion
    //TODO: do zweryfikowania po jakimś czasie
    - create proper input schema (??) <- na razie bardzo prosty tylko query (?), zobaczymy, czy to wystarczy
---------------
Utworzyć agenta do:
 - witania i dzielenia prompta na kroki (steps)
 Jakie problemy możemy na potkać implementując tego agenta?:
    - jak dzielić prompta na kroki? (??) <- jaki mam być system prompt? Rodziel na etapy rozwiązania problemu. 
        Nie zawsze musi to być krok(?). Może zwykłe pytanie?
    - jak rozróżnić problem, pytanie, rozkaz?

Output:
- Lista kroków (steps)

Rozważyć:
 - może dodać agenta sprawdzającego, czy prompt wymaga dzielenia na kroki? -> proste pytanie, czy trudne, długi i skomplikowane

---------------

Dla każdego kroku szukamy odpowiednich narzędzi.
To będzie wymagało:
    1. Mieć bazę.
    2. Mieć embeddingi narzędzi.
    3. Utworzyć w "locie" embeddingi dla każdego z kroków.
    //TODO: zweryfikować
    4. Porównać i wziąc __5__ (do zmiany ) najlepszych narzędzi dla każdego kroku.

Output:
- Lista narzędzi dla każdego kroku.

---------------

Tworzenie dynamicznie agentów dla każdego z kroków.
Każdy agent ma toola odpowiedniego dla siebie, dla kroku, który ma wykonać.
Utworzyć generycznego agenta, który będzie elastyczny na tyle, że będzie można mu podać dowolne narzędzie i będzie w stanie z niego skorzystać.
**DUŻĄ UWAGĘ poświęcić system promptowi!!!**

---------------

If ilość_kroków > 1:
    Sumowanie i generowanie odpowiedzi. (agregator)
If ilość_kroków == 1:
    Zwrócenie odpowiedzi z konkretnego poprzedniego agenta.



Dodatkowe uwagi:
 - logować ile się da, a zwłaszcza użycie tooli!
