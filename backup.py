#!/usr/bin/env python

"""
User should provide credential for AWS in /home/<username>/.boto

Example
======

[Credentials]
aws_access_key_id = <access-key>
aws_secret_access_key = <secret-access-key>

"""
import sys
import datetime
import boto.ec2

REGION='<region-name>'
TARGET_INSTANCES = ['<instance-id>']

def time_point():
    return datetime.datetime.now().strftime('%Y-%m-%d-%H%M')

def backup():
    conn = boto.ec2.connect_to_region(region_name=REGION)
    if conn:
        reservations = conn.get_all_reservations()
        target_instances = []
        for reservation in reservations:
            if reservation.instances and reservation.instances[0].id in TARGET_INSTANCES:
                target_instances.extend(reservation.instances)
        for instance in target_instances:
            ami_id = instance.create_image(
                name="MSSQL-%s" % time_point(),
                description="Backup from schedule script",
                no_reboot=True,
                dry_run=True
            )
            print 'Backup %s' % ami_id
        else:
            print 'Cannot find target instance.'

    else:
        print "Cannot connect to AWS."
        sys.exit(1)

if __name__ == '__main__':
    print "Start backup process on %s." % time_point()
    backup()
