To do list:

Wat is er nodig om het game element te implementeren

* session id
    * "inlog" dus je username waarmee ook je score wordt gelinkt.
    * Zorgen dat deze username wordt toegevoegd aan een active room.

1. Klik create room
2. Er wordt een room aangemaakt met unieke code en door user gekozen naam
3. user joint deze room automatisch
4. deze room is een object wat bijhoudt welke spelers in de room zitten.
5. Zodra alle spelers op de ready check hebben geklikt kan het spel worden gestart.
6. Op het moment van starten wordt er uit de spelers een random quizmaster gekozen.
7. Deze krijgt via een pop-up box de keuze uit 3 categorieen.
8. Zodra een categorie wordt geselecteerd wordt er een format string naar de API server gestuurd.
9. Van de API moet een set vragen terugkomen. 
10. Deze vragen worden gesteld via de lobby.
11. Zodra de vraag gesteld is gaat er een timer lopen. binnen 10 seconden moet het antwoord gegeven worden.
12. Spelers krijgen punten voor het goed en snel beantwoorden van een vraag.
13. De winnaar is degene met de meeste punten.