from grow.pods import pods
from grow.pods import storage
from grow.testing import testing
import unittest
import webob.exc


class RoutesTest(unittest.TestCase):

  def setUp(self):
    self.dir_path = testing.create_test_pod_dir()
    self.pod = pods.Pod(self.dir_path, storage=storage.FileStorage)

  def test_match(self):
    self.pod.match('/')
    self.pod.match('/fr/about/')
    self.pod.match('/de_alias/about/')
    self.assertRaises(webob.exc.HTTPNotFound, self.pod.match, '/dummy/')

  def test_list_concrete_paths(self):
    expected = [
        '/',
        '/about/',
        '/app/static/test.txt',
        '/app/static/somepath/de_alias/test.txt',
        '/contact-us/',
        '/de_alias/about/',
        '/de_alias/contact-us/',
        '/de_alias/home/',
        '/de_alias/html/',
        '/de_alias/intro/',
        '/de_alias/yaml_test/',
        '/fr/about/',
        '/fr/contact-us/',
        '/fr/home/',
        '/fr/html/',
        '/fr/intro/',
        '/fr/yaml_test/',
        '/html/',
        '/intro/',
        '/it/about/',
        '/it/contact-us/',
        '/it/home/',
        '/it/html/',
        '/it/intro/',
        '/it/yaml_test/',
        '/post/newer/',
        '/post/newest/',
        '/post/older/',
        '/post/oldest/',
        '/public/file.txt',
        '/public/main.css',
        '/public/main.min.js',
        '/yaml_test/',
    ]
    result = self.pod.routes.list_concrete_paths()
    self.assertItemsEqual(expected, result)


if __name__ == '__main__':
  unittest.main()
