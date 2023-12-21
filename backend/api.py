import os
import time
import json
from datetime import datetime
from google.cloud import resourcemanager_v3, monitoring_v3, compute_v1
from google.auth import default
from flask import Flask
from flask_restful import Resource, Api
import google.api_core.exceptions
from concurrent.futures import ThreadPoolExecutor
from flask_cors import CORS
from flask import Flask, jsonify

credentials, project = default()
client = resourcemanager_v3.ProjectsClient(credentials=credentials)
compute_client = compute_v1.InstancesClient(credentials=credentials)
os.environ["GOOGLE_CLOUD_QUOTA_PROJECT"] = 'gc-r-prj-samsbx-0001-2043'

zones = ['europe-west2-a', 'europe-west2-b', 'europe-west2-c']

app = Flask("GCP_API")
api = Api(app)
CORS(app)


def cpu_utilization(project_id, zone, instance_id):
    client = monitoring_v3.MetricServiceClient()
    metric_type = "compute.googleapis.com/instance/cpu/utilization"
    resource_name = f"projects/{project_id}/zones/{zone}/instances/{instance_id}"
    interval = monitoring_v3.TimeInterval({"end_time": {"seconds": int(time.time()) - 60}, "start_time": {"seconds": int(time.time() - 3600)}})

    metric_results = client.list_time_series(name=f"projects/{project_id}", filter=f'resource.type="gce_instance" AND resource.label.instance_id="{instance_id}" AND metric.type="{metric_type}"', interval=interval, view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL)

    total_utilization = 0
    count = 0

    for result in metric_results:
        for point in result.points:
            timestamp_seconds = point.interval.end_time.timestamp_pb().seconds + point.interval.end_time.timestamp_pb().nanos / 1e9
            timestamp = datetime.fromtimestamp(timestamp_seconds).strftime('%Y-%m-%d %H:%M:%S')
            total_utilization += point.value.double_value
            count += 1

    if count == 0:
        return "0%"

    average_utilization = total_utilization / count
    return f"{average_utilization * 100:.2f}%"



def vm(project_id):
    VMs = []


    for zone in zones:
        try:
            instances = compute_client.list(project=project_id, zone=zone, timeout=30)


            for instance in instances:
                VMs.append({
                    'Name': instance.name,
                    'ID': instance.id,
                    'Status': instance.status,
                    'Internal_IP': instance.network_interfaces[0].network_i_p,
                    'CPU_Utilization': cpu_utilization(project_id, zone, instance.id)
                })
        except google.api_core.exceptions.NotFound as e:
            print(f"Instance not found in project {project_id} and zone {zone}: {e}")
            continue

    return VMs

            



def projects():
    GCP = []
    projects = list(client.search_projects())

    for project in projects:

        GCP.append({
            'Name': project.display_name,
            'ID':  project.project_id
        })
    
    return (GCP)

class GCP(Resource):
    def get(self, project_id):
        if project_id == "all":
            return jsonify(projects())
        else:
         return (vm(project_id))

api.add_resource(GCP, '/projects/<project_id>')

if __name__ == '__main__':
    app.run(debug=False)