from fabric.api import *
import uuid


env.roledefs = {
    'production': ['chris@178.62.92.190']
}

@roles('production')
def deploy(gitonly=False):
    with cd('/home/chris/flowpatrol'):
        run("git pull")
        run("/home/chris/Env/flowpatrol/bin/pip install -r requirements.txt")
        sudo("service nginx restart")
        sudo("service uwsgi restart")

@roles('production')
def fetch_live_data():
    filename = "flowpatrol_%s.sql" % uuid.uuid4()
    local_path = "~/flowpatrol/tmp/%s" % filename
    remote_path = "/tmp/%s" % filename

    run('pg_dump -Upostgres -cf %s flowpatrol' % remote_path)
    run('gzip %s' % remote_path)
    get("%s.gz" % remote_path, "%s.gz" % local_path)
    run('rm %s.gz' % remote_path)
    local('dropdb -Upostgres flowpatrol')
    local('createdb -Upostgres flowpatrol')
    local('gunzip %s.gz' % local_path)
    local('psql -Upostgres flowpatrol -f %s' % local_path)
    local('rm %s' % local_path)

@roles('production')
def send_live_data():
    filename = "flowpatrol_%s.sql" % uuid.uuid4()
    local_path = "~/flowpatrol/tmp/%s" % filename
    remote_path = "/tmp/%s" % filename

    local('pg_dump -Upostgres -cf %s flowpatrol' % local_path)
    local('gzip %s' % local_path)
    put("%s.gz" % local_path, "%s.gz" % remote_path)
    local('rm %s.gz' % local_path)
    run('dropdb -Upostgres flowpatrol')
    run('createdb -Upostgres flowpatrol')
    run('gunzip %s.gz' % remote_path)
    run('psql -Upostgres flowpatrol -f %s' % remote_path)
    run('rm %s' % remote_path)


def update_upgrade():
    """
        Update the default OS installation's
        basic default tools.
                                            """
    sudo("aptitude update")
    sudo("aptitude -y upgrade")

def install_memcached():
    """ Download and install memcached. """
    sudo("aptitude install -y memcached")

def update_install():

    # Update
    update_upgrade()

    # Install
    install_memcached()