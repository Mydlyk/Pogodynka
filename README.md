Dokumentacja aplikacji „Pogodynka”

Opis uruchomienia Aplikacji
Pogodynka została stworzony w pliku py w języku python z wykorzystaniem freameworka graficznego streamlit. Do uruchomiania aplikacji wymagane jest środowisko python(osobiście korzystałem z wersji pythona 3.12) oraz IDE obsługujące pliki pythonowe np. Visual Studio Code(z którego korzystałem). Do poprawnego działania aplikacji wymagane są następujące biblioteki:
langchain==0.1.16
langchain_core==0.1.43
python-decouple==3.8
Requests==2.31.0
streamlit==1.33.0
openai
Spis potrzebnych bibliotek znajduję się również w pliku „requirements.txt”.
W pliku .env znajdują się klucze potrzebne do poprawnego działania aplikacji.
Klucz Open_Api_Key z pozyskany https://openai.com/.
Login oraz hasło dla api DATAFORSEO pozyskane z https://app.dataforseo.com/
 ![image](https://github.com/Mydlyk/Pogodynka/assets/65900710/53bed0e5-dc54-425d-aad2-14da77c68ebb)

Aplikację uruchomiamy poprzez wykonanie polecenia  w terminalu:
 ![image](https://github.com/Mydlyk/Pogodynka/assets/65900710/ee332082-e3e7-431e-a65d-45533f5114d0)

streamlit run  Pogodynka.py
Uruchomiona aplikacja powinna znajdować na adresie http://localhost:8501/
Opis uruchomienia Aplikacji Docker
Pierwszym krokiem jest zbudowanie obrazu z pliku Dockerfile. 
Przykładowa komenda budująca obraz:
 ![image](https://github.com/Mydlyk/Pogodynka/assets/65900710/43005707-9fa1-49fc-ab87-27e966b167d4)

docker build -f Dockerfile -t pogodynka .  
Następnym krokiem jest uruchomienie/stworzenie kontenera z obrazu.
 Przykładowe polecenie:
 ![image](https://github.com/Mydlyk/Pogodynka/assets/65900710/fcacbe6e-9c5e-400c-a0e3-f7c1922b7850)

docker run --name Pogodynka -p 8501:8501 pogodynka
Uruchomiona aplikacja powinna znajdować na adresie http://localhost:8501/.

Opis działania aplikacji
Aplikacja jest chatem ze sztuczną inteligencją ,który wykorzystuje 2 agentów Ai jednego do prowadzenia konwersacji i drugiego do formatowania pytań. Główny agent przeszukuje informacje o pogodzie w polskich miastach i odpowiada na pytanie jedynie związane z pogodą w języku polskim. Chat utrzymuje również kontekst konwersacji i wypowiedzi.
Aplikacja pobiera z api dane o pogodzie w polskich miastach oraz  za pomocą api DATAFORSEO przeszukuje Internet w celu pozyskania informacji dla Agenta. Agent analizuje pozyskane dane, zadane pytanie, całkowity kontekst oraz stosuje się do zasad ustalonych w promp’cie. Gdy pytanie nie są jednoznacznym zapytaniem dla przeglądarki drugi Agent analizuje je i na podstawie wcześniejszej historii i zwraca nowe pytania dla api DATAFORSEO(Przykład Jaka będzie pogada agent zwróci Jaka będzie jutro pogoada w Lublinie?). Gdy pytanie nie dotyczy pogody aplikacja odpowiada że nie jest to pytanie o pogodę.
Opis kodu aplikacji
![image](https://github.com/Mydlyk/Pogodynka/assets/65900710/f8e67523-4c9f-46cb-9795-8957ddf17846)
 
Wykorzystanie kluczy api oraz zainicjalizowanie modelu sztucznej inteligencji temperatura oraz konkretny model openai które najlepiej odpowiadały to Temperatura=0 oraz model chat gpt 3.5-Turbo.
![image](https://github.com/Mydlyk/Pogodynka/assets/65900710/b9b26a1e-70e1-46aa-9639-0d6ed4d40ed7)

Stworzenie prompta dla agenta w którym są ustalone zasady działania oraz przekazane są dane takie jak język, pytanie, kontekst, historia_chatu, i kroki działania.
![image](https://github.com/Mydlyk/Pogodynka/assets/65900710/1b7f07e6-70ac-4a18-b033-41927455fce1)
 
Stworzenie prompta dla pomocniczego agenta tworzącego pytania dla DATAFORSEO jeśli pytanie jest zadane poprawnie nie zmienia go.

![image](https://github.com/Mydlyk/Pogodynka/assets/65900710/01ff1808-c79d-4468-8242-f4f73c16528a)

Stworzenie dwóch agentów.
![image](https://github.com/Mydlyk/Pogodynka/assets/65900710/351f4eb4-f9dc-45e5-804e-edaaed2b89e2)
 
Funkcja generate_ai_response na podstawie st.session_state.chat_history(tutaj zapisywana jest historia chatu) tworzy historię chatu. Kolejnym krokiem jest stworzenie executora dla agenta pomocniczego następnie pierwszy response przechowuje odpowiedz pierwszego agenta. Zmienna json_wrapper przechowuje wyniki z wyszukiwanie w internecie przez DataForSeoAPIWrapper top_count oznacza górne 3 wyszukiwania, jso_results_fields okreśa jak dane zostały pobrane a w params ustawiona jest przeglądarka wyszukiwania.
Następnie Wywoływane jest wyszukiwanie i przypisane do zmiennej context.
Kolejny respone jest odpowiedzią drugiego agenta na zadane pytanie na podstawie kontekstu, pytania i historii. Funkcja zwraca wynik wyszukiwania w internecie i odpowiedz chatu, gdy coś pójdzie nie tak zwraca puste obiekty.
![image](https://github.com/Mydlyk/Pogodynka/assets/65900710/d92c5db0-723a-492b-b5a2-fef5331f7beb)
 
Funkcja pobierająca dane o pogodzie w polskich miast z api pogodowego (agen posiada informacje z internetu jak i api).
 ![image](https://github.com/Mydlyk/Pogodynka/assets/65900710/183dc302-2d50-4086-8853-01e178557aed)

W zmiennej search_history jest przechowywana historia przeglądania.
Oraz inicjalizacja chat’u do wpisywania pytań oraz tytuł aplikacji.
![image](https://github.com/Mydlyk/Pogodynka/assets/65900710/aa6b7576-0adb-4309-9fff-fa914c500633)
 
Dodanie do historii chatu nowych odpowiedzi oraz zaznaczenie przez kogo została ona dodana.
![image](https://github.com/Mydlyk/Pogodynka/assets/65900710/602c8be0-a387-42be-922d-12874d9d7cb7)
 
Wyświetlenie powitania przez bota na początku konwersacji.
 ![image](https://github.com/Mydlyk/Pogodynka/assets/65900710/157634a1-d6cf-490b-9c86-2a63806d7e05)

Ten kod odpowiada za wyświetlanie chatu.
![image](https://github.com/Mydlyk/Pogodynka/assets/65900710/393acdc4-9363-4d03-a00f-80345513a4f5)
 
Ten kod javascriptowy odpowiada za automatyczne scrolowanie w dół strony po dodaniu nowej wiadomości na wzór działania chatu gpt.
Działanie aplikacji
 ![image](https://github.com/Mydlyk/Pogodynka/assets/65900710/3f8e20a0-ba64-4125-80d2-649d080efd28)

Rysunek 1 Odpowiedz agenta w przypadku dostępu do internetu
 ![image](https://github.com/Mydlyk/Pogodynka/assets/65900710/77226c71-3bf1-442a-9424-f65f41b42ea2)

Rysunek 2 Sprawdzenie utrzymania kontekstu i porównania 2 miast
 ![image](https://github.com/Mydlyk/Pogodynka/assets/65900710/128ec321-fac3-4234-8815-9b0e28a87f4b)

Rysunek 3 Sprawdzenie czy chat odpowiada tylko na pogodę w polskich miastach
 ![image](https://github.com/Mydlyk/Pogodynka/assets/65900710/ffcada7b-6803-44c5-b3e3-4bf436d4538e)

Rysunek 4 Utrzymanie kontekstu wypowiedzi

