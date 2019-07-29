import os
from jinja2 import Environment, FileSystemLoader

import gspread
from oauth2client.service_account import ServiceAccountCredentials

CREDS_FILE = '/Users/michael_musson/Codes/jupyter/notebooks/Operas/python-sheets-1df8b20db8ae.json'

class Render():
    def __init__(self, template_file):
        self.template_file = template_file
        self.sheets = self.sheets_init()

    def sheets_init(self):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
        client = gspread.authorize(creds)
        # Return the set of sheets for this google sheets
        return client.open("Website Content")

    def get_about(self):
        return self.sheets.get_worksheet(0).cell(1, 1).value

    def get_photos(self):
        photos = self.sheets.get_worksheet(1).get_all_values()
        # Split the photos into 4 columns. We're splitting based on
        # if there is a '--' in the cell value in col 1
        idx = []
        for (i, (p, t)) in enumerate(photos):
            if p[:2] == '--':
                idx.append(i)
        return [
            photos[:idx[0]],
            photos[idx[0]+1:idx[1]],
            photos[idx[1]+1:idx[2]],
            photos[idx[2]+1:]
        ]

    def get_recordings(self):
        return self.sheets.get_worksheet(2).get_all_values()

    def get_resume(self):
        return self.sheets.get_worksheet(3).get_all_values()

    def get_engagements(self):
        return self.sheets.get_worksheet(4).get_all_values()

    def render_index(self):
        (template_path, template_file) = os.path.split(self.template_file)
        j2_env = Environment(loader=FileSystemLoader(template_path),
                     trim_blocks=True)
        return j2_env.get_template(template_file).render(
            about_text=self.get_about(),
            photo_set=self.get_photos(),
            recordings=self.get_recordings(),
            resume=self.get_resume(),
            engagements=self.get_engagements(),
        )
