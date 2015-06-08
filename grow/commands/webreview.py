from grow.common import utils
from grow.deployments import deployments
from grow.deployments.destinations import base
from grow.deployments.destinations import webreview_destination
from grow.deployments.stats import stats
from grow.pods import pods
from grow.pods import storage
import click
import os


@click.command()
@click.argument('pod_path', default='.')
@click.option('--build/--nobuild', default=True, is_flag=True,
              help='Whether to build prior to deployment.')
@click.option('--project', help='Project name on webreview server.', required=True)
@click.option('--build_name', help='Build name on webreview server.',
              default=None)
@click.option('--server', help='Webreview server host (and optional port).',
              required=True)
@click.option('--secure', help='Whether to use an https connection to the '
                               'webreview server.', default=True, is_flag=True)
@click.option('--auth', help='Email address to use for oauth2 with webreview.')
@click.option('--api_key', help='Webreview API key.', envvar='WEBREVIEW_API_KEY')
def webreview(pod_path, build, project, build_name, server, secure, auth, api_key):
  """Deploys a pod to a destination."""
  root = os.path.abspath(os.path.join(os.getcwd(), pod_path))
  try:
    pod = pods.Pod(root, storage=storage.FileStorage)
    config = webreview_destination.Config(
        project=project,
        name=build_name,
        server=server,
        secure=secure,
        api_key=api_key)
    deployment = deployments.make_deployment('webreview', config)
    deployment.pod = pod
    if auth:
      deployment.login(auth)
    if build:
      pod.preprocess()
    paths_to_contents = deployment.dump(pod)
    repo = utils.get_git_repo(pod.root)
    stats_obj = stats.Stats(pod, paths_to_contents=paths_to_contents)
    deployment.deploy(paths_to_contents, stats=stats_obj, repo=repo,
                      confirm=False, test=False)
  except base.Error as e:
    raise click.ClickException(str(e))
  except pods.Error as e:
    raise click.ClickException(str(e))
