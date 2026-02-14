import streamlit as st

PL = {
    # Page chrome
    "page_title": "Wszystko czego NIE musisz wiedzieć o wyborach 2023",
    "page_header": "Wszystko czego nie musisz wiedzieć o wyborach 2023",
    "lang_toggle": "🇬🇧 English",

    # Navigation
    "view_select": "Wybierz artykuł",
    "view_rejected_leaders": "Jedynki odrzucone przez głosujących",
    "view_biggest_winners": "Najwięksi zwycięzcy, największe porażki",
    "view_simulator": "A co by było gdyby...",
    "view_entropy": "Entropia partyjna",

    # Footer / wordcloud
    "wordcloud_caption": "Najpopularniejsze imiona wśród {count} kandydatów i kandydatek do sejmu",

    # ── Entropy section ──────────────────────────────────────────────
    "entropy_desc": "**Entropia - matematyczna miara niepewności** - w przypadku wyborów możemy użyć tej miary aby odnaleźć listy na których większość głosów skupiona jest na jednym lub kilku kandydatach (niska entropia) oraz takie na których głosy są bardziej równomiernie rozłożone (wysoka entropia)",
    "entropy_low": "Niska",
    "entropy_high": "Wysoka",
    "entropy_subheader": "{text} entropia:\n {list}, okręg {district}",
    "entropy_all": "A tak rozkłada się entropia dla wszystkich list",
    "select_district": "Wybierz okręg",
    "select_list": "Wybierz listę",

    # ── Rejected leaders section ─────────────────────────────────────
    "rejected_header": 'Około 38% głosujących polaków głosuje na "jedynki"',
    "rejected_question": "Ale czy pierwsza pozycja na liście jest gwarancją zwycięstwa?",
    "rejected_answer": "Odpowiedź brzmi **nie** - w {count} przypadkach lider(ka) listy nie uzykał(a) mandatu, chociaż mandat przypadł komu innemu na liście. Szczegóły poniżej",
    "rejected_no_seat_f": "#### **{name}**, pomimo pierwszego miejsca na liście, nie otrzymała mandatu w okręgu {district}",
    "rejected_no_seat_m": "#### **{name}**, pomimo pierwszego miejsca na liście, nie otrzymał mandatu w okręgu {district}",
    "rejected_candidate_votes_f": "Kandydatka komitetu {list} otrzymała {votes} głosów",
    "rejected_candidate_votes_m": "Kandydat komitetu {list} otrzymał {votes} głosów",
    "rejected_winner_f": "Mandat z tej listy zdobyła za to **{name}** startująca z pozycji {position}",
    "rejected_winner_m": "Mandat z tej listy zdobył za to **{name}** startujący z pozycji {position}",
    "rejected_winner_votes_f": "**{name}** otrzymała {votes} głosów, o {diff} więcej niż {loser}",
    "rejected_winner_votes_m": "**{name}** otrzymał {votes} głosów, o {diff} więcej niż {loser}",
    "rejected_expander": "Wszystkie głosy na listę {list_num} w okręgu {district}",

    # ── Biggest winners / losers section ─────────────────────────────
    "biggest_winner_f": "największa zwyciężczyni",
    "biggest_winner_m": "największy zwycięzca",
    "winner_header": "{emoji} {text} wyborów {emoji}",
    "won_seat_f": "**{name}** zdobyła mandat przy zaledwie **{votes}** głosach",
    "won_seat_m": "**{name}** zdobył mandat przy zaledwie **{votes}** głosach",
    "congrats": "gratulujemy",
    "avg_votes": "Przeciętna liczba głosów skutkująca otrzymaniem mandatu to {avg_votes},",
    "dhondt_note": "jednakże, w wyniku działania metody d'Hondta do sejmu wchodzą czasem kandydaci i kandydatki ze znacznie mniejszą liczbą głosów",
    "avg_per_party": "A tak wygląda przeciętna liczba głosów potrzebna do uzyskania mandatu dla każdego ugrupowania:",
    "all_seats": "Wszystkie zdobyte mandaty vs. liczba otrzymanych głosów",
    "biggest_losers": "A najwięksi przegrani?",
    "biggest_loser_f": "największa przegrana",
    "biggest_loser_m": "największy przegrany",
    "loser_header": "{emoji} {text} wyborów {emoji}",
    "lost_seat_f": "**{name}** nie zdobyła mandatu pomimo otrzymania **{votes}** głosów",
    "lost_seat_m": "**{name}** nie zdobył mandatu pomimo otrzymania **{votes}** głosów",
    "no_congrats": "nie gratulujemy",
    "other_losses": "Inne porażki",

    # ── Simulator section ────────────────────────────────────────────
    "sim_results": "Wyniki wyborów przedstawiają się następująco",
    "sim_what_if": "Ale co gdyby coś potoczyło się inaczej? Wybierz scenariusz poniżej",
    "sim_unified_header": "A gdyby poszli razem?",
    "sim_unified_note": (
        "**UWAGA** symulacja jest bardzo uproszczona, zakłada po prostu, "
        "że wszyscy kandydaci z list 2, 3 i 6 należą do tego samego "
        "komitetu przy podziale mandatów metodą d'Hondta. Liczba głosów "
        "na każdego kandydata nie jest zmieniona. Oczywiście w "
        "rzeczywistości rozkład głosów wyglądałby inaczej, zjednoczona "
        "opozycja mogłaby też umieścić znacznie mniej kandydatów i "
        "kandydatek na jednej wspólnej liście."
    ),
    "sim_below_threshold": "{name} poniżej progu wyborczego",
    "sim_unified_list": "Wspólna lista opozycji",
    "sim_select": "Wybierz symulację",
    "sim_unified_opposition": "Zjednoczona opozycja",

    # ── Column / axis labels ─────────────────────────────────────────
    "col_name": "Nazwisko, Imię",
    "col_votes_received": "Otrzymane głosy",
    "col_position": "Pozycja",
    "col_position_on_list": "Pozycja na liście",
    "col_vote_share": "% głosów",
    "col_votes": "Głosy",
    "col_list": "Lista",
    "col_list_num": "Num. listy",
    "col_district": "Okręg",
    "col_pos_short": "Poz. na liście",
    "col_entropy": "Entropia",
    "col_leader": "Lider/Liderka",
    "col_vote_count": "liczba głosów",
    "col_list_lower": "lista",
    "col_district_lower": "okręg wyborczy",
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EN = {
    # Page chrome
    "page_title": "Everything you DON'T need to know about the 2023 Polish elections",
    "page_header": "Everything you don't need to know about the 2023 elections",
    "lang_toggle": "🇵🇱 Polski",

    # Navigation
    "view_select": "Choose an article",
    "view_rejected_leaders": "List leaders rejected by voters",
    "view_biggest_winners": "Biggest winners, biggest losers",
    "view_simulator": "What if…",
    "view_entropy": "Party entropy",

    # Footer / wordcloud
    "wordcloud_caption": "Most popular first names among {count} candidates for the Sejm",

    # ── Entropy section ──────────────────────────────────────────────
    "entropy_desc": "**Entropy — a mathematical measure of uncertainty** — in the context of elections we can use it to find party lists where most votes are concentrated on one or a few candidates (low entropy) and lists where votes are more evenly distributed (high entropy)",
    "entropy_low": "Low",
    "entropy_high": "High",
    "entropy_subheader": "{text} entropy:\n {list}, district {district}",
    "entropy_all": "Entropy across all party lists",
    "select_district": "Select district",
    "select_list": "Select party list",

    # ── Rejected leaders section ─────────────────────────────────────
    "rejected_header": 'About 38% of Polish voters vote for the №1 candidate on the list',
    "rejected_question": "But is being first on the list a guarantee of winning?",
    "rejected_answer": "The answer is **no** — in {count} cases the list leader did not win a seat, even though someone else on the same list did. Details below",
    "rejected_no_seat_f": "#### **{name}**, despite being first on the list, did not win a seat in district {district}",
    "rejected_no_seat_m": "#### **{name}**, despite being first on the list, did not win a seat in district {district}",
    "rejected_candidate_votes_f": "The candidate from {list} received {votes} votes",
    "rejected_candidate_votes_m": "The candidate from {list} received {votes} votes",
    "rejected_winner_f": "The seat from this list was won instead by **{name}**, running from position {position}",
    "rejected_winner_m": "The seat from this list was won instead by **{name}**, running from position {position}",
    "rejected_winner_votes_f": "**{name}** received {votes} votes, {diff} more than {loser}",
    "rejected_winner_votes_m": "**{name}** received {votes} votes, {diff} more than {loser}",
    "rejected_expander": "All votes for list {list_num} in district {district}",

    # ── Biggest winners / losers section ─────────────────────────────
    "biggest_winner_f": "the biggest winner",
    "biggest_winner_m": "the biggest winner",
    "winner_header": "{emoji} {text} of the elections {emoji}",
    "won_seat_f": "**{name}** won a seat with only **{votes}** votes",
    "won_seat_m": "**{name}** won a seat with only **{votes}** votes",
    "congrats": "congratulations",
    "avg_votes": "The average number of votes needed to win a seat is {avg_votes},",
    "dhondt_note": "however, due to the d'Hondt method, some candidates enter the Sejm with far fewer votes",
    "avg_per_party": "Average votes needed to win a seat, by party:",
    "all_seats": "All seats won vs. number of votes received",
    "biggest_losers": "And the biggest losers?",
    "biggest_loser_f": "the biggest loser",
    "biggest_loser_m": "the biggest loser",
    "loser_header": "{emoji} {text} of the elections {emoji}",
    "lost_seat_f": "**{name}** did not win a seat despite receiving **{votes}** votes",
    "lost_seat_m": "**{name}** did not win a seat despite receiving **{votes}** votes",
    "no_congrats": "no congratulations",
    "other_losses": "Other notable losses",

    # ── Simulator section ────────────────────────────────────────────
    "sim_results": "The election results are as follows",
    "sim_what_if": "But what if things had gone differently? Choose a scenario below",
    "sim_unified_header": "What if they ran together?",
    "sim_unified_note": (
        "**NOTE** this simulation is very simplified — it simply assumes "
        "that all candidates from lists 2, 3 and 6 belong to the same "
        "committee when distributing seats via the d'Hondt method. The number "
        "of votes for each candidate is unchanged. Of course, in reality "
        "the vote distribution would look different, and a united opposition "
        "could also field far fewer candidates on one common list."
    ),
    "sim_below_threshold": "{name} below the electoral threshold",
    "sim_unified_list": "United opposition list",
    "sim_select": "Choose a simulation",
    "sim_unified_opposition": "United opposition",

    # ── Column / axis labels ─────────────────────────────────────────
    "col_name": "Surname, Name",
    "col_votes_received": "Votes received",
    "col_position": "Position",
    "col_position_on_list": "Position on list",
    "col_vote_share": "% of votes",
    "col_votes": "Votes",
    "col_list": "List",
    "col_list_num": "List no.",
    "col_district": "District",
    "col_pos_short": "List pos.",
    "col_entropy": "Entropy",
    "col_leader": "Leader",
    "col_vote_count": "vote count",
    "col_list_lower": "list",
    "col_district_lower": "electoral district",
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TRANSLATIONS = {"pl": PL, "en": EN}


def get_lang():
    """Get current language from query params, defaulting to 'pl'."""
    return st.query_params.get("lang", "pl")


def t(key, **kwargs):
    """Get translated string for current language, with optional {}-formatting."""
    lang = get_lang()
    template = TRANSLATIONS[lang].get(key, TRANSLATIONS["pl"].get(key, key))
    if kwargs:
        return template.format(**kwargs)
    return template


def g(is_female, key_base, **kwargs):
    """Gender-aware translation: picks key_base + '_f' or '_m'."""
    suffix = "_f" if is_female else "_m"
    return t(key_base + suffix, **kwargs)
