#!/usr/bin/env python3

from argparse import ArgumentParser
import datetime
import json
import urllib.request

ROW_TITLE_AND_DATE_OFFSET = [
    ('Due date', 0),
    ('Release', 7),
]

GITHUB_BASE_URL = 'https://api.github.com'

KEY_TITLE = 'title'
KEY_DUE = 'due_on'

PROGRAM_DESCRIPTION = 'Generates release calendars for the Android Product Team at Mozilla, e.g. https://wiki.mozilla.org/Mobile/Focus/Android/Train_Schedule'
USAGE = '''%(prog)s owner repo
  e.g. %(prog)s mozilla-mobile focus-android'''

def parse_args():
    p = ArgumentParser(description=PROGRAM_DESCRIPTION, usage=USAGE)
    p.add_argument('owner', help='username who owns repository, e.g. "mozilla-mobile"')
    p.add_argument('repo', help='repository name, e.g. "focus-android"')
    return p.parse_args()

def get_milestone_url(owner, repo):
    return GITHUB_BASE_URL + '/repos/{owner}/{repo}/milestones?state=all&sort=due_on&direction=desc'.format(owner=owner, repo=repo)

def fetch_milestones(owner, repo): # Filter by year, paginate.
    milestoneJSON = urllib.request.urlopen(get_milestone_url(owner, repo)).read()
    return json.loads(milestoneJSON)

def get_milestones_from_raw(raw_milestones):
    all_milestones = [{
        KEY_DUE: datetime.datetime.strptime(milestone[KEY_DUE].split('T')[0], '%Y-%m-%d'),
        KEY_TITLE: milestone[KEY_TITLE],
    } for milestone in raw_milestones if milestone[KEY_DUE]]

    current_year = datetime.datetime.now().year
    return filter(lambda m: m[KEY_DUE].year == current_year, all_milestones)

def generate_table(milestones):
    header_row = ["'''Title'''"] + ["'''{}'''".format(title) for (title, _) in ROW_TITLE_AND_DATE_OFFSET]
    table = [header_row]

    sorted_milestones = sorted(milestones, key=lambda x: x[KEY_DUE]) # asc or desc?
    for milestone in sorted_milestones:
        data_row = [milestone[KEY_TITLE]]
        due_date = milestone[KEY_DUE]
        for (_, days_offset) in ROW_TITLE_AND_DATE_OFFSET:
            col_date = due_date + datetime.timedelta(days=days_offset)
            col_date_str = col_date.strftime('%b %d, %Y')
            data_row.append(col_date_str)
        table.append(data_row)
    return table

def get_wiki_markup(table):
    wiki_markup = '{| class="wikitable" style="padding:10; font-size:100%; text-align:center;"\n'
    for row in table:
        wiki_markup += '|-\n'
        wiki_markup += '| ' + ' || '.join(row) + '\n'
    wiki_markup += '|}'
    return wiki_markup

def main():
    args = parse_args()
    raw_milestones = fetch_milestones(args.owner, args.repo)
    milestones = get_milestones_from_raw(raw_milestones)
    table = generate_table(milestones)
    wiki_markup = get_wiki_markup(table)
    print(wiki_markup)

if __name__ == '__main__':
    main()
