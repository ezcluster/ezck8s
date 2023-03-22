
mkfs.xfs incompatibility whith RHEL/Centos7.X

On a CentOS 7.9, when running a pod with a PVC on topolvm, I have the following error:

```
Events:
  Type     Reason                  Age                From                     Message
  ----     ------                  ----               ----                     -------
  Normal   Scheduled               <unknown>                                   Successfully assigned default/visitor to kspray1
  Normal   SuccessfulAttachVolume  52s                attachdetach-controller  AttachVolume.Attach succeeded for volume "pvc-de572ac9-12c2-4ee8-89ec-a46cb001d435"
  Warning  FailedMount             16s (x7 over 48s)  kubelet, kspray1         MountVolume.SetUp failed for volume "pvc-de572ac9-12c2-4ee8-89ec-a46cb001d435" : rpc error: code = Internal desc = mount failed: volume=a3c69f68-2e6d-4ce3-8dcc-0dcaf993f3b6, error=invalid argument
```

Digging a bit, it appears than the XFS file system created by the latest version of topolvm (based on ubuntu 20.04) is incompatible with an host on centOS 7.9 (and, I think older version).

- centos7.9 host mkfs.xfs version: 4.5.0
- ubuntu 20.04 (topolvm base image) mkfs.xfs version: 5.3.0

Digging a bit more, it appears than the latest version, by default, add some metadata (`rmapbt` and `reflink`) which break compatibility with older version. 

The good news is by switching these metadata off, the resulting filesystem is compatible with older;

So, as a matter of proof, here is how I can temporary fix this, when there is a pod in the state described above:

```
# Log on the topolvm node

# kubectl -n topolvm-system exec -it node-dvcb6 -c topolvm-node  -- /bin/bash

# There is only on PV/PVC for this test. So here is the device uncorrectly formatted
# ls /dev/topolvm/
0d8a492d-7d34-4dc3-b020-76b3bad10eef

# Perform mkfs.xfs with option to remove some metadata
mkfs.xfs -f -m rmapbt=0,reflink=0 /dev/topolvm/0d8a492d-7d34-4dc3-b020-76b3bad10eef
meta-data=/dev/topolvm/0d8a492d-7d34-4dc3-b020-76b3bad10eef isize=512    agcount=4, agsize=65536 blks
         =                       sectsz=512   attr=2, projid32bit=1
         =                       crc=1        finobt=1, sparse=1, rmapbt=0
         =                       reflink=0
data     =                       bsize=4096   blocks=262144, imaxpct=25
         =                       sunit=0      swidth=0 blks
naming   =version 2              bsize=4096   ascii-ci=0, ftype=1
log      =internal log           bsize=4096   blocks=2560, version=2
         =                       sectsz=512   sunit=0 blks, lazy-count=1
realtime =none                   extsz=4096   blocks=0, rtextents=0

```

Then, on next retry, the volume is mounted and the requesting pod is launched successfully.

```
Events:
  Type     Reason                  Age                From                     Message
  ----     ------                  ----               ----                     -------
  Normal   Scheduled               <unknown>                                   Successfully assigned default/visitor to kspray1
  Normal   SuccessfulAttachVolume  20m                attachdetach-controller  AttachVolume.Attach succeeded for volume "pvc-763c78ba-2eb3-45d0-badc-b28d4b39d597"
  Warning  FailedMount             19m (x7 over 20m)  kubelet, kspray1         MountVolume.SetUp failed for volume "pvc-763c78ba-2eb3-45d0-badc-b28d4b39d597" : rpc error: code = Internal desc = mount failed: volume=0d8a492d-7d34-4dc3-b020-76b3bad10eef, error=invalid argument
  Normal   Pulling                 19m                kubelet, kspray1         Pulling image "centos"
  Normal   Pulled                  19m                kubelet, kspray1         Successfully pulled image "centos" in 1.4883742s
  Normal   Created                 19m                kubelet, kspray1         Created container visitor
  Normal   Started                 19m                kubelet, kspray1         Started container visitor

```

So, I suggest you add these options (`-m rmapbt=0,reflink=0`) in the mkfs.xfs performed by the topolvm dameonset.

(In the meantime, I will switch to ext4).

Best regards

-------------------------------------------------------------------------


I can fix this by login on the node and manually perform the mkfs.xfs on the created logical volume. But, of course, not a practicable solution :).

Digging a bit, it appears than the XFS file system created by the latest version of topolvm (based on ubuntu 20.04) is incompatible with an host on centOS 7.9 (and, I think older version).

centos7.9 host mkfs.xfs version: 4.5.0
ubuntu 20.04 (topolvm base image) mkfs.xfs version: 5.3.0

Digging a bit more, it appears than the latest version, by default, add some metadata which break compatibility with older version. 

The good news is by switching these metadata off, the resulting filesystem is compatible with older;

So, by issuing  mkfs.xfs -m rmapbt=0,reflink=0 ..., the resulting filesystem will be mount-able by a CentOS node.

Could you include this patch in your next release.

(Will use ext4, as a quick workaround).


Here is what I did to be sure of this.

On my node (centos), I copied the mkfs.xfs of the topolvm node container in /tmp and renamed mkfs.xfs.5.3.0 (Which is its version)

cat /etc/redhat-release
CentOS Linux release 7.9.2009 (Core)

mkfs.xfs -V
mkfs.xfs version 4.5.0

/tmp/mkfs.xfs.5.3.0 -V
mkfs.xfs.5.3.0 version 5.3.0

lvcreate -L 2G -n test topolvm-tlvm1
   Logical volume "test" created.
   
/tmp/mkfs.xfs.5.3.0 /dev/topolvm-tlvm1/test
meta-data=/dev/topolvm-tlvm1/test isize=512    agcount=4, agsize=131072 blks
         =                       sectsz=512   attr=2, projid32bit=1
         =                       crc=1        finobt=1, sparse=1, rmapbt=0
         =                       reflink=1
data     =                       bsize=4096   blocks=524288, imaxpct=25
         =                       sunit=0      swidth=0 blks
naming   =version 2              bsize=4096   ascii-ci=0, ftype=1
log      =internal log           bsize=4096   blocks=2560, version=2
         =                       sectsz=512   sunit=0 blks, lazy-count=1
realtime =none                   extsz=4096   blocks=0, rtextents=0


mount /dev/topolvm-tlvm1/test /mnt
mount: wrong fs type, bad option, bad superblock on /dev/mapper/topolvm--tlvm1-test,
       missing codepage or helper program, or other error

       In some cases useful info is found in syslog - try
       dmesg | tail or so.
       
       
mkfs.xfs -f /dev/topolvm-tlvm1/test
meta-data=/dev/topolvm-tlvm1/test isize=512    agcount=4, agsize=131072 blks
         =                       sectsz=512   attr=2, projid32bit=1
         =                       crc=1        finobt=0, sparse=0
data     =                       bsize=4096   blocks=524288, imaxpct=25
         =                       sunit=0      swidth=0 blks
naming   =version 2              bsize=4096   ascii-ci=0 ftype=1
log      =internal log           bsize=4096   blocks=2560, version=2
         =                       sectsz=512   sunit=0 blks, lazy-count=1
realtime =none                   extsz=4096   blocks=0, rtextents=0


mount /dev/topolvm-tlvm1/test /mnt
echo $?
0

umount  /mnt


/tmp/mkfs.xfs.5.3.0 -m rmapbt=0,reflink=0 /dev/topolvm-tlvm1/test
meta-data=/dev/topolvm-tlvm1/test isize=512    agcount=4, agsize=131072 blks
         =                       sectsz=512   attr=2, projid32bit=1
         =                       crc=1        finobt=1, sparse=1, rmapbt=0
         =                       reflink=0
data     =                       bsize=4096   blocks=524288, imaxpct=25
         =                       sunit=0      swidth=0 blks
naming   =version 2              bsize=4096   ascii-ci=0, ftype=1
log      =internal log           bsize=4096   blocks=2560, version=2
         =                       sectsz=512   sunit=0 blks, lazy-count=1
realtime =none                   extsz=4096   blocks=0, rtextents=0
[root@kspray1 topolvm]#


mount /dev/topolvm-tlvm1/test /mnt
echo $?
0

umount  /mnt

lvremove /dev/topolvm-tlvm1/test




