#!/usr/bin/env python
import argparse
import json
import os
import re
from googleapiclient.discovery import build
from oauth2client.client import GoogleCredentials


# Re-runs the specified dataflow jobs. It Uses the environment var 'GOOGLE_APPLICATION_CREDENTIALS' for authentication.
def main(project_id, jobs, suffix):

    credentials = GoogleCredentials.get_application_default()
    service = build('dataflow', 'v1b3', credentials=credentials)

    all_jobs = jobs.split(",")

    for job in all_jobs:

        print 'Working on job id: %s' % (job)

        request = service.projects().jobs().get(projectId=project_id, jobId=job, view='JOB_VIEW_ALL')
        response = str(request.execute())

        # TEMPLATE: u'templateLocation': u'gs://..',
        m = re.search("'templateLocation': u'([:a-zA-Z0-9_/\-\.]*)'", response)
        if m:
            template = m.groups()[0]
        print "Detected original pipeline template file as: '%s'" % (template)

        # FILE: u'strValue': u'gs://..', u'key': u'inputFile'
        m = re.search("u'strValue': u'([:a-zA-Z0-9_/\-\.]*)', u'key': u'inputFile'", response)
        if m:
            file = m.groups()[0]
        print "Detected original pipeline input file as: '%s'" % (file)

        # JOB_NAME: 'name': u'..'
        m = re.search("'name': u'([:a-zA-Z0-9_/\-\.]*)'", response)
        if m:
            job_name = m.groups()[0]
        print "Detected original pipeline job name as: '%s'" % (job_name)

        if suffix is not None:
            job_name = "%s-%s" % (job_name, suffix)

        BODY = {
            "jobName": job_name,
            "parameters": {
                "inputFile": "%s" % (file)
            }
        }

        request = service.projects().templates().launch(projectId=project_id, gcsPath=template, body=BODY)
        response = request.execute()

        print 'Executed templated Dataflow pipeline. HTTP response:\n%s' % (json.dumps(response, indent=4))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--project_id', help='Your GCP project id')
    parser.add_argument('--jobs', help='A comma separated list of job ids to rerun')
    parser.add_argument('--suffix', nargs='?', help='A suffix to add the job name (optional)')
    args = parser.parse_args()
    main(args.project_id, args.jobs, args.suffix)
