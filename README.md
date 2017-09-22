# cloud-dataflow-zombie
A rather crude Python script to easily rerun failed Cloud Dataflow **templated** pipelines.

https://cloud.google.com/dataflow/

Sometimes your templated Cloud Dataflow pipelines will fail due to transiet errors. Or your bad code. Currently, there is no quick/easy way to rerun these failed pipelines. You can rerun the pipelines via the GCP console (_"Create job from template"_), but that requires a gazillion clicks, and you also have to remember all the paramter names/values/formats that it needs.

https://cloud.google.com/dataflow/docs/templates/executing-templates

This script is designed to work with our pipelines that are triggered by a new file (`inputFile`) landing in GCS, which automatically triggers a Cloud Function to execute the templated pipeline, and passes the name of the file to the template parameter `inputFile`. It is then ingested into BigQuery

Although this pattern is specific to our project, you could easily fork and adapt/munge to suit your template. All the script does is it scrapes the Dataflow job(s) details, and uses some gnarly regex to extract all the parameters it needs to execute the template again (yes, regex may break at any time).

e.g. `python rerun.py --project_id=<your_project_id> --jobs=<job_ids> --suffix=<optional_suffix>`

- '--project_id', help='Your GCP project id'
- '--jobs', help='A comma separated list of job ids to rerun'
- '--suffix', nargs='?', help='A suffix to add the job name (optional)'

The script uses the default GCP credentials set to `GOOGLE_APPLICATION_CREDENTIALS` (https://developers.google.com/identity/protocols/application-default-credentials)
