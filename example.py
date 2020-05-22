"""
An example script to show how to start a Genesis Cloud GPU instance
with custom user data to install the NVIDIA GPU driver.

Grab your API key from the UI and save it in a safe place.
on the shell before running this script

$ export GENESISCLOUD_API_KEY=secretkey
"""
import os
import time
import subprocess as sp


from pygc.client import Client, INSTANCE_TYPES


def get_startup_script():
    return \
"""#!/bin/bash
set -eux

IS_INSTALLED=false
NVIDIA_SHORT_VERSION=430

manual_fetch_install() {
    __nvidia_full_version="430_430.50-0ubuntu2"
    for i in $(seq 1 5)
    do
      echo "Connecting to http://archive.ubuntu.com site for $i time"
      if curl -s --head  --request GET http://archive.ubuntu.com/ubuntu/pool/restricted/n/nvidia-graphics-drivers-"${NVIDIA_SHORT_VERSION}" | grep "HTTP/1.1" > /dev/null ;
      then
          echo "Connected to http://archive.ubuntu.com. Start downloading and installing the NVIDIA driver..."
          __tempdir="$(mktemp -d)"
          apt-get install -y --no-install-recommends "linux-headers-$(uname -r)" dkms
          wget -P "${__tempdir}" http://archive.ubuntu.com/ubuntu/pool/restricted/n/nvidia-graphics-drivers-${NVIDIA_SHORT_VERSION}/nvidia-kernel-common-${__nvidia_full_version}_amd64.deb
          wget -P "${__tempdir}" http://archive.ubuntu.com/ubuntu/pool/restricted/n/nvidia-graphics-drivers-${NVIDIA_SHORT_VERSION}/nvidia-kernel-source-${__nvidia_full_version}_amd64.deb
          wget -P "${__tempdir}" http://archive.ubuntu.com/ubuntu/pool/restricted/n/nvidia-graphics-drivers-${NVIDIA_SHORT_VERSION}/nvidia-dkms-${__nvidia_full_version}_amd64.deb
          dpkg -i "${__tempdir}"/nvidia-kernel-common-${__nvidia_full_version}_amd64.deb "${__tempdir}"/nvidia-kernel-source-${__nvidia_full_version}_amd64.deb "${__tempdir}"/nvidia-dkms-${__nvidia_full_version}_amd64.deb
          wget -P "${__tempdir}" http://archive.ubuntu.com/ubuntu/pool/restricted/n/nvidia-graphics-drivers-${NVIDIA_SHORT_VERSION}/nvidia-utils-${__nvidia_full_version}_amd64.deb
          wget -P "${__tempdir}" http://archive.ubuntu.com/ubuntu/pool/restricted/n/nvidia-graphics-drivers-${NVIDIA_SHORT_VERSION}/libnvidia-compute-${__nvidia_full_version}_amd64.deb
          dpkg -i "${__tempdir}"/nvidia-utils-${__nvidia_full_version}_amd64.deb "${__tempdir}"/libnvidia-compute-${__nvidia_full_version}_amd64.deb
          IS_INSTALLED=true
          rm -r "${__tempdir}"
          break
      fi
      sleep 2
    done
}

apt_fetch_install() {
    add-apt-repository -s -u -y restricted

    # Ubuntu has only a single version in the repository marked as "latest" of
    # this series.
    for _ in $(seq 1 5)
    do
        if apt-get install -y --no-install-recommends nvidia-utils-${NVIDIA_SHORT_VERSION} libnvidia-compute-${NVIDIA_SHORT_VERSION} \
           nvidia-kernel-common-${NVIDIA_SHORT_VERSION} \
           nvidia-kernel-source-${NVIDIA_SHORT_VERSION} \
           nvidia-dkms-${NVIDIA_SHORT_VERSION} \
           "linux-headers-$(uname -r)" dkms; then
           IS_INSTALLED=true
           break
        fi
        sleep 2
    done

}


main() {
    apt-get update
    if grep xenial /etc/os-release; then
        manual_fetch_install
    else
       apt_fetch_install
    fi
    # remove the module if it is inserted, blacklist it
    rmmod nouveau || echo "nouveau kernel module not loaded ..."
    echo "blacklist nouveau" > /etc/modprobe.d/nouveau.conf

    # log insertion of the nvidia module
    # this should always succeed on customer instances
    if modprobe -vi nvidia; then
       nvidia-smi
       modinfo nvidia
       gpu_found=true
    else
       gpu_found=false
    fi

    if [ "${IS_INSTALLED}" = true ]; then
        echo "NVIDIA driver has been successfully installed."
    else
        echo "NVIDIA driver has NOT been installed."
    fi

    if [ "${gpu_found}" ]; then
       echo "NVIDIA GPU device is found and ready"
    else
       echo "WARNING: NVIDIA GPU device is not found or is failed"
    fi
}

main
"""

def create_instance():
    client = Client(os.getenv("GENESISCLOUD_API_KEY"))

    # before we continue to create objects, we check that we can communicate with
    # the API, if the connect method does not succeed it will throw an error
    # and the script will terminate
    if client.connect():
        pass
    # To create an instance you will need an SSH public key.
    # Upload it via the Web UI, you can now find it with.
    # replace this to match your key
    SSHKEYNAME = 'oz123'

    # pygc Instace.find method return generators - that is, they are lazy
    # per-default.

    sshkey_gen = client.SSHKeys.find({"name": SSHKEYNAME})
    sshkey = list(sshkey_gen)[0]

    # You need to tell the client which OS should be used for your instance
    # One can use a snapshot or a base-os to create a new instance
    ubuntu_18 = [image for image in client.Images.find({"name": 'Ubuntu 18.04'})][0]

    # choose the most simple instance type
    # to see the instance properties, use
    # list(INSTANCE_TYPES.items())[0]
    #
    # ('vcpu-4_memory-12g_disk-80g_nvidia1080ti-1',
    # {'vCPUs': 4, 'RAM': 12, 'Disk': 80, 'GPU': 1})

    instace_type = list(INSTANCE_TYPES.keys())[0]
    # To create an instace use Instances.create
    # You must pass a ssh key to SSH into the machine. Currently, only one
    # SSH key is supported. If you need more use the command
    # `ssh-import-id-gh oz123`
    # it can fetch public key from github.com/oz123.keys
    # *Obviously* __replace__ my user name with YOURS or anyone you TRUST.
    # You should put this in the user_data script. You can add this in the
    # text block that the function `get_startup_script` returns.

    my_instance = client.Instances.create(name="demo",
                                          hostname="demo",
                                          ssh_keys=[sshkey['id']],
                                          image=ubuntu_18['id'],
                                          type=instace_type,
                                          metadata={"startup_script":
                                                    get_startup_script()},
                                          )
    # my_instance is a dictionary containing information about the instance
    # that was just created.
    print(my_instance)
    while my_instance['instance']['status'] != 'active':
        time.sleep(1)
        my_instance = client.Instances.get(my_instance['instance']['id'])
        print(f"{my_instance['instance']['status']}\r", end="")
    print("")
    # yay! the instance is active
    # let's ssh to the public IP of the instance
    public_ip = my_instance['instance']['public_ip']
    print(f"The ssh address of the Instance is: {public_ip}")

    # wait for ssh to become available, this returns exit code other
    # than 0 as long the ssh connection isn't available
    while sp.run(
        ("ssh -l ubuntu -o StrictHostKeyChecking=accept-new "
            "-o ConnectTimeout=50 "
            f"{public_ip} hostname"), shell=True).returncode:
        time.sleep(1)

    print("Congratulations! You genesiscloud instance has been created!")
    print("You can ssh to it with:")
    print(f"ssh -l ubuntu {public_ip}")
    print("Some interesting commands to try at first:")
    print("cloud-init stats # if this is still running, NVIDIA driver is still"
          " installing")
    print("use the following to see cloud-init output in real time:")
    print("sudo tail -f /var/log/cloud-init-output.log")
    return my_instance


def destroy(instance_id):
    # finally destory this instance, when you no longer need it
    client = Client(os.getenv("GENESISCLOUD_API_KEY"))
    client.Instances.delete(id=instance_id)


if __name__ == "__main__":
    instance = create_instance()
    instance_id = instance['instance']['id']
    # destroy(instance_id)
