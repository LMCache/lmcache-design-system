"""The field vocabulary shared by every LMCache event template.

One name per field, across all twelve SVG templates and the landing page.
Before this file existed, the same two fields were called EVENT/TITLE LINE 2
on the squares, HEADLINE/SECOND LINE on the posters, and HEADLINE/LINE TWO on
the social cards, which made filling a whole set for one event a manual job.

`_build_templates.py` validates the generated SVGs against this registry and
fails the build on any placeholder that is not declared here. `events/fill.py`
reads it to check an event file before rendering. Adding a field means adding
it here first.
"""

# name -> (required?, one-line description shown in generated event files)
FIELDS = {
    # ── Event identity: on nearly every surface ──────────────────────
    'KICKER':        (True,  'Eyebrow, set in caps. The series line — "LMCache SF Bay · Workshop"'),
    'TITLE_1':       (True,  'First title line. White on dark, Ink on light'),
    'TITLE_2':       (True,  'Second title line, set in teal. Two lines is the limit'),
    'STANDFIRST':    (True,  'One line on what it is. Read after the title, before the details'),

    # ── The square card's blurb ─────────────────────────────────────
    # Two fields, not one, because SVG does not wrap: the break is a decision
    # someone makes rather than one the renderer makes badly. ~44 characters
    # a line. This is the only body copy on the square, so it carries the
    # whole answer to "what kind of afternoon is this".
    # Three lines, because line count sets the type size: the widest line is
    # what has to fit 936px. Measured in Geist Medium — two lines capped the
    # type at 41px, three allow 52px, and the plus signs live in a gutter so
    # they cost the binding line nothing. Keep each under about 28 characters;
    # every character you add here comes out of the type size at thumbnail.
    'BLURB_1':       (True,  'Square card, line 1 — keep under ~28 characters'),
    'BLURB_2':       (True,  'Square card, line 2 — keep under ~28 characters'),
    'BLURB_3':       (True,  'Square card, line 3 — keep under ~28 characters'),

    # ── When and where ──────────────────────────────────────────────
    'DATE':          (True,  'Human-readable date — "Tue 6 October 2026"'),
    'TIME':          (True,  'Start and end with timezone — "1:30-5:30 PM PT"'),
    'VENUE':         (True,  'Building or host name — "Samsung"'),
    'CITY':          (True,  'City and region — "San Jose, CA"'),

    # ── Registration ────────────────────────────────────────────────
    'QR':            (False, 'Label under the QR well. The code itself is dropped in at export'),

    # ── Three value lines: the square card and the banner ────────────
    # Stated once, drawn on both. On the square they fill the band the title
    # does not use; on the banner they are the read at walking pace. Keep the
    # last one for networking at a meetup — it is half of why people come.
    'POINT_1':       (True,  'Value line 1 — what you will actually do'),
    'POINT_2':       (True,  'Value line 2 — who is speaking, or what you get'),
    'POINT_3':       (True,  'Value line 3 — the networking or social line'),

    # ── Sponsors, in the order they should be read ───────────────────
    'SPONSOR_1':     (True,  'First sponsor, named in reading order'),
    'SPONSOR_2':     (True,  'Second sponsor'),

    # ── Table tent: one per session, not one per event ───────────────
    'SESSION':       (False, 'Session eyebrow — "Deep dive"'),
    'SESSION_TITLE': (False, 'Session title'),
    'SPEAKER':       (False, 'Speaker name'),
    'AFFILIATION':   (False, 'Speaker or attendee organisation'),

    # ── Name badge: one per attendee ────────────────────────────────
    'EVENT_SHORT':   (False, 'Short event name for the badge header — under 24 characters'),
    'FIRST_NAME':    (False, 'Given name, set large. 14 characters at 11mm'),
    'LAST_NAME':     (False, 'Family name'),
    'ROLE':          (False, 'Badge stripe label — SPEAKER, HOST, ATTENDEE'),
}

# Which fields each template consumes. Kept here so `fill.py` can render a
# subset without hunting through the SVGs, and so a missing field is reported
# against the template that actually wants it.
# The square deliberately carries less than every other surface. It sits above
# a page that already states the date, the address, and the agenda, and a
# thumbnail that repeats all of it is a worse version of that page rather than
# an entry to it. Date, time, venue, and city are not on this list on purpose.
SQUARE = ('KICKER', 'TITLE_1', 'TITLE_2', 'BLURB_1', 'BLURB_2', 'BLURB_3',
          'SPONSOR_1', 'SPONSOR_2')

TEMPLATE_FIELDS = {
    'event-square-1080.svg':            SQUARE,
    'event-square-1200.svg':            SQUARE,
    'event-square-1080-light.svg':      SQUARE,
    'social-og-1200x630.svg':           ('KICKER', 'TITLE_1', 'TITLE_2', 'STANDFIRST'),
    'social-linkedin-1200x627.svg':     ('KICKER', 'TITLE_1', 'TITLE_2', 'STANDFIRST'),
    'social-x-1600x900.svg':            ('KICKER', 'TITLE_1', 'TITLE_2', 'STANDFIRST'),
    'poster-a2-420x594.svg':            ('KICKER', 'TITLE_1', 'TITLE_2', 'STANDFIRST', 'DATE', 'VENUE', 'QR'),
    'poster-a1-594x841.svg':            ('KICKER', 'TITLE_1', 'TITLE_2', 'STANDFIRST', 'DATE', 'VENUE', 'QR'),
    'poster-24x36in.svg':               ('KICKER', 'TITLE_1', 'TITLE_2', 'STANDFIRST', 'DATE', 'VENUE', 'QR'),
    'banner-retractable-850x2000.svg':  ('KICKER', 'TITLE_1', 'TITLE_2', 'STANDFIRST',
                                         'POINT_1', 'POINT_2', 'POINT_3', 'QR'),
    'table-tent-a5.svg':                ('SESSION', 'SESSION_TITLE', 'SPEAKER', 'AFFILIATION'),
    'name-badge-4x3in.svg':             ('EVENT_SHORT', 'FIRST_NAME', 'LAST_NAME', 'AFFILIATION', 'ROLE'),
}

# Templates filled once per event, versus once per session or per person.
PER_EVENT   = tuple(k for k in TEMPLATE_FIELDS if k not in ('table-tent-a5.svg', 'name-badge-4x3in.svg'))
PER_SESSION = ('table-tent-a5.svg',)
PER_PERSON  = ('name-badge-4x3in.svg',)


def unknown(names):
    """Return the names that are not declared fields, in the order given."""
    return [n for n in names if n not in FIELDS]


def missing(template, provided):
    """Required fields this template wants that `provided` does not supply."""
    return [f for f in TEMPLATE_FIELDS.get(template, ())
            if FIELDS[f][0] and f not in provided]


# ── The landing page ────────────────────────────────────────────────
# event-landing.html wants everything the print set wants, plus prose and
# links that only a web page has room for. Same vocabulary, more of it.
PAGE_FIELDS = {
    'TITLE_FULL':       (True,  'Full title on one line, for <title> and og:title'),
    'LEAD':             (True,  'One or two sentences under the title. Say who it is for'),
    'BODY':             (True,  'Two or three paragraphs. Practical details in the first two'),
    'SLUG':             (True,  'URL segment — "2026-10-06-samsung-workshop"'),
    'DAY':              (True,  'Weekday, shown small under the date'),
    'TIMEZONE':         (True,  'Timezone, shown small under the time'),
    'COST':             (True,  'Price or "Free"'),
    'COST_NOTE':        (False, 'Small print under the cost'),
    'REGISTRATION_URL': (True,  'Where Register goes'),
    'CALENDAR_URL':     (False, 'Where Add to calendar goes'),
}

# Repeating blocks on the landing page, marked in the HTML with
# <!-- repeat:NAME --> ... <!-- /repeat -->. One rendering per list entry.
REPEAT_FIELDS = {
    'agenda':   ('AT', 'CLOCK', 'SESSION_TITLE', 'SESSION_NOTE', 'SPEAKER', 'AFFILIATION'),
    'speakers': ('NAME', 'ROLE', 'BIO'),
}
