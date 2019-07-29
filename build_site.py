import os
import datetime
import boto3
import glob
import mimetypes
import sass
import argparse
from configparser import ConfigParser
from render_site import Render

class SiteBuilder():

    _css_files = ['style.scss', 'bootstrap.scss']
    _dt_format = '%Y-%m-%d %H:%M:%S'
    _bucket_name = 'lindabairdmezzo.com'
    _include_files = [
        'index.html',
        'favicon.ico',
        'include/css/*.css',
        'include/js/*.js',
        'include/images/*.jpg',
        'include/images/gallery/*.jpg',
        'include/fonts/bootstrap/*',
        'include/fonts/icomoon/*',
        'include/fonts/simple-line-icons/*',
    ]

    def __init__(self,
                 base_path,
                 template_file='index_template.html',
                 config_file='config.ini'):
        self.base_path = base_path
        self.template_file = os.path.join(base_path, template_file)
        self.input_path = os.path.join(base_path, 'sass')
        self.output_path = os.path.join(base_path, 'include/css')
        config = ConfigParser()
        config.read(config_file)
        self.s3_access_key = config.get('s3', 'access_key')
        self.s3_secret_key = config.get('s3', 'private_key')

    def get_last_uploaded(self, ts='ts.txt'):
        ts_file = os.path.join(self.base_path, ts)
        # Get our last upload timestamp
        try:
            with open(ts_file, 'r') as f:
                last_uploaded_raw = f.readlines()[0]
                last_uploaded = datetime.datetime.strptime(last_uploaded_raw, self._dt_format)
        except:
            last_uploaded = datetime.datetime(2000,1,1)
        return last_uploaded

    def set_last_uploaded(self, ts='ts.txt'):
        ts_file = os.path.join(self.base_path, ts)
        tsnow = datetime.datetime.utcnow().strftime(self._dt_format)
        # Get our last upload timestamp
        with open(ts_file, 'w') as f:
            f.write(tsnow)

    def get_file_updated(self, f):
        return datetime.datetime.utcfromtimestamp(os.path.getmtime(f))

    def render_index(self):
        with open(os.path.join(self.base_path, 'index.html'), 'w') as f:
            f.write(Render(os.path.join(self.base_path, 'index_template.html')).render_index())

    def css_compile(self):
        last_uploaded = self.get_last_uploaded()
        for f in self._css_files:
            basename, _ = os.path.splitext(f)
            outfname = os.path.join(self.output_path, basename + '.css')
            fname = os.path.join(self.input_path, f)
            if self.get_file_updated(fname) > last_uploaded:
                compiletime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                compiled_css = sass.compile(filename=fname)
                outfname = os.path.join(self.output_path, basename + '.css')
                with open(outfname, 'w') as of:
                    of.write('// Compiled on {}\n'.format(compiletime))
                    of.write(compiled_css)

    def sync_files(self, ts='ts.txt'):
        s3 = boto3.resource('s3',
                            aws_access_key_id=self.s3_access_key,
                            aws_secret_access_key=self.s3_secret_key,
                           )
        ts_file = os.path.join(self.base_path, ts)
        last_uploaded = self.get_last_uploaded(ts_file)
        nfiles = 0
        for infile in self._include_files:
            for globfile in glob.glob(os.path.join(self.base_path, infile)):
                if self.get_file_updated(globfile) > last_uploaded:
                    dest_key = os.path.relpath(globfile, self.base_path)
                    mtype, _ = mimetypes.guess_type(globfile)
                    ext = os.path.splitext(globfile)[1]
                    if mtype is None and ext in ['.woff2', '.ttf', '.woff']:
                        mtype = 'font/{}'.format(ext[1:])
                    elif mtype is None:
                        print("!!!! Not handling type of this file: {} !!!".format(globfile))
                    print("{} -> {} ({})".format(globfile, dest_key, mtype))
                    with open(globfile, 'rb') as data:
                        s3.Bucket(self._bucket_name).put_object(Key=dest_key, Body=data, ContentType=mtype)
                    nfiles+=1
        self.set_last_uploaded(ts_file)
        print("{} files uploaded".format(nfiles))

    def update_site(self, deploy=False):
        print("Compiling CSS...")
        self.css_compile()
        self.render_index()
        if deploy:
            print("Syncing files to S3...")
            self.sync_files()
        else:
            print("Not deploying to S3...")

if __name__ == '__main__':
    path = '/Users/michael_musson/Codes/static_website/lindabaird'
    config_file = '/Users/michael_musson/Codes/static_website/config.ini'
    parser = argparse.ArgumentParser()
    parser.add_argument("--deploy", help="deploy the site to S3", action='store_true')
    args = parser.parse_args()
if args.deploy:
    SiteBuilder(path, config_file=config_file).update_site(deploy=True)
else:
    SiteBuilder(path, config_file=config_file).update_site()
