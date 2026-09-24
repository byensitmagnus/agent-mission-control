# Produktmål

Gør det nemmere for Byens IT og andre at få krævende AI-opgaver helt færdige: Brugeren beskriver det ønskede resultat, mens AMC hjælper agenten med at finde den relevante viden, organisere arbejdet og levere et kontrolleret resultat.

Når AMC er valgt i hosten, skal en almindelig opgavebeskrivelse være nok til at starte. Brugeren angiver resultat, rammer og hvad der gør opgaven færdig; agenten afklarer kun nødvendige mangler. Brugeren skal ikke først skrive avancerede prompts, udvælge kontekst til hver underagent eller tegne en arbejdsgraf. Hosten ejer stadig indlæsning, værktøjer og tilladelser.

AMC skal bære det praktiske koordineringsarbejde:

1. **Relevant kontekst:** Find de nødvendige filer, fakta og beslutninger. Overdrag dem med kilde og aktuel version, og hent mere, når en konkret mangel viser sig.
2. **Rigtig rækkefølge:** Genkend hvilke resultater næste trin behøver. Vent på dem; udfør uafhængigt arbejde parallelt, når det gavner.
3. **Passende hjælp:** Brug direkte arbejde, en specialist eller flere uafhængige jobs efter opgaven. Én lead samler arbejdet og har ansvaret for resultatet.
4. **Et brugbart resultat:** Afslut mod brugerens acceptkriterier, ret konstaterede fejl og vis hvad der faktisk blev kontrolleret.
5. **Kontinuitet:** Bevar mål, beslutninger, artefakter og næste handling, så arbejdet kan genoptages uden at brugeren rekonstruerer forløbet.

Det er vores praktiske brug af **context engineering** og **graph engineering**: relevant viden ved det trin, der behøver den, og afhængigheder mellem konkrete arbejdsresultater. En grafdatabase, et fast agenthold eller et ekstra system er ikke et krav.

Designvalg skal bygge på vores inspirationsrepos og officielle AI-dokumentation, med spor fra kilde til lokalt problem og brugeropgave; se [kildekortet](../docs/field-state.md). Debat på X kan pege på noget, der skal undersøges. Popularitet alene er ikke et acceptkriterium.

# Exit gate for denne leverance

1. Tydelig og indbydende GitHub-præsentation
README forklarer målgruppe, konkret nytte og første handling. Grafik, navigation og eksempler fungerer i den renderede visning, også på smal skærm. Links, About-tekst og emneord passer til det faktiske produkt. Gem før/efter-visning.

2. Installation fører til faktisk brug
En ny bruger kan følge vejledningen, installere den aktuelle version og vælge den i mindst én tilgængelig, relevant host. Kontrollér både filindhold og faktisk indlæsning. MATCH alene er utilstrækkeligt. Andre hosts har tydelig status og dokumenterede begrænsninger.

3. Ét konkret arbejdsforløb er gennemført
Brug eksisterende, kontrollerbar erfaring eller én afgrænset, reel opgave til at vise vejen fra brugerens almindelige målbeskrivelse til en accepteret leverance. Spor den valgte kontekst, relevante afhængigheder, eventuelle overdragelser og slutkontrollen. Vis hvilket koordineringsarbejde agenten håndterede, og hvad brugeren stadig måtte gøre. Knyt den konkrete produktforbedring til en fundet fejl eller friktion og kontrollér rettelsen. Demonstrér genoptagelse, hvis forløbet kræver det. Tving ikke flere agenter ind i en opgave alene for demonstrationen.

4. Produktet hænger sammen
Skill, referencer, templates, eksempler, installationsvejledning og versionsstatus er indbyrdes konsistente. Direkte arbejde er standard; én specialist kan bruges for ekspertise eller frisk kontekst, og parallelle jobs kræver uafhængige input og passende isolation. Overdragelser bevarer ejerskab, nødvendige artefakter og acceptkriterier. Relevante eksisterende checks består på den konkrete version, også på det installerede indhold. Kendte fejl, der hindrer de lovede brugerforløb, er løst. Ny research eller flere regler skal begrundes i et konkret behov.

5. Den færdige version kan tages i brug
Ændringerne er samlet, reviewet og publiceret på main inden for det aktuelle mandat. Den aftalte projektinstallation bruger denne version. Projektstatus viser præcis leverance og evidens. Ingen nødvendige opgaver gemmes som fremtidige forbedringer; øvrige idéer får en kort backlog.

# Afgrænsning og bevis

AMC forbliver en portabel skill, hvor hosten leverer agenter, værktøjer og isolation.

Ingen stor benchmarkkampagne. Brug målrettede engineering-checks og konkret brugserfaring. Påstande om generelt bedre kvalitet, pris eller hastighed kræver særskilt evidens og er ikke nødvendige for denne exit gate.

Headless automatisering er ikke et krav. Faktisk brug i hosten er. Hvis en kontrol kræver UI, brug UI-adgang eller identificér den præcise nødvendige brugerhandling.

Et manglende bevis skal stå åbent. Fjern ikke et succeskriterium for at kunne erklære målet nået.

Produktmålet består efter denne leverance. En senere forbedring skal kunne pege på et konkret problem i brugen, den ændrede mekanisme og en relevant kontrol eller faktisk observation. Denne exit gate afslutter en brugsklar version; den beviser ikke generel produktivitetsgevinst eller at AMC er færdigudviklet.

PR #10 og kontrollerne fra 2026-09-23 er delmilepæle, ikke denne exit gate.

Udgangspunktet er `main` ved `3f35485`. Hele repoet, den tilgængelige historik, PR #7–10 og de eksisterende lokale ændringer indgår i gennemgangen. Aktuel fremdrift og fastlagte kontroller står i `MISSION.md`.

_Opdateret: 2026-09-24_
