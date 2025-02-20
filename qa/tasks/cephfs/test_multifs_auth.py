"""
Test for Ceph clusters with multiple FSs.
"""
import logging

from tasks.cephfs.cephfs_test_case import CephFSTestCase
from tasks.cephfs.caps_helper import CapTester

from teuthology.exceptions import CommandFailedError


log = logging.getLogger(__name__)


class TestMultiFS(CephFSTestCase):
    client_id = 'testuser'
    client_name = 'client.' + client_id
    # one dedicated for each FS
    MDSS_REQUIRED = 2
    CLIENTS_REQUIRED = 2

    def setUp(self):
        super(TestMultiFS, self).setUp()

        self.captester = CapTester()

        # we might have it - the client - if the same cluster was used for a
        # different vstart_runner.py run.
        self.run_ceph_cmd(f'auth rm {self.client_name}')

        self.fs1 = self.fs
        self.fs2 = self.mds_cluster.newfs(name='cephfs2', create=True)

        # we'll reassign caps to client.1 so that it can operate with cephfs2
        self.run_ceph_cmd(f'auth caps client.{self.mount_b.client_id} mon '
                          f'"allow r" osd "allow rw '
                          f'pool={self.fs2.get_data_pool_name()}" mds allow')
        self.mount_b.remount(cephfs_name=self.fs2.name)


class TestMONCaps(TestMultiFS):

    def test_moncap_with_one_fs_names(self):
        moncap = f'allow r fsname={self.fs1.name}'
        self.create_client(self.client_id, moncap)

        self.captester.run_mon_cap_tests(self.fs1, self.client_id)

    def test_moncap_with_multiple_fs_names(self):
        moncap = (f'allow r fsname={self.fs1.name}, '
                  f'allow r fsname={self.fs2.name}')
        self.create_client(self.client_id, moncap)

        self.captester.run_mon_cap_tests(self.fs1, self.client_id)

    def test_moncap_with_blanket_allow(self):
        moncap = 'allow r'
        self.create_client(self.client_id, moncap)

        self.captester.run_mon_cap_tests(self.fs1, self.client_id)


#TODO: add tests for capsecs 'p' and 's'.
class TestMDSCaps(TestMultiFS):
    """
    0. Have 2 FSs on Ceph cluster.
    1. Create new files on both FSs.
    2. Create a new client that has authorization for both FSs.
    3. Remount the current mounts with this new client.
    4. Test read and write on both FSs.
    """
    def setUp(self):
        super(self.__class__, self).setUp()
        self.mounts = (self.mount_a, self.mount_b)

    def test_rw_with_fsname_and_no_path_in_cap(self):
        PERM = 'rw'
        self.captester.write_test_files(self.mounts)
        keyring_paths = self._create_client(PERM, fsname=True)
        self.remount_with_new_client(keyring_paths)

        self.captester.run_mds_cap_tests(PERM)

    def test_r_with_fsname_and_no_path_in_cap(self):
        PERM = 'r'
        self.captester.write_test_files(self.mounts)
        keyring_paths = self._create_client(PERM, fsname=True)
        self.remount_with_new_client(keyring_paths)

        self.captester.run_mds_cap_tests(PERM)

    def test_rw_with_fsname_and_path_in_cap(self):
        PERM, CEPHFS_MNTPT = 'rw', 'dir1'
        self.mount_a.run_shell(f'mkdir {CEPHFS_MNTPT}')
        self.mount_b.run_shell(f'mkdir {CEPHFS_MNTPT}')
        self.captester.write_test_files(self.mounts, CEPHFS_MNTPT)
        keyring_paths = self._create_client(PERM, fsname=True)
        self.remount_with_new_client(keyring_paths, CEPHFS_MNTPT)

        self.captester.run_mds_cap_tests(PERM, CEPHFS_MNTPT)

    def test_r_with_fsname_and_path_in_cap(self):
        PERM, CEPHFS_MNTPT = 'r', 'dir1'
        self.mount_a.run_shell(f'mkdir {CEPHFS_MNTPT}')
        self.mount_b.run_shell(f'mkdir {CEPHFS_MNTPT}')
        self.captester.write_test_files(self.mounts, CEPHFS_MNTPT)
        keyring_paths = self._create_client(PERM, fsname=True)
        self.remount_with_new_client(keyring_paths, CEPHFS_MNTPT)

        self.captester.run_mds_cap_tests(PERM, CEPHFS_MNTPT)

    # XXX: this tests the backward compatibility; "allow rw path=<dir1>" is
    # treated as "allow rw fsname=* path=<dir1>"
    def test_rw_with_no_fsname_and_path_in_cap(self):
        PERM, CEPHFS_MNTPT = 'rw', 'dir1'
        self.mount_a.run_shell(f'mkdir {CEPHFS_MNTPT}')
        self.mount_b.run_shell(f'mkdir {CEPHFS_MNTPT}')
        self.captester.write_test_files(self.mounts, CEPHFS_MNTPT)
        keyring_paths = self._create_client(PERM)
        self.remount_with_new_client(keyring_paths, CEPHFS_MNTPT)

        self.captester.run_mds_cap_tests(PERM, CEPHFS_MNTPT)

    # XXX: this tests the backward compatibility; "allow r path=<dir1>" is
    # treated as "allow r fsname=* path=<dir1>"
    def test_r_with_no_fsname_and_path_in_cap(self):
        PERM, CEPHFS_MNTPT = 'r', 'dir1'
        self.mount_a.run_shell(f'mkdir {CEPHFS_MNTPT}')
        self.mount_b.run_shell(f'mkdir {CEPHFS_MNTPT}')
        self.captester.write_test_files(self.mounts, CEPHFS_MNTPT)
        keyring_paths = self._create_client(PERM)
        self.remount_with_new_client(keyring_paths, CEPHFS_MNTPT)

        self.captester.run_mds_cap_tests(PERM, CEPHFS_MNTPT)

    def test_rw_with_no_fsname_and_no_path(self):
        PERM = 'rw'
        self.captester.write_test_files(self.mounts)
        keyring_paths = self._create_client(PERM)
        self.remount_with_new_client(keyring_paths)

        self.captester.run_mds_cap_tests(PERM)

    def test_r_with_no_fsname_and_no_path(self):
        PERM = 'r'
        self.captester.write_test_files(self.mounts)
        keyring_paths = self._create_client(PERM)
        self.remount_with_new_client(keyring_paths)

        self.captester.run_mds_cap_tests(PERM)

    def tearDown(self):
        self.mount_a.umount_wait()
        self.mount_b.umount_wait()

        super(type(self), self).tearDown()

    def generate_caps(self, perm, fsname, cephfs_mntpt):
        moncap = 'allow r'
        osdcap = (f'allow {perm} tag cephfs data={self.fs1.name}, '
                  f'allow {perm} tag cephfs data={self.fs2.name}')

        if fsname:
            if cephfs_mntpt == '/':
                mdscap = (f'allow {perm} fsname={self.fs1.name}, '
                          f'allow {perm} fsname={self.fs2.name}')
            else:
                mdscap = (f'allow {perm} fsname={self.fs1.name} '
                          f'path=/{cephfs_mntpt}, '
                          f'allow {perm} fsname={self.fs2.name} '
                          f'path=/{cephfs_mntpt}')
        else:
            if cephfs_mntpt == '/':
                mdscap = f'allow {perm}'
            else:
                mdscap = f'allow {perm} path=/{cephfs_mntpt}'

        return moncap, osdcap, mdscap

    def _create_client(self, perm, fsname=False, cephfs_mntpt='/'):
        moncap, osdcap, mdscap = self.generate_caps(perm, fsname,
                                                    cephfs_mntpt)

        keyring = self.create_client(self.client_id, moncap, osdcap, mdscap)
        keyring_paths = []
        for mount_x in self.mounts:
            keyring_paths.append(mount_x.client_remote.mktemp(data=keyring))

        return keyring_paths

    def remount_with_new_client(self, keyring_paths, cephfs_mntpt='/'):
        if isinstance(cephfs_mntpt, str) and cephfs_mntpt != '/' :
            cephfs_mntpt = '/' + cephfs_mntpt

        self.mount_a.remount(client_id=self.client_id,
                             client_keyring_path=keyring_paths[0],
                             client_remote=self.mount_a.client_remote,
                             cephfs_name=self.fs1.name,
                             cephfs_mntpt=cephfs_mntpt,
                             hostfs_mntpt=self.mount_a.hostfs_mntpt,
                             wait=True)
        self.mount_b.remount(client_id=self.client_id,
                             client_keyring_path=keyring_paths[1],
                             client_remote=self.mount_b.client_remote,
                             cephfs_name=self.fs2.name,
                             cephfs_mntpt=cephfs_mntpt,
                             hostfs_mntpt=self.mount_b.hostfs_mntpt,
                             wait=True)


class TestClientsWithoutAuth(TestMultiFS):
    # c.f., src/mount/mtab.c: EX_FAIL
    RETVAL_KCLIENT = 32
    # c.f., src/ceph_fuse.cc: (cpp EXIT_FAILURE). Normally the check for this
    # case should be anything-except-0, but EXIT_FAILURE is 1 in most systems.
    RETVAL_USER_SPACE_CLIENT = 1

    def setUp(self):
        super(TestClientsWithoutAuth, self).setUp()
        self.retval = self.RETVAL_KCLIENT if 'kernel' in str(type(self.mount_a)).lower() \
            else self.RETVAL_USER_SPACE_CLIENT

    def test_mount_all_caps_absent(self):
        # setup part...
        keyring = self.fs1.authorize(self.client_id, ('/', 'rw'))
        keyring_path = self.mount_a.client_remote.mktemp(data=keyring)

        # mount the FS for which client has no auth...
        try:
            self.mount_a.remount(client_id=self.client_id,
                                 client_keyring_path=keyring_path,
                                 cephfs_name=self.fs2.name,
                                 check_status=False)
        except CommandFailedError as e:
            self.assertEqual(e.exitstatus, self.retval)

    def test_mount_mon_and_osd_caps_present_mds_caps_absent(self):
        # setup part...
        moncap = f'allow rw fsname={self.fs1.name}, allow rw fsname={self.fs2.name}'
        mdscap = f'allow rw fsname={self.fs1.name}'
        osdcap = (f'allow rw tag cephfs data={self.fs1.name}, allow rw tag '
                  f'cephfs data={self.fs2.name}')
        keyring = self.create_client(self.client_id, moncap, osdcap, mdscap)
        keyring_path = self.mount_a.client_remote.mktemp(data=keyring)

        # mount the FS for which client has no auth...
        try:
            self.mount_a.remount(client_id=self.client_id,
                                 client_keyring_path=keyring_path,
                                 cephfs_name=self.fs2.name,
                                 check_status=False)
        except CommandFailedError as e:
            self.assertEqual(e.exitstatus, self.retval)
