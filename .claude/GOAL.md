# Mål

Gør Agent Mission Control til en sammenhængende, indbydende og brugsklar skill, der hjælper Byens IT og andre med at gennemføre krævende AI-opgaver.

Brugeren beskriver resultatet og rammerne. AMC hjælper agenten med at vælge passende arbejde, bruge specialister når det gavner, give dem den nødvendige kontekst, samle resultaterne og afslutte med relevante kontroller. Brugeren skal kunne genoptage arbejdet uden at rekonstruere hele forløbet.

Designet skal bygge på relevante erfaringer fra vores inspirationsrepos og officielle AI-dokumentation. Konkrete valg skal kunne spores til en kilde, et fund i repoet og den brugeropgave, de løser. Denne leverance skal gøre AMC klar til daglig brug.

Context engineering betyder her, at agenten finder og overdrager den relevante viden, beslutninger og filer. Graph engineering betyder, at den genkender reelle afhængigheder og kun starter arbejde, der har sine nødvendige input. Brugeren skal ikke selv bygge grafer, vælge en agentorganisation eller vedligeholde et ekstra system.

# Exit gate for denne leverance

1. Tydelig og indbydende GitHub-præsentation
README forklarer målgruppe, konkret nytte og første handling. Grafik, navigation og eksempler fungerer i den renderede visning, også på smal skærm. Links, About-tekst og emneord passer til det faktiske produkt. Gem før/efter-visning.

2. Installation fører til faktisk brug
En ny bruger kan følge vejledningen, installere den aktuelle version og vælge den i mindst én tilgængelig, relevant host. Kontrollér både filindhold og faktisk indlæsning. MATCH alene er utilstrækkeligt. Andre hosts har tydelig status og dokumenterede begrænsninger.

3. Ét konkret arbejdsforløb er gennemført
Brug eksisterende, kontrollerbar erfaring eller én afgrænset, reel opgave til at vise vejen fra mål til leverance. Vis passende arbejdsdeling, nødvendig kontekstoverdragelse og kontrolleret slutresultat. Dokumentér brugerindgreb og friktion. Demonstrér genoptagelse, hvis forløbet kræver det. Tving ikke flere agenter ind i en opgave alene for demonstrationen.

4. Produktet hænger sammen
Skill, referencer, templates, eksempler, installationsvejledning og versionsstatus er indbyrdes konsistente. Direkte arbejde er standard; én specialist kan bruges for ekspertise eller frisk kontekst, og parallelle jobs kræver uafhængige input og passende isolation. Overdragelser bevarer ejerskab, nødvendige artefakter og acceptkriterier. Relevante eksisterende checks består på den konkrete version, også på det installerede indhold. Kendte fejl, der hindrer de lovede brugerforløb, er løst. Ny research eller flere regler skal begrundes i et konkret behov.

5. Den færdige version kan tages i brug
Ændringerne er samlet, reviewet og publiceret på main inden for det aktuelle mandat. Den aftalte projektinstallation bruger denne version. Projektstatus viser præcis leverance og evidens. Ingen nødvendige opgaver gemmes som fremtidige forbedringer; øvrige idéer får en kort backlog.

# Afgrænsning og bevis

AMC forbliver en portabel skill, hvor hosten leverer agenter, værktøjer og isolation.

Ingen stor benchmarkkampagne. Brug målrettede engineering-checks og konkret brugserfaring. Påstande om generelt bedre kvalitet, pris eller hastighed kræver særskilt evidens og er ikke nødvendige for denne exit gate.

Headless automatisering er ikke et krav. Faktisk brug i hosten er. Hvis en kontrol kræver UI, brug UI-adgang eller identificér den præcise nødvendige brugerhandling.

Et manglende bevis skal stå åbent. Fjern ikke et succeskriterium for at kunne erklære målet nået.

PR #10 og kontrollerne fra 2026-09-23 er delmilepæle, ikke denne exit gate.

Udgangspunktet er `main` ved `3f35485`. Hele repoet, den tilgængelige historik, PR #7–10 og de eksisterende lokale ændringer indgår i gennemgangen. Aktuel fremdrift og fastlagte kontroller står i `MISSION.md`.

_Opdateret: 2026-09-24_
