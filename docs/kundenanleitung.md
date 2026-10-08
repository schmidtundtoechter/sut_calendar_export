# Anleitung: ERPNext-Aufgaben im Outlook-Kalender anzeigen

Mit dieser Funktion werden Aufgaben aus ERPNext in Outlook angezeigt. Die
Aufgaben bleiben in ERPNext angelegt und verwaltet. Outlook zeigt sie nur als
abonnierten Kalender an; Aenderungen in Outlook werden nicht nach ERPNext
uebertragen.

## Voraussetzung

Damit eine Aufgabe im Kalender erscheint, muss sie in ERPNext ein Datum im Feld
**Date** haben. Aufgaben ohne Datum werden nicht angezeigt.

## Einmalige Einrichtung

Die Einrichtung nimmt ein Benutzer mit der Rolle **System Manager** vor.

1. Melden Sie sich in ERPNext an.
2. Suchen Sie nach **Calendar Export Settings** und oeffnen Sie die Seite.
3. Aktivieren Sie **Enable Calendar Feed** und speichern Sie die Einstellungen.
4. Kopieren Sie die angezeigte **Outlook Feed URL**.
5. Oeffnen Sie Outlook und waehlen Sie "Kalender hinzufuegen" und danach
   "Aus dem Internet abonnieren". Die genaue Bezeichnung kann je nach
   Outlook-Version leicht abweichen.
6. Fuegen Sie die kopierte URL ein und bestaetigen Sie das Abonnement.

Der neue Kalender erscheint anschliessend in Outlook in der Kalenderliste. Sie
koennen ihn ein- oder ausblenden wie jeden anderen Kalender.

## Taegliche Nutzung

1. Legen oder bearbeiten Sie Aufgaben wie gewohnt im ERPNext-DocType `ToDo`.
2. Tragen Sie im Feld **Date** den gewuenschten Kalendertag ein.
3. Outlook uebernimmt die Aufgabe beim naechsten Abruf des abonnierten
   Kalenders.

ERPNext erzeugt den Kalender bei jedem Abruf neu. Es gibt keinen manuellen
Export. Wann Outlook die Aenderung anzeigt, bestimmt Outlook beziehungsweise
Microsoft; das kann etwas Zeit in Anspruch nehmen.

## Was Wird Angezeigt?

Pro datierter ERPNext-Aufgabe wird ein ganztagiger Kalendereintrag erzeugt.
Neben der Aufgabenbeschreibung koennen Prioritaet, Zuweisung und eine
ERPNext-Referenz angezeigt werden. Abgeschlossene oder stornierte Aufgaben
bleiben im Kalender mit ihrem jeweiligen Status erkennbar.

## Wichtiger Sicherheitshinweis

Die **Outlook Feed URL** enthaelt einen persoenlichen Zugangsschluessel. Behandeln
Sie diese URL wie ein Passwort und geben Sie sie nicht an unbeteiligte Personen
weiter. Wenn sie versehentlich weitergegeben wurde, aendern Sie den Token in
**Calendar Export Settings** und richten Sie den Kalender in Outlook mit der
neuen URL erneut ein.
