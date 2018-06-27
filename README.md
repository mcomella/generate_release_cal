# Generate Release Calendars
This script is used to generate release calendars for the Android Product Team
at Mozilla, like the one at
https://wiki.mozilla.org/Mobile/Focus/Android/Train_Schedule

Only milestones from the current year will be included in the output.

## Usage
On macOS, run the following command:
```sh
./generate_release_cal.py <owner> <repo> | pbcopy
```

And the wiki markup will be in your clipboard, where:
- owner: username who owns the repository, e.g. mozilla-mobile
- repo: repository name, e.g. focus-android

## Development
To modify the column output, see `ROW_TITLE_AND_DATE_OFFSET`.
