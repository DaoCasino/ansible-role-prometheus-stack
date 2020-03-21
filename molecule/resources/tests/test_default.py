import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_docker(host):
    daemon = host.service("docker")
    assert daemon.is_running
    assert daemon.is_enabled


@pytest.mark.parametrize('file, content', [
  ("/etc/prometheus/prometheus.yml", "job_name"),
  ("/etc/prometheus/prometheus.yml", "rule_files")
])
def test_config_file_exists(host, file, content):
    file = host.file(file)

    assert file.exists
    assert file.contains(content)
